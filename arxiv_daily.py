#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arxiv_daily.py — arXiv 每日新增论文摘要器 + 论文下载器

功能:
  1. fetch  : 从指定 arXiv 类别抓取过去 N 小时(默认 24)新增论文,
              生成/更新 arXiv-schedule.md 中以日期(YYYYMMDD)为标题的章节,
              并将原始数据保存为 data/YYYYMMDD.json (供 agent 做推荐)。
              若存在 interests.md, 用其中 keywords 对论文做 🎯 命中标记(★=兴趣点, 🧐=扩展点)。
  2. download: 按 arXiv id 下载 PDF 到 arXiv/ 目录, 自动按仓库命名规则命名:
              "arXiv<年份> <id><版本> <去标点标题>.pdf"
  3. feedback: 人工调整某篇论文的推荐指数(★/🧐 0-5), 同步更新 digest 表格中的指数,
              并据此调整 interests.md 中命中条目的权重(≥4星 +1, ≤2星 -1), 记录到 feedback.jsonl。
  4. reanchor: 为指定日期章节补齐摘要锚点与推荐表 📄 跳转链接(agent 填表后运行)。

用法:
  python arxiv_daily.py fetch [--hours 24] [--cap 100] [--date YYYYMMDD]
  python arxiv_daily.py download <id> [<id> ...]     # 例: 2507.12345
  python arxiv_daily.py feedback <id> [--stars N] [--curiosity N]
  python arxiv_daily.py reanchor [--date YYYYMMDD]
"""

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ---------------------------------------------------------------- 配置

CATEGORIES = [
    "math.LO", "cs.AI", "cs.LG", "cs.DB", "cs.DC",
    "cs.FL", "cs.LO", "cs.PL", "cs.SE",
]

# 摘要清单中每个类别最多列出的论文数(高产类别如 cs.LG 防止刷屏)
DEFAULT_CAP = 100

SCHEDULE_DIR = Path(__file__).resolve().parent          # .../paper-glean
ARXIV_DIR = Path.home() / "papers"                    # configurable paper storage directory
DATA_DIR = SCHEDULE_DIR / "data"
DIGEST_MD = SCHEDULE_DIR / "arXiv-schedule.md"
INTERESTS_MD = SCHEDULE_DIR / "interests.md"      # 兴趣画像(兴趣点/扩展点 keywords+weight)
FEEDBACK_LOG = SCHEDULE_DIR / "feedback.jsonl"    # 人工调整推荐指数的反馈日志

API = "http://export.arxiv.org/api/query"
UA = "arxiv-daily-digest/1.0 (personal research paper collection)"

ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"

HEADER = """# arXiv Daily Digest

> 自动生成的 arXiv 每日新增论文摘要。类别: math.LO, cs.AI, cs.LG, cs.DB, cs.DC, cs.FL, cs.LO, cs.PL, cs.SE。
> 由 `arxiv_daily.py` 抓取; ★/🧐 推荐由 agent 根据研究兴趣补充(见 `README.md`)。
> 推荐指数: ★=基于当前研究兴趣(五星强烈推荐); 🧐=视野扩展(五个强烈推荐)。

"""

# ---------------------------------------------------------------- 抓取


def http_get(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def parse_xml(data: bytes) -> ET.Element:
    """解析 Atom XML; 拒绝含 DTD/实体声明的响应以防实体注入攻击。"""
    head = data[:2048].lstrip()
    if b"<!DOCTYPE" in head or b"<!ENTITY" in head:
        raise ValueError("refusing to parse XML containing DTD/ENTITY declarations")
    return ET.fromstring(data)


def fetch_category(cat: str, start_utc: datetime, end_utc: datetime, max_results: int = 500):
    """按提交时间窗口抓取单个类别的论文条目。"""
    fmt = "%Y%m%d%H%M"
    q = f"cat:{cat} AND submittedDate:[{start_utc.strftime(fmt)} TO {end_utc.strftime(fmt)}]"
    params = {
        "search_query": q,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "start": 0,
        "max_results": max_results,
    }
    url = API + "?" + urllib.parse.urlencode(params)
    root = parse_xml(http_get(url))
    entries = []
    for e in root.findall(ATOM + "entry"):
        raw_id = e.findtext(ATOM + "id", "")          # http://arxiv.org/abs/2507.12345v1
        m = re.search(r"abs/([^v]+)(v\d+)?$", raw_id)
        if not m:
            continue
        short_id, ver = m.group(1), (m.group(2) or "v1")
        prim = e.find(ARXIV_NS + "primary_category")
        entries.append({
            "id": short_id,
            "version": ver,
            "title": re.sub(r"\s+", " ", e.findtext(ATOM + "title", "")).strip(),
            "authors": [a.findtext(ATOM + "name", "").strip()
                        for a in e.findall(ATOM + "author")],
            "abstract": re.sub(r"\s+", " ", e.findtext(ATOM + "summary", "")).strip(),
            "primary": prim.get("term") if prim is not None else cat,
            "categories": [c.get("term") for c in e.findall(ATOM + "category")],
            "published": e.findtext(ATOM + "published", ""),
            "abs_url": f"https://arxiv.org/abs/{short_id}",
            "pdf_url": f"https://arxiv.org/pdf/{short_id}",
        })
    return entries


def fetch_all(hours: int):
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    seen, papers = {}, []
    for cat in CATEGORIES:
        try:
            batch = fetch_category(cat, start, end)
        except Exception as ex:  # 网络失败不阻塞其余类别
            print(f"[WARN] fetch {cat} failed: {ex}", file=sys.stderr)
            batch = []
        for p in batch:
            if p["id"] in seen:                       # 跨类别去重
                continue
            seen[p["id"]] = True
            papers.append(p)
        print(f"[INFO] {cat}: +{len(batch)} (total unique {len(papers)})")
        time.sleep(3)                                 # arXiv API 礼仪
    return papers, start, end


# ---------------------------------------------------------------- 兴趣画像


def load_interest_entries():
    """解析 interests.md, 返回条目列表: {section: star|expand, title, keywords, weight}。"""
    entries = []
    if not INTERESTS_MD.exists():
        return entries
    section, cur = None, None
    for line in INTERESTS_MD.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("## "):
            section = "star" if "兴趣点" in s else ("expand" if "扩展点" in s else None)
            cur = None
        elif s.startswith("### ") and section:
            cur = {"section": section, "title": s[4:].strip(), "keywords": [], "weight": 3}
            entries.append(cur)
        elif cur is not None and s.lower().startswith("- keywords:"):
            cur["keywords"] = [k.strip() for k in s.split(":", 1)[1].split(";") if k.strip()]
        elif cur is not None and s.lower().startswith("- weight:"):
            m = re.search(r"\d+", s)
            if m:
                cur["weight"] = max(1, min(10, int(m.group())))
    return entries


def load_interest_keywords():
    """返回 (兴趣点关键词列表, 扩展点关键词列表)。"""
    star, expand = [], []
    for e in load_interest_entries():
        (star if e["section"] == "star" else expand).extend(e["keywords"])
    return star, expand


def match_keywords(paper, keywords):
    """标题+摘要 中整词匹配(大小写不敏感, 容忍复数形式), 返回命中的关键词。"""
    text = paper["title"] + " " + paper["abstract"]
    hits = []
    for k in keywords:
        if re.search(r"(?<![A-Za-z0-9])" + re.escape(k) + r"(?:e?s)?(?![A-Za-z0-9])",
                     text, re.I):
            hits.append(k)
    return hits


def annotate_hits(papers):
    """为每篇论文添加 hits_star/hits_expand(命中词) 与 score_star/score_expand(命中条目权重和)。"""
    entries = load_interest_entries()
    for p in papers:
        p["hits_star"], p["hits_expand"] = [], []
        p["score_star"] = p["score_expand"] = 0
        for e in entries:
            hit = match_keywords(p, e["keywords"])
            if hit:
                key = e["section"]      # star | expand
                p["hits_" + key].extend(k for k in hit if k not in p["hits_" + key])
                p["score_" + key] += e["weight"]
    return bool(entries)


# ---------------------------------------------------------------- Markdown 生成


def excerpt(text: str, limit: int = 400) -> str:
    """取摘要重点: 前两句, 上限 limit 字符。"""
    parts = re.split(r"(?<=[.!?]) +", text)
    out = " ".join(parts[:2])
    if len(out) > limit:
        out = out[:limit].rsplit(" ", 1)[0] + " …"
    return out


def day_section(day: str, papers, start, end, cap: int) -> str:
    by_cat = {}
    for p in papers:
        key = p["primary"] if p["primary"] in CATEGORIES else \
            next((c for c in p["categories"] if c in CATEGORIES), p["primary"])
        by_cat.setdefault(key, []).append(p)

    n_star = sum(1 for p in papers if p.get("hits_star"))
    n_expand = sum(1 for p in papers if p.get("hits_expand"))
    hit_s = (f" | 🎯 关键词命中(interests.md): ★ {n_star} 篇 / 🧐 {n_expand} 篇"
             if (n_star or n_expand) else "")
    lines = [f"<!-- BEGIN {day} -->",
             f"## {day}",
             "",
             f"时间窗口(UTC): {start:%Y-%m-%d %H:%M} → {end:%Y-%m-%d %H:%M} | "
             f"去重后共 **{len(papers)}** 篇{hit_s}",
             "",
             "### 📌 重点关注(基于研究兴趣, agent 填写)",
             "",
             "_待 agent 分析填写_",
             "",
             "### 🧐 视野扩展(agent 填写)",
             "",
             "_待 agent 分析填写_",
             "",
             "### 分类清单",
             ""]
    for cat in CATEGORIES + sorted(set(by_cat) - set(CATEGORIES)):
        ps = by_cat.get(cat)
        if not ps:
            continue
        # 🎯 命中权重高的论文排在类别前面(稳定排序, 反馈调权直接影响次日排序)
        ps = sorted(ps, key=lambda p: -(p.get("score_star", 0) + p.get("score_expand", 0)))
        shown = ps[:cap]
        lines.append(f"#### {cat} ({len(ps)})")
        lines.append("")
        for p in shown:
            cross = [c for c in p["categories"] if c != p["primary"]]
            cross_s = f" | cross: {', '.join(cross)}" if cross else ""
            hit_s = ""
            if p.get("hits_star"):
                hit_s += f" | 🎯★ {', '.join(p['hits_star'])}"
            if p.get("hits_expand"):
                hit_s += f" | 🎯🧐 {', '.join(p['hits_expand'])}"
            authors = ", ".join(p["authors"][:4]) + (" et al." if len(p["authors"]) > 4 else "")
            lines.append(f"- <a id=\"{day}-{p['id']}\"></a>"
                         f"**{p['title']}** — [{p['id']}]({p['abs_url']}){cross_s}{hit_s}  ")
            lines.append(f"  {authors}  ")
            lines.append(f"  {excerpt(p['abstract'])}")
        if len(ps) > cap:
            lines.append(f"- _…另有 {len(ps) - cap} 篇, 见 `data/{day}.json`_")
        lines.append("")
    lines.append(f"<!-- END {day} -->")
    return "\n".join(lines) + "\n"


def _rec_blocks(sec: str):
    """提取章节中 📌/🧐 两个推荐小节(自 '### 📌'/'### 🧐' 起至下一个 '### ')。"""
    out = {}
    for h in ("### 📌", "### 🧐"):
        i = sec.find(h)
        if i == -1:
            continue
        j = sec.find("\n### ", i)
        out[h] = sec[i:(j + 1) if j != -1 else len(sec)]
    return out


def upsert_digest(day: str, section: str):
    """把当天章节写入 arXiv-schedule.md: 已存在则替换, 否则插入到 HEADER 之后(最新在前)。
    替换时保留 agent 已填写的 📌/🧐 推荐小节(非占位内容)。"""
    if DIGEST_MD.exists():
        content = DIGEST_MD.read_text(encoding="utf-8")
    else:
        content = HEADER
    begin, endm = f"<!-- BEGIN {day} -->", f"<!-- END {day} -->"
    if begin in content and endm in content:
        pre = content[:content.index(begin)]
        old = content[content.index(begin):content.index(endm)]
        post = content[content.index(endm) + len(endm):].lstrip("\n")
        new_blocks = _rec_blocks(section)
        for h, old_block in _rec_blocks(old).items():
            if "_待 agent 分析填写_" not in old_block and h in new_blocks:
                section = section.replace(new_blocks[h], old_block)
        content = pre + section + "\n" + post
    else:
        if "<!-- BEGIN " in content:                  # 插到最近一天之前
            idx = content.index("<!-- BEGIN ")
            content = content[:idx] + section + "\n" + content[idx:]
        else:
            content = content.rstrip("\n") + "\n\n" + section
    DIGEST_MD.write_text(content, encoding="utf-8")


def cmd_fetch(args):
    day = args.date or datetime.now().strftime("%Y%m%d")
    papers, start, end = fetch_all(args.hours)
    if annotate_hits(papers):
        n = sum(1 for p in papers if p["hits_star"] or p["hits_expand"])
        print(f"[INFO] interests.md keywords: {n}/{len(papers)} papers hit")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    data_file = DATA_DIR / f"{day}.json"
    data_file.write_text(
        json.dumps({"day": day, "window_utc": [start.isoformat(), end.isoformat()],
                    "papers": papers}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    upsert_digest(day, day_section(day, papers, start, end, args.cap))
    print(f"[OK] {len(papers)} papers -> {DIGEST_MD.name} section {day}; data -> {data_file}")


# ---------------------------------------------------------------- 反馈学习与锚点维护


def find_paper(pid: str):
    """在 data/*.json 中(从新到旧)查找论文, 返回 (paper, day)。"""
    for f in sorted(DATA_DIR.glob("*.json"), reverse=True):
        data = json.loads(f.read_text(encoding="utf-8"))
        for p in data.get("papers", []):
            if p["id"] == pid:
                return p, data.get("day", f.stem)
    return None, None


def set_entry_weights(new_weights: dict):
    """把 {条目标题: 新权重} 写回 interests.md(更新/插入 '- weight:' 行)。"""
    lines = INTERESTS_MD.read_text(encoding="utf-8").splitlines()
    out, i, n = [], 0, len(lines)
    while i < n:
        s = lines[i].strip()
        out.append(lines[i])
        if s.startswith("### ") and s[4:].strip() in new_weights:
            w = new_weights[s[4:].strip()]
            j = i + 1
            block = []
            while j < n and not lines[j].strip().startswith(("### ", "## ")):
                if not lines[j].strip().lower().startswith("- weight:"):
                    block.append(lines[j])
                j += 1
            k = next((x for x, b in enumerate(block)
                      if b.strip().lower().startswith("- keywords:")), -1)
            block.insert(k + 1, f"- weight: {w}")
            out.extend(block)
            i = j
        else:
            i += 1
    INTERESTS_MD.write_text("\n".join(out) + "\n", encoding="utf-8")


def patch_rating(pid: str, symbol: str, n: int) -> bool:
    """把 digest 推荐表中该论文所在行的推荐指数改为 n 个 symbol。"""
    if not DIGEST_MD.exists():
        return False
    content = DIGEST_MD.read_text(encoding="utf-8")
    pat = re.compile(r"^(\|\s*)(" + symbol + r"+)(\s*\|.*\[" + re.escape(pid) + r"\].*)$",
                     re.M)
    new_content, cnt = pat.subn(lambda m: m.group(1) + symbol * n + m.group(3), content)
    if cnt:
        DIGEST_MD.write_text(new_content, encoding="utf-8")
    return bool(cnt)


def cmd_feedback(args):
    if args.stars is None and args.curiosity is None:
        print("[ERR] 需要 --stars N 和/或 --curiosity N (0-5)")
        return
    paper, day = find_paper(args.id)
    if paper is None:
        print(f"[ERR] {args.id}: 未在 data/*.json 中找到(请先 fetch)")
        return
    entries = load_interest_entries()
    changed, adjustments = {}, []
    for kind, rating, symbol, label in (("star", args.stars, "★", "兴趣点"),
                                        ("expand", args.curiosity, "🧐", "扩展点")):
        if rating is None:
            continue
        rating = max(0, min(5, rating))
        delta = 1 if rating >= 4 else (-1 if rating <= 2 else 0)
        matched = [e for e in entries
                   if e["section"] == kind and match_keywords(paper, e["keywords"])]
        for e in matched:
            if delta:
                changed[e["title"]] = max(1, min(10, e["weight"] + delta))
        patched = patch_rating(args.id, symbol, rating) if rating > 0 else False
        adjustments.append({"kind": kind, "rating": rating, "delta": delta,
                            "matched_entries": [e["title"] for e in matched],
                            "digest_updated": patched})
        print(f"[OK] {symbol}x{rating}"
              f" | 命中{label}条目: {', '.join(e['title'] for e in matched) or '无'}"
              f" | digest 表格{'已更新' if patched else '未找到对应行(跨类调整请交给 agent)'}")
        if not matched and delta > 0:
            print(f"[HINT] 该论文未命中任何{label}条目; 建议让 agent 依据此论文在"
                  f" interests.md 新增{label}(参考 feedback.jsonl 中本条记录)")
    if changed:
        set_entry_weights(changed)
        for t, w in changed.items():
            print(f"[OK] interests.md 权重: {t} -> {w}")
    with FEEDBACK_LOG.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps({
            "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "id": args.id, "day": day, "title": paper["title"],
            "primary": paper["primary"], "abstract_head": excerpt(paper["abstract"], 200),
            "adjustments": adjustments, "weight_updates": changed},
            ensure_ascii=False) + "\n")
    print(f"[OK] 反馈已记录 -> {FEEDBACK_LOG.name}")


def cmd_reanchor(args):
    """为指定日期章节: 分类清单条目补锚点; 推荐表行补 📄 跳转链接。幂等。"""
    day = args.date or datetime.now().strftime("%Y%m%d")
    content = DIGEST_MD.read_text(encoding="utf-8")
    begin, endm = f"<!-- BEGIN {day} -->", f"<!-- END {day} -->"
    if begin not in content or endm not in content:
        print(f"[ERR] digest 中无 {day} 章节")
        return
    i, j = content.index(begin), content.index(endm) + len(endm)
    out, n_anchor, n_link = [], 0, 0
    for line in content[i:j].splitlines():
        if line.startswith("- **") and "<a id=" not in line:
            m = re.search(r"\[([\d.]+)\]\(https://arxiv\.org/abs/", line)
            if m:
                line = line.replace("- **", f'- <a id="{day}-{m.group(1)}"></a>**', 1)
                n_anchor += 1
        elif (line.startswith("|") and ("★" in line or "🧐" in line)
              and f"](#{day}-" not in line):
            m = re.search(r"\[([\d.]+)\]\(https://arxiv\.org/abs/[\d.]+\)", line)
            if m:
                line = line.replace(
                    m.group(0), m.group(0) + f" · [📄](#{day}-{m.group(1)})", 1)
                n_link += 1
        out.append(line)
    DIGEST_MD.write_text(content[:i] + "\n".join(out) + content[j:], encoding="utf-8")
    print(f"[OK] {day}: +{n_anchor} 锚点, +{n_link} 跳转链接")


# ---------------------------------------------------------------- 下载


def sanitize_title(title: str) -> str:
    """按仓库命名规则去标点: 保留连字符, 移除 : ? , . " ' 及 LaTeX 数学记号等。"""
    t = title.replace("\u2013", "-").replace("\u2014", "-")
    # 常见 LaTeX 清理
    t = re.sub(r"\\mathbb\s*\{?([A-Za-z])\}?", r"\1", t)
    t = t.replace("\\varepsilon", "epsilon").replace("\\epsilon", "epsilon")
    t = re.sub(r"[:?,.\"'!;`\u2019\u201c\u201d()\[\]{}<>/\\|*$]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def cmd_download(args):
    for pid in args.ids:
        url = (API + "?" +
               urllib.parse.urlencode({"id_list": pid, "max_results": 1}))
        root = parse_xml(http_get(url))
        e = root.find(ATOM + "entry")
        if e is None or not e.findtext(ATOM + "title"):
            print(f"[ERR] {pid}: not found on arXiv API")
            continue
        raw_id = e.findtext(ATOM + "id", "")
        m = re.search(r"abs/([^v]+)(v\d+)?$", raw_id)
        ver = m.group(2) if m and m.group(2) else "v1"
        title = sanitize_title(re.sub(r"\s+", " ", e.findtext(ATOM + "title", "")).strip())
        year = (e.findtext(ATOM + "published", "") or "XXXX")[:4]
        dest = ARXIV_DIR / f"arXiv{year} {pid}{ver} {title}.pdf"
        pdf_url = f"https://arxiv.org/pdf/{pid}{ver}"
        try:
            data = http_get(pdf_url, timeout=120)
            if not data.startswith(b"%PDF"):
                print(f"[ERR] {pid}: response is not a PDF ({pdf_url})")
                continue
            dest.write_bytes(data)
            print(f"[OK] {len(data):>8} bytes  {dest.name}")
        except Exception as ex:
            print(f"[ERR] {pid}: {ex}")
        time.sleep(3)


# ---------------------------------------------------------------- main


def main():
    if hasattr(sys.stdout, "reconfigure"):      # Windows GBK 控制台兼容
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="arXiv daily digest & downloader")
    sub = ap.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fetch", help="抓取过去 N 小时新增论文并更新 digest")
    f.add_argument("--hours", type=int, default=24)
    f.add_argument("--cap", type=int, default=DEFAULT_CAP,
                   help="digest 中每类别最多列出的论文数")
    f.add_argument("--date", help="覆盖章节日期 YYYYMMDD(默认今天)")
    f.set_defaults(func=cmd_fetch)

    d = sub.add_parser("download", help="按 id 下载 PDF 到 arXiv/ 并按规则命名")
    d.add_argument("ids", nargs="+", help="arXiv id, 例 2507.12345")
    d.set_defaults(func=cmd_download)

    fb = sub.add_parser("feedback", help="人工调整推荐指数并更新兴趣画像权重")
    fb.add_argument("id", help="arXiv id, 例 2507.12345")
    fb.add_argument("--stars", type=int, help="★ 推荐指数 0-5")
    fb.add_argument("--curiosity", type=int, help="🧐 推荐指数 0-5")
    fb.set_defaults(func=cmd_feedback)

    ra = sub.add_parser("reanchor", help="为指定日期章节补齐锚点与推荐表跳转链接")
    ra.add_argument("--date", help="YYYYMMDD(默认今天)")
    ra.set_defaults(func=cmd_reanchor)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
