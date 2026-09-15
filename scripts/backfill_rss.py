"""Emergency backfill: pull a day's arXiv updates from the **RSS feeds** instead of the API.

Why this exists
---------------
``export.arxiv.org/api/query`` returns ``HTTP 429 Rate exceeded`` when our
egress IP is throttled, which makes the normal ``fetch`` pipeline lose that
day's window entirely. The per-category RSS feeds (``export.arxiv.org/rss/<cat>``)
are served independently of that quota and carry the same content:

    title / link / description(arXiv:<id>v<n> Announce Type: new, Abstract: ...)
    / guid / category / dc:creator / pubDate

They lack nothing that the digest needs: author list, abstract, version and
primary category are all recoverable, so the records written here are
field-for-field compatible with ``glean.core.fetch_category``.

This is a *fallback channel*, not part of the main pipeline: run it only when
the API is throttled, and it writes into the day you name with ``--date``.
"""

from __future__ import annotations

import argparse
import email.utils
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from glean.config import CATEGORIES, DEFAULT_CAP  # noqa: E402
from glean.core import annotate_hits, day_section, save_day_data, upsert_digest  # noqa: E402
from glean.report import render_day  # noqa: E402

## Filtering: why ``replace`` entries are dropped by default
##
## An RSS batch is one announcement day and carries four announce types:
## ``new`` (fresh paper), ``cross`` (cross-listed into this category),
## ``replace`` (a new *version* of an old paper) and ``replace-cross``.
## The digest is a recommendation surface, so revisions of already-seen papers
## are noise there; keep everything with ``--announce all`` if you ever want the
## raw batch instead.
DEFAULT_ANNOUNCE = ("new", "cross")

RSS_URL = "http://export.arxiv.org/rss/{cat}/"
UA = "paper-glean/0.1 (RSS backfill; +https://github.com/0xaiio/paper-glean)"
NS = {"dc": "http://purl.org/dc/elements/1.1/", "arxiv": "http://arxiv.org/schemas/atom"}
REQUEST_INTERVAL = 3.0  # arXiv asks for >=3s between requests


def http_get(url: str, timeout: float = 30.0) -> bytes:
    """GET with no proxy (loopback-style failures) and arXiv's requested UA."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(req, timeout=timeout) as resp:
        return resp.read()


def _text(node: ET.Element | None, path: str, default: str = "") -> str:
    if node is None:
        return default
    found = node.find(path, NS)
    return (found.text or default).strip() if found is not None else default


def parse_feed(xml_bytes: bytes, fallback_cat: str, keep: tuple[str, ...]) -> list[dict[str, str]]:
    """Turn one RSS feed into paper dicts shaped like ``fetch_category`` output."""
    root = ET.fromstring(xml_bytes)
    out: list[dict[str, str]] = []
    for item in root.findall(".//item"):
        announce = _text(item, "arxiv:announce_type", "new")
        if "all" not in keep and announce not in keep:
            continue
        guid = _text(item, "guid")
        m = re.search(r":(\d{4}\.\d{4,5})(v\d+)?$", guid)
        link = _text(item, "link")
        if not m:  # fall back to the abs link
            m = re.search(r"abs/(\d{4}\.\d{4,5})(v\d+)?", link)
        if not m:
            continue
        pid, version = m.group(1), (m.group(2) or "v1")

        desc = _text(item, "description")
        parts = re.split(r"\bAbstract:\s*", desc, maxsplit=1)
        abstract = re.sub(r"\s+", " ", parts[1] if len(parts) > 1 else desc).strip()

        creators = _text(item, "dc:creator")
        authors = [a.strip() for a in creators.split(",") if a.strip()]

        categories = [c.text.strip() for c in item.findall("category") if c.text]
        if not categories:
            categories = [fallback_cat]

        published = ""
        raw_date = _text(item, "pubDate")
        if raw_date:
            try:
                published = email.utils.parsedate_to_datetime(raw_date).isoformat()
            except (TypeError, ValueError):
                published = raw_date

        out.append(
            {
                "id": pid,
                "version": version,
                "announce": announce,
                "title": re.sub(r"\s+", " ", _text(item, "title")).strip(),
                "authors": authors,
                "abstract": abstract,
                "primary": categories[0],
                "categories": categories,
                "published": published,
                "abs_url": f"https://arxiv.org/abs/{pid}",
                "pdf_url": f"https://arxiv.org/pdf/{pid}",
            }
        )
    return out


def run(day: str, hours: int | None, cap: int, keep: tuple[str, ...]) -> tuple[int, str]:
    # An RSS batch is粒度=天 (every item shares one pubDate), so the honest
    # window is the UTC day when ``--hours`` is not given explicitly.
    if hours is None:
        start = datetime.strptime(day, "%Y%m%d").replace(tzinfo=timezone.utc)
        end = start + timedelta(days=1)
    else:
        end = datetime.now(timezone.utc)
        start = end - timedelta(hours=hours)

    seen: set[str] = set()
    papers: list[dict[str, str]] = []
    for i, cat in enumerate(CATEGORIES):
        if i:
            time.sleep(REQUEST_INTERVAL)
        try:
            batch = parse_feed(http_get(RSS_URL.format(cat=cat)), cat, keep)
        except Exception as exc:  # fail-soft per category
            print(f"[WARN] rss {cat} failed: {exc}", file=sys.stderr)
            continue
        added = 0
        for p in batch:
            if p["id"] in seen:
                continue
            seen.add(p["id"])
            papers.append(p)
            added += 1
        print(f"[INFO] {cat}: +{added} (total unique {len(papers)})")

    annotate_hits(papers)
    data_file = save_day_data(day, papers, start, end)
    upsert_digest(day, day_section(day, papers, start, end, cap))
    return len(papers), str(data_file)


def main() -> None:
    ap = argparse.ArgumentParser(description="Backfill a day's arXiv papers via RSS")
    ap.add_argument("--date", default=None, help="digest section / data file key, YYYYMMDD")
    ap.add_argument(
        "--hours",
        type=int,
        default=None,
        help="window written to the day's metadata; omit to use the UTC day itself",
    )
    ap.add_argument("--cap", type=int, default=DEFAULT_CAP, help="max papers rendered per category")
    ap.add_argument(
        "--announce",
        default=",".join(DEFAULT_ANNOUNCE),
        help="announce types to keep, comma-separated; use 'all' for the raw batch",
    )
    args = ap.parse_args()

    keep = tuple(t.strip() for t in args.announce.split(",") if t.strip())
    day = args.date or datetime.now().strftime("%Y%m%d")
    n, path = run(day, args.hours, args.cap, keep)
    print(f"[OK] {n} papers -> arXiv-schedule.md section {day}; data -> {path}")

    # 与主流水线一致：顺带产出可直接在浏览器打开的静态快照。
    try:
        html_file = render_day(day)
    except Exception as exc:
        print(f"[WARN] html 导出失败: {exc}", file=sys.stderr)
        html_file = None
    if html_file:
        print(f"[OK] html snapshot -> {html_file}")


if __name__ == "__main__":
    main()
