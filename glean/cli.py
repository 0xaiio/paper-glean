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
from glean.serve import DEFAULT_HOST, DEFAULT_PORT, base_url, ensure, log_path


def _run_fetch(hours: int, cap: int, date: str | None) -> tuple[str, int, str]:
    """Fetch a time window and update both the JSON data file and the digest.

    Returns ``(day, paper_count, data_file)``. Shared by ``fetch`` and ``daily``
    so the two entry points can never drift apart.
    """
    day = date or datetime.now().strftime("%Y%m%d")
    papers, start, end = fetch_all(hours)
    if annotate_hits(papers):
        n = sum(1 for p in papers if p.get("hits_star") or p.get("hits_expand"))
        print(f"[INFO] interests.md keywords: {n}/{len(papers)} papers hit")
    data_file = save_day_data(day, papers, start, end)
    upsert_digest(day, day_section(day, papers, start, end, cap))
    return day, len(papers), str(data_file)


def cmd_fetch(args: argparse.Namespace) -> None:
    """Fetch papers and update digest."""
    day, n, data_file = _run_fetch(args.hours, args.cap, args.date)
    print(f"[OK] {n} papers -> arXiv-schedule.md section {day}; data -> {data_file}")


def cmd_daily(args: argparse.Namespace) -> None:
    """One-command daily pipeline: fetch -> digest -> optionally serve.

    This is the entry point used by the scheduled task. It is deliberately
    fail-soft: the digest is already written when the web app is brought up, so
    a failure to serve degrades to a warning instead of a non-zero exit.
    """
    day, n, data_file = _run_fetch(args.hours, args.cap, args.date)
    print(f"[OK] {n} papers -> arXiv-schedule.md section {day}; data -> {data_file}")
    print("[NEXT] agent 填写 ★/🧐 推荐小节（见 docs/user-guide/scheduling.md）")

    if not args.serve:
        print("[HINT] 需要顺带拉起本地 Web 服务请加 --serve")
        return

    online, started = ensure(args.host, args.port)
    url = base_url(args.host, args.port)
    if online:
        print(f"[OK] web app {'started' if started else 'already online'} -> {url}")
    else:
        print(f"[WARN] web app 未在 {args.host}:{args.port} 上线; 日志: {log_path(args.host, args.port)}")
        print("[WARN] digest 与 data/*.json 已生成，可直接阅读 arXiv-schedule.md")


def cmd_serve(args: argparse.Namespace) -> None:
    """Start the web app in the foreground (manual / development use)."""
    try:
        import uvicorn
    except ModuleNotFoundError:  # pragma: no cover - depends on optional extra
        print('[ERR] 缺少 Web 依赖; 请先安装: pip install -e ".[web]"')
        return

    if args.reload:
        uvicorn.run("glean.web.__main__:app", host=args.host, port=args.port, reload=True)
    else:
        from glean.web.main import create_app

        uvicorn.run(create_app(), host=args.host, port=args.port)


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

    dl = sub.add_parser("daily", help="每日流水线: fetch -> digest -> (可选)确保本地 Web 服务在线")
    dl.add_argument("--hours", type=int, default=24, help="抓取时间窗口(小时), 默认 24")
    dl.add_argument("--cap", type=int, default=DEFAULT_CAP, help="digest 中每类别最多列出的论文数")
    dl.add_argument("--date", help="覆盖章节日期 YYYYMMDD(默认今天)")
    dl.add_argument("--serve", action="store_true", help="结束后确保本地 Web 服务在线(不在线则后台拉起)")
    dl.add_argument("--host", default=DEFAULT_HOST, help=f"Web 服务地址, 默认 {DEFAULT_HOST}")
    dl.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Web 服务端口, 默认 {DEFAULT_PORT}")
    dl.set_defaults(func=cmd_daily)

    sv = sub.add_parser("serve", help="启动本地 Web 应用(前台)")
    sv.add_argument("--host", default=DEFAULT_HOST, help=f"默认 {DEFAULT_HOST}")
    sv.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"默认 {DEFAULT_PORT}")
    sv.add_argument("--reload", action="store_true", help="开发模式: 代码变更自动重载")
    sv.set_defaults(func=cmd_serve)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
