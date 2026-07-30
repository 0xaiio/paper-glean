"""CLI commands for paper-glean.

This module contains the command-line interface implementation.
It wraps the core library functions with argparse and console output.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone

from glean.config import DEFAULT_CAP
from glean.core import (
    annotate_hits,
    day_section,
    download_paper,
    fetch_all,
    load_interest_entries,
    reanchor_day,
    save_day_data,
    upsert_digest,
    apply_feedback,
    find_paper,
)


def cmd_fetch(args: argparse.Namespace) -> None:
    """Fetch papers and update digest."""
    day = args.date or datetime.now().strftime("%Y%m%d")
    papers, start, end = fetch_all(args.hours)
    if annotate_hits(papers):
        n = sum(1 for p in papers if p.get("hits_star") or p.get("hits_expand"))
        print(f"[INFO] interests.md keywords: {n}/{len(papers)} papers hit")
    data_file = save_day_data(day, papers, start, end)
    upsert_digest(day, day_section(day, papers, start, end, args.cap))
    print(f"[OK] {len(papers)} papers -> arXiv-schedule.md section {day}; data -> {data_file}")


def cmd_download(args: argparse.Namespace) -> None:
    """Download papers by ID."""
    for pid in args.ids:
        download_paper(pid)


def cmd_feedback(args: argparse.Namespace) -> None:
    """Apply feedback rating to a paper."""
    if args.stars is None and args.curiosity is None:
        print("[ERR] 需要 --stars N 和/或 --curiosity N (0-5)")
        return
    paper, day = find_paper(args.id)
    if paper is None:
        print(f"[ERR] {args.id}: 未在 data/*.json 中找到(请先 fetch)")
        return

    record = apply_feedback(paper, day, stars=args.stars, curiosity=args.curiosity)

    # Print human-readable output
    for adj in record["adjustments"]:
        symbol = "★" if adj["kind"] == "star" else "🧐"
        label = "兴趣点" if adj["kind"] == "star" else "扩展点"
        matched = ", ".join(adj["matched_entries"]) or "无"
        print(
            f"[OK] {symbol}x{adj['rating']}"
            f" | 命中{label}条目: {matched}"
            f" | digest 表格{'已更新' if adj['digest_updated'] else '未找到对应行(跨类调整请交给 agent)'}"
        )
        if not adj["matched_entries"] and adj["delta"] > 0:
            print(
                f"[HINT] 该论文未命中任何{label}条目; 建议让 agent 依据此论文在"
                f" interests.md 新增{label}(参考 feedback.jsonl 中本条记录)"
            )

    if record["weight_updates"]:
        for t, w in record["weight_updates"].items():
            print(f"[OK] interests.md 权重: {t} -> {w}")
    print(f"[OK] 反馈已记录 -> feedback.jsonl")


def cmd_reanchor(args: argparse.Namespace) -> None:
    """Re-anchor a day's section."""
    day = args.date or datetime.now().strftime("%Y%m%d")
    n_anchor, n_link = reanchor_day(day)
    if n_anchor == 0 and n_link == 0:
        print(f"[ERR] digest 中无 {day} 章节")
    else:
        print(f"[OK] {day}: +{n_anchor} 锚点, +{n_link} 跳转链接")


def main() -> None:
    """Main CLI entry point."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description="arXiv daily digest & downloader")
    sub = ap.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fetch", help="抓取过去 N 小时新增论文并更新 digest")
    f.add_argument("--hours", type=int, default=24)
    f.add_argument("--cap", type=int, default=DEFAULT_CAP, help="digest 中每类别最多列出的论文数")
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
