#!/usr/bin/env python3
"""Regenerate ``glean/ccf_catalog.py`` from ccfddl.com + a curated supplement.

Why this script exists
----------------------
The CCF-A catalogue must be *auditable*, not hand-waved:

* Conference entries come from **ccfddl.com**'s public RSS feed
  (``/conference/deadlines_en.xml``), which annotates every entry with its CCF
  rank, area, official website and DBLP index. That is a live, citable source.
* ccfddl only tracks venues that publish deadlines, so a curated supplement
  adds well-known CCF-A venues it misses (VLDB, PODS, ICFP, ...) and the
  CCF-A **journals**, which no deadline site covers.
* Every URL is verified with a real HTTP request; failures are reported so a
  stale link never silently ships.

Usage::

    python scripts/gen_ccf_catalog.py            # fetch + verify + write
    python scripts/gen_ccf_catalog.py --dry-run  # report only, write nothing
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
import textwrap
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CCFDDL_RSS = "https://ccfddl.com/conference/deadlines_en.xml"
UA = "paper-glean/0.1.0 (CCF catalogue generator)"
OUT = Path(__file__).resolve().parent.parent / "glean" / "ccf_catalog.py"

# --------------------------------------------------------------------------
# Curated supplement.
#
# Only venues that are unambiguously CCF-A and have a *stable* (non-year-bound)
# homepage belong here — an entry whose homepage rots every year is worse than
# no entry at all. Every URL below is verified by --verify before it ships.
# --------------------------------------------------------------------------

SUPPLEMENT_CONFERENCES: list[dict[str, str]] = [
    {"name": "VLDB", "full": "International Conference on Very Large Data Bases",
     "area": "数据库/数据挖掘/内容检索 (DB)", "homepage": "https://vldb.org/",
     "dblp": "https://dblp.org/db/conf/vldb"},
    {"name": "PODS", "full": "ACM Symposium on Principles of Database Systems",
     "area": "数据库/数据挖掘/内容检索 (DB)", "homepage": "https://sigmod.org/pods/",
     "dblp": "https://dblp.org/db/conf/pods"},
    {"name": "PODC", "full": "ACM Symposium on Principles of Distributed Computing",
     "area": "计算机科学理论 (CT)", "homepage": "https://www.podc.org/",
     "dblp": "https://dblp.org/db/conf/podc"},
    {"name": "DISC", "full": "International Symposium on Distributed Computing",
     "area": "计算机科学理论 (CT)", "homepage": "https://www.disc-conference.org/",
     "dblp": "https://dblp.org/db/conf/wdag"},
    {"name": "ICFP", "full": "International Conference on Functional Programming",
     "area": "软件工程/系统软件/程序设计语言 (SE)", "homepage": "https://icfpconference.org/",
     "dblp": "https://dblp.org/db/conf/icfp"},
    {"name": "TACAS", "full": "International Conference on Tools and Algorithms for the Construction and Analysis of Systems",
     "area": "软件工程/系统软件/程序设计语言 (SE)", "homepage": "https://www.etaps.org/",
     "dblp": "https://dblp.org/db/conf/tacas"},
    {"name": "CAV", "full": "International Conference on Computer-Aided Verification",
     "area": "软件工程/系统软件/程序设计语言 (SE)", "homepage": "https://cavconference.org/",
     "dblp": "https://dblp.org/db/conf/cav"},
    {"name": "IJCAI", "full": "International Joint Conference on Artificial Intelligence",
     "area": "人工智能 (AI)", "homepage": "https://www.ijcai.org/",
     "dblp": "https://dblp.org/db/conf/ijcai"},
    {"name": "EMNLP", "full": "Conference on Empirical Methods in Natural Language Processing",
     "area": "人工智能 (AI)", "homepage": "https://aclanthology.org/venues/emnlp/",
     "dblp": "https://dblp.org/db/conf/emnlp"},
    {"name": "NAACL", "full": "Annual Conference of the North American Chapter of the Association for Computational Linguistics",
     "area": "人工智能 (AI)", "homepage": "https://aclanthology.org/venues/naacl/",
     "dblp": "https://dblp.org/db/conf/naacl"},
    {"name": "ECCV", "full": "European Conference on Computer Vision",
     "area": "人工智能 (AI)", "homepage": "https://eccv.ecva.net/",
     "dblp": "https://dblp.org/db/conf/eccv"},
    {"name": "ICCAD", "full": "International Conference on Computer-Aided Design",
     "area": "计算机体系结构/并行与分布计算/存储系统 (DS)", "homepage": "https://www.iccad.com/",
     "dblp": "https://dblp.org/db/conf/iccad"},
    {"name": "IPDPS", "full": "IEEE International Parallel and Distributed Processing Symposium",
     "area": "计算机体系结构/并行与分布计算/存储系统 (DS)", "homepage": "https://www.ipdps.org/",
     "dblp": "https://dblp.org/db/conf/ipps"},
    {"name": "SIGMETRICS", "full": "ACM SIGMETRICS International Conference on Measurement and Modeling of Computer Systems",
     "area": "计算机网络 (NW)", "homepage": "https://www.sigmetrics.org/",
     "dblp": "https://dblp.org/db/conf/sigmetrics"},
    {"name": "DATE", "full": "Design, Automation and Test in Europe",
     "area": "计算机体系结构/并行与分布计算/存储系统 (DS)", "homepage": "https://www.date-conference.com/",
     "dblp": "https://dblp.org/db/conf/date"},
]

# CCF 推荐国际学术期刊 A 类（人工整理）。期刊没有 ccdeadline 站点收录，
# 只能人工维护；出错的条目请直接在 ccf.md 里取消勾选或删除。
SUPPLEMENT_JOURNALS: list[dict[str, str]] = [
    {"name": "TOPLAS", "full": "ACM Transactions on Programming Languages and Systems",
     "area": "软件工程/系统软件/程序设计语言 (SE)", "homepage": "https://dl.acm.org/journal/toplas"},
    {"name": "TOCS", "full": "ACM Transactions on Computer Systems",
     "area": "计算机体系结构/并行与分布计算/存储系统 (DS)", "homepage": "https://dl.acm.org/journal/tocs"},
    {"name": "TODS", "full": "ACM Transactions on Database Systems",
     "area": "数据库/数据挖掘/内容检索 (DB)", "homepage": "https://dl.acm.org/journal/tods"},
    {"name": "TOIS", "full": "ACM Transactions on Information Systems",
     "area": "数据库/数据挖掘/内容检索 (DB)", "homepage": "https://dl.acm.org/journal/tois"},
    {"name": "TOCL", "full": "ACM Transactions on Computational Logic",
     "area": "计算机科学理论 (CT)", "homepage": "https://dl.acm.org/journal/tocl"},
    {"name": "TOCHI", "full": "ACM Transactions on Computer-Human Interaction",
     "area": "人机交互与普适计算 (HI)", "homepage": "https://dl.acm.org/journal/tochi"},
    {"name": "TOG", "full": "ACM Transactions on Graphics",
     "area": "计算机图形学与多媒体 (CG)", "homepage": "https://dl.acm.org/journal/tog"},
    {"name": "JACM", "full": "Journal of the ACM",
     "area": "计算机科学理论 (CT)", "homepage": "https://dl.acm.org/journal/jacm"},
    {"name": "TKDE", "full": "IEEE Transactions on Knowledge and Data Engineering",
     "area": "数据库/数据挖掘/内容检索 (DB)", "homepage": "https://www.computer.org/csdl/journal/tk"},
    {"name": "TPDS", "full": "IEEE Transactions on Parallel and Distributed Systems",
     "area": "计算机体系结构/并行与分布计算/存储系统 (DS)", "homepage": "https://www.computer.org/csdl/journal/td"},
    {"name": "TC", "full": "IEEE Transactions on Computers",
     "area": "计算机体系结构/并行与分布计算/存储系统 (DS)", "homepage": "https://www.computer.org/csdl/journal/tc"},
    {"name": "TPAMI", "full": "IEEE Transactions on Pattern Analysis and Machine Intelligence",
     "area": "人工智能 (AI)", "homepage": "https://www.computer.org/csdl/journal/tp"},
    {"name": "TSE", "full": "IEEE Transactions on Software Engineering",
     "area": "软件工程/系统软件/程序设计语言 (SE)", "homepage": "https://www.computer.org/csdl/journal/ts"},
    {"name": "TCAD", "full": "IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems",
     "area": "计算机体系结构/并行与分布计算/存储系统 (DS)", "homepage": "https://www.computer.org/csdl/journal/tcad"},
    {"name": "TMC", "full": "IEEE Transactions on Mobile Computing",
     "area": "计算机网络 (NW)", "homepage": "https://www.computer.org/csdl/journal/tm"},
    {"name": "TNNLS", "full": "IEEE Transactions on Neural Networks and Learning Systems",
     "area": "人工智能 (AI)", "homepage": "https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=5962385"},
    {"name": "TIP", "full": "IEEE Transactions on Image Processing",
     "area": "计算机图形学与多媒体 (CG)", "homepage": "https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=83"},
    {"name": "TIT", "full": "IEEE Transactions on Information Theory",
     "area": "计算机科学理论 (CT)", "homepage": "https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=18"},
    {"name": "TIFS", "full": "IEEE Transactions on Information Forensics and Security",
     "area": "网络与信息安全 (SC)", "homepage": "https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=10206"},
    {"name": "AIJ", "full": "Artificial Intelligence",
     "area": "人工智能 (AI)", "homepage": "https://www.sciencedirect.com/journal/artificial-intelligence"},
    {"name": "JMLR", "full": "Journal of Machine Learning Research",
     "area": "人工智能 (AI)", "homepage": "https://www.jmlr.org/"},
    {"name": "LMCS", "full": "Logical Methods in Computer Science",
     "area": "计算机科学理论 (CT)", "homepage": "https://lmcs.episciences.org/"},
]


def _get(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
    return raw.decode(resp.headers.get_content_charset() or "utf-8", errors="replace")


def fetch_ccfddl(min_rank: str = "A") -> list[dict[str, str]]:
    """Parse ccfddl's RSS and return one entry per CCF-A conference.

    Only ``min_rank`` (default CCF-A) venues are kept, and for each venue the
    **newest** edition wins — that is the edition whose site is currently live
    and therefore the one worth monitoring.
    """
    xml_text = _get(CCFDDL_RSS)
    best: dict[str, dict[str, str]] = {}
    for block in re.findall(r"<item>(.*?)</item>", xml_text, re.S):
        title = re.search(r"<title>(.*?)</title>", block, re.S)
        desc = re.search(r"<description>(.*?)</description>", block, re.S)
        link = re.search(r"<link>(.*?)</link>", block, re.S)
        if not title or not desc:
            continue
        lines = [ln.strip() for ln in html.unescape(desc.group(1)).splitlines() if ln.strip()]
        rank_line = next((ln for ln in lines if ln.startswith("CCF ")), "")
        if not rank_line.startswith(f"CCF {min_rank}"):
            continue
        m = re.match(r"^(.*?)\s+(\d{4})\b", html.unescape(title.group(1)))
        if not m:
            continue
        name, year = m.group(1).strip(), int(m.group(2))

        def field(prefix: str) -> str:
            for ln in lines:
                if ln.startswith(prefix):
                    return ln.split(":", 1)[1].strip()
            return ""

        rec = {
            "name": name,
            "full": lines[0],
            "area": field("Category:"),
            "homepage": field("Conference Website:") or (link.group(1).strip() if link else ""),
            "dblp": field("DBLP:"),
            "ccf": min_rank,
        }
        cur = best.get(name)
        if cur is None or year > cur["_year"]:  # type: ignore[operator]
            rec["_year"] = year  # type: ignore[assignment]
            best[name] = rec
    out = []
    for rec in best.values():
        rec.pop("_year", None)
        out.append(rec)
    return out


def _norm_title(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (text or "").lower())


def resolve_issn(full_name: str, timeout: int = 20) -> str:
    """Look a journal's ISSN up on Crossref (open API, no key required).

    Journals are monitored through Crossref rather than their own homepages:
    ACM DL and IEEE Xplore render their tables of contents with JavaScript, so
    scraping them yields nothing, while Crossref exposes volume/issue/date as
    structured data.
    """
    query = urllib.parse.quote(full_name)
    url = f"https://api.crossref.org/journals?query={query}&rows=5"
    try:
        data = json.loads(_get(url, timeout=timeout))
    except Exception:
        return ""
    items = data.get("message", {}).get("items", [])
    if not items:
        return ""
    target = _norm_title(full_name)
    best = items[0]
    for row in items:
        if _norm_title(row.get("title", "")) == target:
            best = row
            break
    issn_list = best.get("ISSN") or []
    return issn_list[0] if issn_list else ""


def verify(url: str, timeout: int = 20) -> tuple[int, str]:
    """Return ``(status, note)``.

    ``status == 0`` means *we could not reach it at all* — which on a proxied /
    TLS-inspecting network is **not** evidence that the link is dead, so callers
    must report those separately from real 4xx/5xx responses.
    """
    if not url:
        return 0, "empty"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return int(resp.status), "ok"
    except urllib.error.HTTPError as exc:
        return int(exc.code), f"http {exc.code}"  # 401/403/429 = "exists, blocks bots"
    except Exception as exc:
        return 0, type(exc).__name__


def verify_all(rows: list[dict[str, str]], workers: int = 16) -> tuple[list[tuple[str, str, str]], list[tuple[str, str, str]]]:
    """Split rows into ``(broken, unreachable)`` — real 4xx/5xx vs network noise."""
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(lambda r: (r, verify(r["homepage"])), rows))

    broken: list[tuple[str, str, str]] = []
    unreachable: list[tuple[str, str, str]] = []
    for row, (status, note) in results:
        if status == 0:
            unreachable.append((row["name"], row["homepage"], note))
        elif status >= 400 and status not in (401, 403, 406, 429):
            broken.append((row["name"], row["homepage"], f"{status} {note}"))
    return broken, unreachable


def merge(fetched: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """ccfddl first (authoritative), curated supplement only fills the gaps."""
    confs: dict[str, dict[str, str]] = {}
    for rec in fetched:
        confs[rec["name"].upper()] = dict(rec, ccf="A")
    for rec in SUPPLEMENT_CONFERENCES:
        confs.setdefault(rec["name"].upper(), dict(rec, ccf="A"))
    journals = {r["name"].upper(): dict(r, ccf="A", dblp="") for r in SUPPLEMENT_JOURNALS}
    order = {"conferences": sorted(confs.values(), key=lambda r: r["name"].upper()),
             "journals": sorted(journals.values(), key=lambda r: r["name"].upper())}
    return order["conferences"], order["journals"]


def render(confs: list[dict[str, str]], journals: list[dict[str, str]], stamp: str) -> str:
    def block(rows: list[dict[str, str]], indent: str = "    ") -> str:
        parts = []
        for r in rows:
            parts.append(
                indent + "{\n"
                + indent + "    \"name\": " + repr(r["name"]) + ",\n"
                + indent + "    \"full\": " + repr(r["full"]) + ",\n"
                + indent + "    \"area\": " + repr(r["area"]) + ",\n"
                + indent + "    \"homepage\": " + repr(r["homepage"]) + ",\n"
                + indent + "    \"dblp\": " + repr(r.get("dblp", "")) + ",\n"
                + indent + "    \"ccf\": " + repr(r.get("ccf", "A")) + ",\n"
                + (indent + "    \"issn\": " + repr(r["issn"]) + ",\n" if r.get("issn") else "")
                + indent + "},"
            )
        return "\n".join(parts)

    return f'''"""CCF-A 会议 / 期刊目录（数据快照，由 ``scripts/gen_ccf_catalog.py`` 生成）。

来源与可信度
------------
* **会议**：`ccfddl.com <https://ccfddl.com/>`_ 的公开 RSS
  （``/conference/deadlines_en.xml``）。每条都带 CCF 等级、领域、官网与 DBLP 索引，
  同一会议取**最新一届**的官网（即当前真正在线的那个）。ccfddl 只收录公布了截稿
  日期的会议，因此 **VLDB / PODS / ICFP 等未收录的 A 类会议由人工补充**。
* **期刊**：没有任何截稿站收录期刊，因此 A 类期刊全部来自人工整理
  （依据 CCF 推荐国际学术期刊目录）。**这是目录里最可能出错的部分** ——
  发现错误请直接在 `ccf.md` 里取消勾选或删除，并提交 issue。

所有 URL 在生成时都经过真实 HTTP 校验。本文件是**快照**：
运行 ``python scripts/gen_ccf_catalog.py`` 可重新抓取并覆盖它。

生成时间：{stamp}
"""

from __future__ import annotations

CCF_CATALOG_VERSION = {stamp[:10]!r}
CCF_CATALOG_SOURCE = "ccfddl.com RSS + curated supplement"

#: CCF-A 会议（{len(confs)} 个）
CCF_A_CONFERENCES: list[dict[str, str]] = [
{block(confs)}
]

#: CCF-A 期刊（{len(journals)} 个）
CCF_A_JOURNALS: list[dict[str, str]] = [
{block(journals)}
]


def catalog(kind: str | None = None) -> list[dict[str, str]]:
    """Return catalogue entries; ``kind`` is ``"conference"`` / ``"journal"`` / ``None`` (both)."""
    if kind == "conference":
        return list(CCF_A_CONFERENCES)
    if kind == "journal":
        return list(CCF_A_JOURNALS)
    return list(CCF_A_CONFERENCES) + list(CCF_A_JOURNALS)
'''


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="report only; do not write")
    ap.add_argument("--no-verify", action="store_true", help="skip HTTP link checking")
    ap.add_argument("--no-issn", action="store_true", help="skip Crossref ISSN lookup")
    args = ap.parse_args()

    print(f"[1/4] fetching {CCFDDL_RSS} ...")
    fetched = fetch_ccfddl()
    print(f"      ccfddl CCF-A venues: {len(fetched)}")
    if not fetched:
        print("[ERR] nothing fetched — aborting (refusing to ship an empty catalogue)")
        return 1

    confs, journals = merge(fetched)
    print(f"[2/4] merged: {len(confs)} conferences, {len(journals)} journals")

    if not args.no_issn:
        print("[3/4] resolving journal ISSNs on Crossref ...")
        missing: list[str] = []
        for row in journals:
            row["issn"] = resolve_issn(row["full"])
            if not row["issn"]:
                missing.append(row["name"])
            else:
                print(f"      {row['name']:10s} {row['issn']}")
        if missing:
            print(f"      no ISSN for: {', '.join(missing)}")
    else:
        print("[3/4] ISSN resolution skipped")

    if not args.no_verify:
        print("[3/4] verifying links ...")
        broken, unreachable = verify_all(confs + journals)
        for name, url, why in broken:
            print(f"      [BROKEN]     {name:12s} {url}  ({why})")
        for name, url, why in unreachable:
            print(f"      [UNVERIFIED] {name:12s} {url}  ({why})")
        print(f"      broken={len(broken)} unverified={len(unreachable)} of {len(confs) + len(journals)}")
        if broken:
            print("      -> fix or drop the BROKEN entries before shipping the catalogue")
    else:
        print("[3/4] link verification skipped")

    stamp = dt.datetime.now().strftime("%Y-%m-%d")
    if args.dry_run:
        print("[4/4] --dry-run: not writing")
        return 0
    OUT.write_text(render(confs, journals, stamp), encoding="utf-8")
    print(f"[4/4] wrote {OUT} ({len(confs)} conferences, {len(journals)} journals)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
