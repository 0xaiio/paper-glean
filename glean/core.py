"""Core library functions for paper-glean.

This module contains all pure business logic extracted from arxiv_daily.py.
Both CLI and web applications should use these functions for data operations
to ensure consistent behavior.
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from glean.config import (
    API,
    ARXIV_NS,
    ARXIV_DIR,
    ATOM,
    CATEGORIES,
    DATA_DIR,
    DEFAULT_CAP,
    DIGEST_MD,
    FEEDBACK_LOG,
    HEADER,
    INTERESTS_MD,
    UA,
)


# ------------------------------------------------------------------
# HTTP / XML utilities
# ------------------------------------------------------------------

def http_get(url: str, timeout: int = 60) -> bytes:
    """Perform an HTTP GET request and return response body."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def parse_xml(data: bytes) -> ET.Element:
    """Parse Atom XML; reject DTD/ENTITY declarations to prevent injection."""
    head = data[:2048].lstrip()
    if b"<!DOCTYPE" in head or b"<!ENTITY" in head:
        raise ValueError("refusing to parse XML containing DTD/ENTITY declarations")
    return ET.fromstring(data)


# ------------------------------------------------------------------
# Fetching
# ------------------------------------------------------------------

def fetch_category(
    cat: str, start_utc: datetime, end_utc: datetime, max_results: int = 500
) -> list[dict[str, Any]]:
    """Fetch papers for a single arXiv category within a time window."""
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
        raw_id = e.findtext(ATOM + "id", "")
        m = re.search(r"abs/([^v]+)(v\d+)?$", raw_id)
        if not m:
            continue
        short_id, ver = m.group(1), (m.group(2) or "v1")
        prim = e.find(ARXIV_NS + "primary_category")
        entries.append(
            {
                "id": short_id,
                "version": ver,
                "title": re.sub(r"\s+", " ", e.findtext(ATOM + "title", "")).strip(),
                "authors": [
                    a.findtext(ATOM + "name", "").strip()
                    for a in e.findall(ATOM + "author")
                ],
                "abstract": re.sub(r"\s+", " ", e.findtext(ATOM + "summary", "")).strip(),
                "primary": prim.get("term") if prim is not None else cat,
                "categories": [c.get("term") for c in e.findall(ATOM + "category")],
                "published": e.findtext(ATOM + "published", ""),
                "abs_url": f"https://arxiv.org/abs/{short_id}",
                "pdf_url": f"https://arxiv.org/pdf/{short_id}",
            }
        )
    return entries


def fetch_all(hours: int) -> tuple[list[dict[str, Any]], datetime, datetime]:
    """Fetch papers from all categories for the past N hours."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    seen: dict[str, bool] = {}
    papers: list[dict[str, Any]] = []
    for cat in CATEGORIES:
        try:
            batch = fetch_category(cat, start, end)
        except Exception as ex:
            print(f"[WARN] fetch {cat} failed: {ex}", file=sys.stderr)
            batch = []
        for p in batch:
            if p["id"] in seen:
                continue
            seen[p["id"]] = True
            papers.append(p)
        print(f"[INFO] {cat}: +{len(batch)} (total unique {len(papers)})")
        time.sleep(3)
    return papers, start, end


# ------------------------------------------------------------------
# Interest profile
# ------------------------------------------------------------------

def load_interest_entries() -> list[dict[str, Any]]:
    """Parse interests.md and return list of interest entries."""
    entries: list[dict[str, Any]] = []
    if not INTERESTS_MD.exists():
        return entries
    section: str | None = None
    cur: dict[str, Any] | None = None
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


def load_interest_keywords() -> tuple[list[str], list[str]]:
    """Return (star_keywords, expand_keywords)."""
    star: list[str] = []
    expand: list[str] = []
    for e in load_interest_entries():
        (star if e["section"] == "star" else expand).extend(e["keywords"])
    return star, expand


# ------------------------------------------------------------------
# Keyword matching
# ------------------------------------------------------------------

def match_keywords(paper: dict[str, Any], keywords: list[str]) -> list[str]:
    """Match keywords against paper title+abstract (whole word, case-insensitive)."""
    text = paper["title"] + " " + paper["abstract"]
    hits: list[str] = []
    for k in keywords:
        if re.search(
            r"(?<![A-Za-z0-9])" + re.escape(k) + r"(?:e?s)?(?![A-Za-z0-9])",
            text,
            re.I,
        ):
            hits.append(k)
    return hits


def annotate_hits(papers: list[dict[str, Any]]) -> bool:
    """Add hits_star/hits_expand and score_star/score_expand to each paper."""
    entries = load_interest_entries()
    for p in papers:
        p["hits_star"], p["hits_expand"] = [], []
        p["score_star"] = p["score_expand"] = 0
        for e in entries:
            hit = match_keywords(p, e["keywords"])
            if hit:
                key = e["section"]
                p["hits_" + key].extend(k for k in hit if k not in p["hits_" + key])
                p["score_" + key] += e["weight"]
    return bool(entries)


# ------------------------------------------------------------------
# Markdown generation
# ------------------------------------------------------------------

def excerpt(text: str, limit: int = 400) -> str:
    """Return first two sentences, truncated to limit chars."""
    parts = re.split(r"(?<=[.!?]) +", text)
    out = " ".join(parts[:2])
    if len(out) > limit:
        out = out[:limit].rsplit(" ", 1)[0] + " …"
    return out


def day_section(day: str, papers: list[dict[str, Any]], start: datetime, end: datetime, cap: int) -> str:
    """Generate markdown section for a single day's digest."""
    by_cat: dict[str, list[dict[str, Any]]] = {}
    for p in papers:
        key = (
            p["primary"]
            if p["primary"] in CATEGORIES
            else next((c for c in p["categories"] if c in CATEGORIES), p["primary"])
        )
        by_cat.setdefault(key, []).append(p)

    n_star = sum(1 for p in papers if p.get("hits_star"))
    n_expand = sum(1 for p in papers if p.get("hits_expand"))
    hit_s = (
        f" | 🎯 关键词命中(interests.md): ★ {n_star} 篇 / 🧐 {n_expand} 篇"
        if (n_star or n_expand)
        else ""
    )
    lines = [
        f"<!-- BEGIN {day} -->",
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
        "",
    ]
    for cat in CATEGORIES + sorted(set(by_cat) - set(CATEGORIES)):
        ps = by_cat.get(cat)
        if not ps:
            continue
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
            lines.append(
                f"- <a id=\"{day}-{p['id']}\"></a>"
                f"**{p['title']}** — [{p['id']}]({p['abs_url']}){cross_s}{hit_s}  "
            )
            lines.append(f"  {authors}  ")
            lines.append(f"  {excerpt(p['abstract'])}")
        if len(ps) > cap:
            lines.append(f"- _…另有 {len(ps) - cap} 篇, 见 `data/{day}.json`_")
        lines.append("")
    lines.append(f"<!-- END {day} -->")
    return "\n".join(lines) + "\n"


def _rec_blocks(sec: str) -> dict[str, str]:
    """Extract 📌 and 🧐 recommendation subsections."""
    out: dict[str, str] = {}
    for h in ("### 📌", "### 🧐"):
        i = sec.find(h)
        if i == -1:
            continue
        j = sec.find("\n### ", i)
        out[h] = sec[i : (j + 1) if j != -1 else len(sec)]
    return out


def upsert_digest(day: str, section: str) -> None:
    """Insert or replace a day's section in arXiv-schedule.md."""
    if DIGEST_MD.exists():
        content = DIGEST_MD.read_text(encoding="utf-8")
    else:
        content = HEADER
    begin, endm = f"<!-- BEGIN {day} -->", f"<!-- END {day} -->"
    if begin in content and endm in content:
        pre = content[: content.index(begin)]
        old = content[content.index(begin) : content.index(endm)]
        post = content[content.index(endm) + len(endm) :].lstrip("\n")
        new_blocks = _rec_blocks(section)
        for h, old_block in _rec_blocks(old).items():
            if "_待 agent 分析填写_" not in old_block and h in new_blocks:
                section = section.replace(new_blocks[h], old_block)
        content = pre + section + "\n" + post
    else:
        if "<!-- BEGIN " in content:
            idx = content.index("<!-- BEGIN ")
            content = content[:idx] + section + "\n" + content[idx:]
        else:
            content = content.rstrip("\n") + "\n\n" + section
    DIGEST_MD.write_text(content, encoding="utf-8")


# ------------------------------------------------------------------
# Feedback
# ------------------------------------------------------------------

def find_paper(pid: str) -> tuple[dict[str, Any] | None, str | None]:
    """Find a paper by id in data/*.json (newest first)."""
    for f in sorted(DATA_DIR.glob("*.json"), reverse=True):
        data = json.loads(f.read_text(encoding="utf-8"))
        for p in data.get("papers", []):
            if p["id"] == pid:
                return p, data.get("day", f.stem)
    return None, None


def set_entry_weights(new_weights: dict[str, int]) -> None:
    """Update weights in interests.md."""
    lines = INTERESTS_MD.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        s = lines[i].strip()
        out.append(lines[i])
        if s.startswith("### ") and s[4:].strip() in new_weights:
            w = new_weights[s[4:].strip()]
            j = i + 1
            block: list[str] = []
            while j < n and not lines[j].strip().startswith(("### ", "## ")):
                if not lines[j].strip().lower().startswith("- weight:"):
                    block.append(lines[j])
                j += 1
            k = next(
                (x for x, b in enumerate(block) if b.strip().lower().startswith("- keywords:")),
                -1,
            )
            block.insert(k + 1, f"- weight: {w}")
            out.extend(block)
            i = j
        else:
            i += 1
    INTERESTS_MD.write_text("\n".join(out) + "\n", encoding="utf-8")


def patch_rating(pid: str, symbol: str, n: int) -> bool:
    """Patch the rating in arXiv-schedule.md digest tables."""
    if not DIGEST_MD.exists():
        return False
    content = DIGEST_MD.read_text(encoding="utf-8")
    pat = re.compile(
        r"^(\|\s*)(" + symbol + r"+)(\s*\|.*\[" + re.escape(pid) + r"\].*)$",
        re.M,
    )
    new_content, cnt = pat.subn(lambda m: m.group(1) + symbol * n + m.group(3), content)
    if cnt:
        DIGEST_MD.write_text(new_content, encoding="utf-8")
    return bool(cnt)


def apply_feedback(
    paper: dict[str, Any],
    day: str,
    stars: int | None = None,
    curiosity: int | None = None,
) -> dict[str, Any]:
    """Apply feedback to a paper and return the feedback record.

    This is the shared core function used by both CLI and web.
    It updates interests.md weights, patches digest tables, and appends to feedback.jsonl.
    """
    entries = load_interest_entries()
    changed: dict[str, int] = {}
    adjustments: list[dict[str, Any]] = []

    for kind, rating, symbol, label in (
        ("star", stars, "★", "兴趣点"),
        ("expand", curiosity, "🧐", "扩展点"),
    ):
        if rating is None:
            continue
        rating = max(0, min(5, rating))
        delta = 1 if rating >= 4 else (-1 if rating <= 2 else 0)
        matched = [
            e for e in entries if e["section"] == kind and match_keywords(paper, e["keywords"])
        ]
        for e in matched:
            if delta:
                changed[e["title"]] = max(1, min(10, e["weight"] + delta))
        patched = patch_rating(paper["id"], symbol, rating) if rating > 0 else False
        adjustments.append(
            {
                "kind": kind,
                "rating": rating,
                "delta": delta,
                "matched_entries": [e["title"] for e in matched],
                "digest_updated": patched,
            }
        )

    if changed:
        set_entry_weights(changed)

    record = {
        "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "id": paper["id"],
        "day": day,
        "title": paper["title"],
        "primary": paper["primary"],
        "abstract_head": excerpt(paper["abstract"], 200),
        "adjustments": adjustments,
        "weight_updates": changed,
    }

    with FEEDBACK_LOG.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(record, ensure_ascii=False) + "\n")

    return record


# ------------------------------------------------------------------
# Reanchor
# ------------------------------------------------------------------

def reanchor_day(day: str | None = None) -> tuple[int, int]:
    """Add anchors and jump links for a day's section. Returns (n_anchor, n_link)."""
    day = day or datetime.now().strftime("%Y%m%d")
    if not DIGEST_MD.exists():
        return 0, 0
    content = DIGEST_MD.read_text(encoding="utf-8")
    begin, endm = f"<!-- BEGIN {day} -->", f"<!-- END {day} -->"
    if begin not in content or endm not in content:
        return 0, 0
    i, j = content.index(begin), content.index(endm) + len(endm)
    out: list[str] = []
    n_anchor, n_link = 0, 0
    for line in content[i:j].splitlines():
        if line.startswith("- **") and "<a id=" not in line:
            m = re.search(r"\[([\d.]+)\]\(https://arxiv\.org/abs/", line)
            if m:
                line = line.replace("- **", f'- <a id="{day}-{m.group(1)}"></a>**', 1)
                n_anchor += 1
        elif (
            line.startswith("|")
            and ("★" in line or "🧐" in line)
            and f"](#{day}-" not in line
        ):
            m = re.search(r"\[([\d.]+)\]\(https://arxiv\.org/abs/[\d.]+\)", line)
            if m:
                line = line.replace(
                    m.group(0), m.group(0) + f" · [📄](#{day}-{m.group(1)})", 1
                )
                n_link += 1
        out.append(line)
    DIGEST_MD.write_text(content[:i] + "\n".join(out) + content[j:], encoding="utf-8")
    return n_anchor, n_link


# ------------------------------------------------------------------
# Download
# ------------------------------------------------------------------

def sanitize_title(title: str) -> str:
    """Sanitize paper title for filesystem naming."""
    t = title.replace("\u2013", "-").replace("\u2014", "-")
    t = re.sub(r"\\mathbb\s*\{?([A-Za-z])\}?", r"\1", t)
    t = t.replace("\\varepsilon", "epsilon").replace("\\epsilon", "epsilon")
    t = re.sub(r"[:?,.\"'!;`\u2019\u201c\u201d()\[\]{}<>/\\|*$]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def download_paper(pid: str) -> Path | None:
    """Download a single paper PDF and return the destination path."""
    url = API + "?" + urllib.parse.urlencode({"id_list": pid, "max_results": 1})
    root = parse_xml(http_get(url))
    e = root.find(ATOM + "entry")
    if e is None or not e.findtext(ATOM + "title"):
        print(f"[ERR] {pid}: not found on arXiv API", file=sys.stderr)
        return None
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
            print(f"[ERR] {pid}: response is not a PDF ({pdf_url})", file=sys.stderr)
            return None
        ARXIV_DIR.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        print(f"[OK] {len(data):>8} bytes  {dest.name}")
        return dest
    except Exception as ex:
        print(f"[ERR] {pid}: {ex}", file=sys.stderr)
        return None


# ------------------------------------------------------------------
# Data persistence
# ------------------------------------------------------------------

def save_day_data(day: str, papers: list[dict[str, Any]], start: datetime, end: datetime) -> Path:
    """Save daily paper data to JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    data_file = DATA_DIR / f"{day}.json"
    data_file.write_text(
        json.dumps(
            {"day": day, "window_utc": [start.isoformat(), end.isoformat()], "papers": papers},
            ensure_ascii=False,
            indent=1,
        ),
        encoding="utf-8",
    )
    return data_file


def load_day_data(day: str) -> dict[str, Any] | None:
    """Load daily paper data from JSON file."""
    data_file = DATA_DIR / f"{day}.json"
    if not data_file.exists():
        return None
    return json.loads(data_file.read_text(encoding="utf-8"))


def list_available_days() -> list[str]:
    """Return list of available day strings (YYYYMMDD) from data directory."""
    if not DATA_DIR.exists():
        return []
    return sorted([f.stem for f in DATA_DIR.glob("*.json")], reverse=True)
