"""CLI commands for paper-glean.

This module contains the command-line interface implementation.
It wraps the core library functions with argparse and console output.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone

from glean import notify
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
from glean.ccf import (
    add_venue,
    load_venues,
    remove_venue,
    run as run_ccf,
    set_enabled as set_venue_enabled,
    set_enabled_area,
    sync_catalog,
)
from glean.serve import DEFAULT_HOST, DEFAULT_PORT, base_url, ensure, log_path
from glean.watch import (
    add_researcher,
    load_events as load_watch_events,
    load_watchlist,
    remove_researcher,
    run as run_watch,
    set_enabled,
)


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


def cmd_watch_add(args: argparse.Namespace) -> None:
    """Add a researcher to watchlist.md."""
    tags = [t.strip() for t in args.tags.split(";") if t.strip()] if args.tags else []
    try:
        entry = add_researcher(args.name, args.homepage, args.dblp, args.s2, tags)
    except ValueError as exc:
        print(f"[ERR] {exc}")
        return
    src = [s for s in ("homepage", "dblp", "s2") if entry.get(s)]
    print(f"[OK] 已添加: {entry['name']} (key={entry['key']}, 源={'/'.join(src) or '仅主页'})")
    print("[NEXT] 运行 `arxiv_daily.py watch run --only <姓名>` 建立基线")


def cmd_watch_remove(args: argparse.Namespace) -> None:
    """Remove a researcher and forget their seen-state."""
    if remove_researcher(args.name):
        print(f"[OK] 已移除: {args.name}")
    else:
        print(f"[ERR] 未找到: {args.name}")


def cmd_watch_toggle(args: argparse.Namespace) -> None:
    """Pause / resume a researcher."""
    if set_enabled(args.name, args.enable):
        print(f"[OK] {'已启用' if args.enable else '已暂停'}: {args.name}")
    else:
        print(f"[ERR] 未找到: {args.name}")


def cmd_watch_list(args: argparse.Namespace) -> None:
    """Show the watchlist."""
    entries = load_watchlist()
    if not entries:
        print("[INFO] 名单为空; 用 `watch add <姓名> --homepage <URL>` 添加")
        return
    for e in entries:
        if not args.all and not e.get("enabled", True):
            continue
        mark = "●" if e.get("enabled", True) else "○"
        src = "/".join(s for s in ("homepage", "dblp", "s2") if e.get(s)) or "无可用源"
        tags = f"  tags={','.join(e['tags'])}" if e.get("tags") else ""
        print(f"{mark} {e['name']}  [{src}]{tags}")


def cmd_watch_run(args: argparse.Namespace) -> None:
    """Scan every enabled researcher and push what is new."""
    res = run_watch(only=args.only, force=args.force, push=not args.no_push)
    for b in res["baselined"]:
        print(f"[BASE] {b} — 已建立基线，本次不推送（加 --force 可强制推送）")
    for name, items in res["grouped"].items():
        print(f"[NEW] {name}: {len(items)} 条新作")
        for it in items:
            kind = {"paper": "论文", "video": "视频", "report": "技术报告",
                    "talk": "报告/演讲", "other": "其它"}.get(it.get("kind"), "其它")
            flag = " ⚠️低置信" if (it.get("confidence") or 1.0) < 0.6 else ""
            print(f"      · [{kind}] {it['title'][:80]}{flag}")
    if not res["grouped"] and not res["baselined"]:
        print("[OK] 没有新作")
    for err in res["errors"]:
        print(f"[WARN] {err}")
    if res["new_items"]:
        print(f"[OK] 共 {len(res['new_items'])} 条新作 -> WATCH-digest.md (run {res['run_id']})")
        print(f"[OK] 推送通道: {', '.join(res['pushed_to']) or '无（仅落盘 digest）'}")


def cmd_watch_ack(args: argparse.Namespace) -> None:
    """Clear the Web UI's NEW badges."""
    print(f"[OK] 已标记 {notify.ack_all()} 条新作为已读")


def cmd_watch_push_test(args: argparse.Namespace) -> None:
    """Report which push channels would fire, and send a probe payload."""
    states = notify.enabled_channels()
    for name, on in states.items():
        print(f"[{'ON ' if on else 'OFF'}] {name}")
    if not states["webhook"]:
        print("[HINT] 设置环境变量 PAPER_GLEAN_WEBHOOK_URL 以启用 webhook")
    if args.send:
        probe = [
            {
                "researcher": "推送自检",
                "title": "paper-glean 推送通道自检",
                "kind": "other",
                "url": "",
                "fingerprint": "probe",
            }
        ]
        done = notify.push(probe)
        print(f"[OK] 自检已发送 -> {', '.join(done) or '无通道'}")
        notify.ack_all()


def cmd_ccf_list(args: argparse.Namespace) -> None:
    """Show the CCF venue list."""
    entries = load_venues()
    if not entries:
        print("[INFO] 名单为空; 先运行 `ccf refresh` 从目录生成")
        return
    for e in entries:
        if not args.all and not e.get("enabled", True):
            continue
        if args.area and args.area.lower() not in (e.get("area") or "").lower():
            continue
        mark = "[x]" if e.get("enabled", True) else "[ ]"
        kind = "期刊" if e.get("kind") == "journal" else "会议"
        print(f"{mark} {e['name']:12s} {kind}  {e.get('area', '')}")
    on = sum(1 for e in entries if e.get("enabled", True))
    print(f"[INFO] 共 {len(entries)} 个条目，其中 {on} 个已勾选")


def cmd_ccf_toggle(args: argparse.Namespace) -> None:
    """Tick / untick venues — by name, or in bulk by area."""
    if args.area:
        touched = set_enabled_area(args.area, args.enable)
        if not touched:
            print(f"[ERR] 没有匹配领域「{args.area}」的条目")
            return
        verb = "已勾选" if args.enable else "已取消勾选"
        print(f"[OK] {verb} {len(touched)} 个条目: {', '.join(sorted(touched))}")
        return
    if set_venue_enabled(args.name, args.enable):
        print(f"[OK] {'已勾选' if args.enable else '已取消勾选'}: {args.name}")
    else:
        print(f"[ERR] 未找到: {args.name}")


def cmd_ccf_add(args: argparse.Namespace) -> None:
    """Add a venue that the built-in catalogue does not cover."""
    try:
        entry = add_venue(
            args.name,
            kind="journal" if args.journal else "conference",
            full=args.full or "",
            area=args.area or "",
            homepage=args.homepage,
            dblp=args.dblp or "",
            ccf=args.ccf,
            issn=args.issn or "",
        )
    except ValueError as exc:
        print(f"[ERR] {exc}")
        return
    print(f"[OK] 已添加: {entry['name']} (key={entry['key']}, {'期刊' if args.journal else '会议'})")


def cmd_ccf_remove(args: argparse.Namespace) -> None:
    """Remove a venue and forget its seen-state."""
    print(f"[OK] 已移除: {args.name}" if remove_venue(args.name) else f"[ERR] 未找到: {args.name}")


def cmd_ccf_run(args: argparse.Namespace) -> None:
    """Scan every ticked venue and push what is new."""
    res = run_ccf(only=args.only, force=args.force, push=not args.no_push)
    for b in res["baselined"]:
        print(f"[BASE] {b} — 已建立基线，本次不推送（加 --force 可强制推送）")
    for name, items in res["grouped"].items():
        print(f"[NEW] {name}: {len(items)} 条更新")
        for it in items:
            label = {"cfp": "CFP", "program": "Program", "papers": "接收论文",
                     "other": "其它"}.get(it.get("kind"), "其它")
            flag = " ⚠️低置信" if (it.get("confidence") or 1.0) < 0.6 else ""
            extra = f"  截稿 {it['deadline']}" if it.get("deadline") else ""
            print(f"      · [{label}] {it['title'][:80]}{extra}{flag}")
    if not res["grouped"] and not res["baselined"]:
        print("[OK] 没有更新")
    for err in res["errors"]:
        print(f"[WARN] {err}")
    if res["new_items"]:
        print(f"[OK] 共 {len(res['new_items'])} 条更新 -> CCF-digest.md (run {res['run_id']})")
        print(f"[OK] 推送通道: {', '.join(res['pushed_to']) or '无（仅落盘 digest）'}")


def cmd_ccf_ack(args: argparse.Namespace) -> None:
    """Clear the Web UI's CCF NEW badges."""
    print(f"[OK] 已标记 {notify.ack_all('ccf')} 条更新为已读")


def cmd_ccf_refresh(args: argparse.Namespace) -> None:
    """Re-merge the built-in catalogue into ccf.md (keeps your ticks)."""
    added, updated = sync_catalog(default_enabled=not args.new_disabled)
    print(f"[OK] 目录同步: 新增 {added} 个条目，更新 {updated} 个字段")
    print("[NEXT] 运行 `ccf list` 查看，用 `ccf disable --area <领域>` 批量取消勾选")


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

    w = sub.add_parser("watch", help="学者监控与推送(名单见 watchlist.md)")
    wsub = w.add_subparsers(dest="watch_cmd", required=True)

    wa = wsub.add_parser("add", help="添加监控对象")
    wa.add_argument("name", help="姓名，建议「中文名 英文名」")
    wa.add_argument("--homepage", help="个人主页 URL(首选解析源)")
    wa.add_argument("--dblp", help="DBLP PID(pid/xx/yyyy) 或作者全名(兜底)")
    wa.add_argument("--s2", help="Semantic Scholar author id(兜底)")
    wa.add_argument("--tags", help="标签，分号分隔")
    wa.set_defaults(func=cmd_watch_add)

    wr = wsub.add_parser("remove", help="移除监控对象(同时清除其已见状态)")
    wr.add_argument("name")
    wr.set_defaults(func=cmd_watch_remove)

    we = wsub.add_parser("enable", help="启用监控对象")
    we.add_argument("name")
    we.set_defaults(func=cmd_watch_toggle, enable=True)

    wd = wsub.add_parser("disable", help="暂停监控对象(保留条目与历史)")
    wd.add_argument("name")
    wd.set_defaults(func=cmd_watch_toggle, enable=False)

    wl = wsub.add_parser("list", help="列出监控名单")
    wl.add_argument("--all", action="store_true", help="同时显示已暂停的条目")
    wl.set_defaults(func=cmd_watch_list)

    wu = wsub.add_parser("run", help="扫描全部启用对象并推送新作")
    wu.add_argument("--only", help="只扫描指定姓名/key")
    wu.add_argument("--force", action="store_true", help="首次运行也推送(默认只建基线)")
    wu.add_argument("--no-push", action="store_true", help="只落盘 digest，不推送")
    wu.set_defaults(func=cmd_watch_run)

    wk = wsub.add_parser("ack", help="清除 Web 端的 NEW 徽标(标记已读)")
    wk.set_defaults(func=cmd_watch_ack)

    wt = wsub.add_parser("push-test", help="检查推送通道并可选发一条自检")
    wt.add_argument("--send", action="store_true", help="实际发送一条自检消息")
    wt.set_defaults(func=cmd_watch_push_test)

    c = sub.add_parser("ccf", help="CCF-A 会议/期刊监控与推送(名单见 ccf.md)")
    csub = c.add_subparsers(dest="ccf_cmd", required=True)

    cl = csub.add_parser("list", help="列出会议/期刊勾选状态")
    cl.add_argument("--all", action="store_true", help="同时显示未勾选的条目")
    cl.add_argument("--area", help="只显示某领域(支持子串，如 DB / 数据库)")
    cl.set_defaults(func=cmd_ccf_list)

    ce = csub.add_parser("enable", help="勾选(订阅)会议/期刊")
    ce.add_argument("name", nargs="?", help="名称; 与 --area 二选一")
    ce.add_argument("--area", help="批量勾选整个领域")
    ce.set_defaults(func=cmd_ccf_toggle, enable=True)

    cd = csub.add_parser("disable", help="取消勾选(暂停)会议/期刊")
    cd.add_argument("name", nargs="?", help="名称; 与 --area 二选一")
    cd.add_argument("--area", help="批量取消勾选整个领域")
    cd.set_defaults(func=cmd_ccf_toggle, enable=False)

    ca = csub.add_parser("add", help="添加目录未覆盖的会议/期刊")
    ca.add_argument("name")
    ca.add_argument("--homepage", required=True, help="会议/期刊主页(监控的唯一依据)")
    ca.add_argument("--journal", action="store_true", help="声明为期刊(默认是会议)")
    ca.add_argument("--full", help="全称")
    ca.add_argument("--area", help="领域")
    ca.add_argument("--dblp", help="DBLP 索引地址(仅作参考链接)")
    ca.add_argument("--issn", help="ISSN(期刊经 Crossref 监控新卷期时需要)")
    ca.add_argument("--ccf", default="A", help="CCF 等级, 默认 A")
    ca.set_defaults(func=cmd_ccf_add)

    cr = csub.add_parser("remove", help="移除条目(同时清除其已见状态)")
    cr.add_argument("name")
    cr.set_defaults(func=cmd_ccf_remove)

    cu = csub.add_parser("run", help="扫描全部勾选条目并推送新 CFP / Program / 接收论文")
    cu.add_argument("--only", help="只扫描指定名称")
    cu.add_argument("--force", action="store_true", help="首次运行也推送(默认只建基线)")
    cu.add_argument("--no-push", action="store_true", help="只落盘 digest，不推送")
    cu.set_defaults(func=cmd_ccf_run)

    ck = csub.add_parser("ack", help="清除 Web 端 CCF 的 NEW 徽标")
    ck.set_defaults(func=cmd_ccf_ack)

    cf = csub.add_parser("refresh", help="把内置 CCF-A 目录并入 ccf.md(保留你的勾选)")
    cf.add_argument("--new-disabled", action="store_true", help="新增条目默认不勾选")
    cf.set_defaults(func=cmd_ccf_refresh)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
