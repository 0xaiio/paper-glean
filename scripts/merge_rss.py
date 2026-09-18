"""Merge a day's arXiv **RSS batch** into an existing (partial) API fetch.

Why this exists
---------------
``daily``/``fetch`` talk to ``export.arxiv.org/api/query``, which is throttled
per egress IP. Three distinct failure shapes have been observed in production:

* all nine categories return ``429`` -> 0 papers for the day;
* a *subset* of categories fail (``502``/timeout, or silently 0) while the rest
  succeed -> a digest that looks fine until you check the primary-category
  distribution (``cs.DB == 0`` is the telltale);
* all nine return 200 but the window is an early slice of the announcement day,
  so ``published`` is entirely ``D-1`` and coverage is a third of the real batch.

``scripts/backfill_rss.py`` fixes the first case but is a **whole-day replace**:
``save_day_data(day, papers, ...)`` overwrites whatever the API already got, so
using it to top up one category throws away the good part. This script is the
complement: it is **id-additive** — existing records are never dropped, RSS items
are only inserted for ids that are not already present.

Usage
-----
    python -X utf8 scripts/merge_rss.py --date 20260918
    python -X utf8 scripts/merge_rss.py            # defaults to today

``--cap`` defaults to a very large number on purpose: ``day_section`` renders
only ``papers[:cap]`` sorted by score, and the papers an agent recommends by
hand usually have ``score == 0`` — with the default cap of 100 they get no
``<a id>`` anchor and ``reanchor`` cannot link to them.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from glean.config import CATEGORIES  # noqa: E402
from glean.core import annotate_hits, day_section, save_day_data, upsert_digest  # noqa: E402
from glean.report import render_day  # noqa: E402
import backfill_rss as br  # noqa: E402

# Anchors for hand-written recommendations must all exist -> render everything.
DEFAULT_CAP = 1_000_000


def merge(day: str, cap: int, keep: tuple[str, ...]) -> tuple[int, int]:
    data_file = ROOT / "data" / f"{day}.json"
    existing = json.loads(data_file.read_text(encoding="utf-8"))["papers"]
    by_id = {p["id"]: p for p in existing}
    base = len(by_id)
    print(f"[INFO] existing in data/{day}.json: {base}")

    for i, cat in enumerate(CATEGORIES):
        if i:
            time.sleep(br.REQUEST_INTERVAL)
        try:
            batch = br.parse_feed(br.http_get(br.RSS_URL.format(cat=cat)), cat, keep)
        except Exception as exc:  # fail-soft per category
            print(f"[WARN] rss {cat} failed: {exc}", file=sys.stderr)
            continue
        added = 0
        for p in batch:
            if p["id"] in by_id:
                continue
            by_id[p["id"]] = p
            added += 1
        print(f"[INFO] {cat}: rss={len(batch)} new=+{added} (unique {len(by_id)})")

    papers = list(by_id.values())
    annotate_hits(papers)
    start = datetime.strptime(day, "%Y%m%d").replace(tzinfo=timezone.utc)
    end = start + timedelta(days=1)
    save_day_data(day, papers, start, end)
    upsert_digest(day, day_section(day, papers, start, end, cap))
    return base, len(papers)


def main() -> None:
    ap = argparse.ArgumentParser(description="Merge an arXiv RSS day-batch into an existing fetch")
    ap.add_argument("--date", default=None, help="digest section / data file key, YYYYMMDD")
    ap.add_argument("--cap", type=int, default=DEFAULT_CAP, help="max papers rendered per category")
    ap.add_argument(
        "--announce",
        default=",".join(br.DEFAULT_ANNOUNCE),
        help="announce types to keep; use 'all' for the raw batch including replacements",
    )
    args = ap.parse_args()

    keep = tuple(t.strip() for t in args.announce.split(",") if t.strip())
    day = args.date or datetime.now().strftime("%Y%m%d")
    base, total = merge(day, args.cap, keep)
    print(f"[OK] {total} papers for {day} (+{total - base} from RSS); data -> data/{day}.json")

    try:
        html_file = render_day(day)
    except Exception as exc:
        print(f"[WARN] html 导出失败: {exc}", file=sys.stderr)
        html_file = None
    if html_file:
        print(f"[OK] html snapshot -> {html_file}")


if __name__ == "__main__":
    main()
