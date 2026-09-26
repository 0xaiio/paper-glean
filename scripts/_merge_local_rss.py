"""Merge locally-downloaded RSS feed files into a day's data (id-additive).

Ad-hoc helper for the case where python's urllib gets HTTP 406 from
export.arxiv.org while curl still gets 200: download the feeds with curl and
merge them here instead of losing the categories.

Usage::

    for c in cs.DB cs.DC cs.FL cs.LO cs.PL; do
      curl --noproxy '*' -sL -o ".rss_$c.xml" "http://export.arxiv.org/rss/$c/"
    done
    python -X utf8 scripts/_merge_local_rss.py --date 20260924
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from backfill_rss import parse_feed  # noqa: E402

from glean.config import CATEGORIES  # noqa: E402
from glean.core import annotate_hits, day_section, load_day_data, save_day_data, upsert_digest  # noqa: E402

CAP = 1000000
KEEP = ("new", "cross")


def main() -> None:
    ap = argparse.ArgumentParser(description="Merge .rss_<cat>.xml files into a day's data")
    ap.add_argument("--date", required=True, help="YYYYMMDD")
    args = ap.parse_args()
    day = args.date

    existing = load_day_data(day)
    papers = list((existing or {}).get("papers") or [])
    print(f"[INFO] existing: {len(papers)}")
    seen = {p["id"] for p in papers}

    for cat in CATEGORIES:
        f = ROOT / f".rss_{cat}.xml"
        if not f.exists():
            continue
        batch = parse_feed(f.read_bytes(), cat, KEEP)
        added = 0
        for p in batch:
            if p["id"] in seen:
                continue
            seen.add(p["id"])
            papers.append(p)
            added += 1
        print(f"[INFO] {cat}: rss={len(batch)} new=+{added} (unique {len(papers)})")

    start = datetime.strptime(day, "%Y%m%d").replace(tzinfo=timezone.utc)
    end = start + timedelta(days=1)
    annotate_hits(papers)
    save_day_data(day, papers, start, end)
    upsert_digest(day, day_section(day, papers, start, end, CAP))
    print(f"[OK] {len(papers)} papers for {day}")


if __name__ == "__main__":
    main()
