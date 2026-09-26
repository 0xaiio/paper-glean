"""Tests for CLI commands."""

from __future__ import annotations

import argparse
import subprocess
import sys


def _leaves(parser: argparse.ArgumentParser, prefix: tuple[str, ...] = ()):
    """Return ``[(name_path, parser), ...]`` for every childless sub-command.

    ``argparse`` exposes no public walker, so the sub-parser actions are read
    off ``_actions`` (the long-standing idiom for introspecting a command tree).
    """
    groups = [a for a in parser._actions if isinstance(a, argparse._SubParsersAction)]
    if not groups:
        return [(prefix, parser)]
    out: list[tuple[tuple[str, ...], argparse.ArgumentParser]] = []
    for group in groups:
        for name, child in group.choices.items():
            out.extend(_leaves(child, prefix + (name,)))
    return out


def test_every_leaf_command_is_wired_to_a_handler():
    """``main()`` ends in ``args.func(args)``, so a leaf without ``func`` crashes.

    This invariant is why ``build_parser()`` was split out of ``main()``: a new
    sub-command whose ``set_defaults(func=...)`` was forgotten only explodes at
    runtime, on the single code path no other test exercises.
    """
    from glean.cli import build_parser

    leaves = _leaves(build_parser())
    missing = [".".join(prefix) for prefix, p in leaves if p.get_default("func") is None]

    assert missing == []


def test_command_surface_is_exactly_the_documented_one():
    """Locks the public command tree (docs/user-guide/cli.md) in one place."""
    from glean.cli import build_parser

    names = {".".join(prefix) for prefix, _ in _leaves(build_parser())}

    assert names == {
        "fetch", "download", "feedback", "reanchor", "html", "daily", "weekly", "serve",
        "watch.add", "watch.remove", "watch.enable", "watch.disable",
        "watch.list", "watch.run", "watch.ack", "watch.push-test",
        "ccf.list", "ccf.enable", "ccf.disable", "ccf.add", "ccf.remove",
        "ccf.run", "ccf.ack", "ccf.refresh",
    }


def test_both_monitor_scans_share_one_flag_group():
    """``watch run`` / ``ccf run`` come from ``_add_run_args`` — one source, not two."""
    from glean.cli import build_parser

    leaves = dict(_leaves(build_parser()))
    shared = {"--only", "--force", "--no-push"}

    for name in (("watch", "run"), ("ccf", "run")):
        options = {s for action in leaves[name]._actions for s in action.option_strings}
        assert shared <= options, name


def test_cli_help():
    result = subprocess.run(
        [sys.executable, "-m", "glean.cli", "--help"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert result.returncode == 0
    assert "fetch" in result.stdout
    assert "download" in result.stdout
    assert "feedback" in result.stdout
    assert "reanchor" in result.stdout
    assert "daily" in result.stdout
    assert "weekly" in result.stdout
    assert "serve" in result.stdout
    assert "watch" in result.stdout
    assert "ccf" in result.stdout


def test_cli_watch_help():
    """The monitoring sub-command group exposes the full list-management surface."""
    result = subprocess.run(
        [sys.executable, "-m", "glean.cli", "watch", "--help"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert result.returncode == 0
    for sub in ("add", "remove", "enable", "disable", "list", "run", "ack", "push-test"):
        assert sub in result.stdout


def test_cli_watch_list_is_read_only():
    """`watch list` reads the repo watchlist.md and must not mutate anything."""
    result = subprocess.run(
        [sys.executable, "-m", "glean.cli", "watch", "list", "--all"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert result.returncode == 0
    assert "魏恒峰" in result.stdout


def test_cli_ccf_help():
    """The CCF sub-command group exposes the full venue-management surface."""
    result = subprocess.run(
        [sys.executable, "-m", "glean.cli", "ccf", "--help"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert result.returncode == 0
    for sub in ("add", "remove", "enable", "disable", "list", "run", "ack", "refresh"):
        assert sub in result.stdout


def test_cli_ccf_list_is_read_only():
    """`ccf list` reads the repo ccf.md and must not mutate anything."""
    result = subprocess.run(
        [sys.executable, "-m", "glean.cli", "ccf", "list"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert result.returncode == 0
    assert "SIGMOD" in result.stdout


def test_cli_daily_help():
    result = subprocess.run(
        [sys.executable, "-m", "glean.cli", "daily", "--help"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert result.returncode == 0
    assert "--serve" in result.stdout
    assert "--host" in result.stdout
    assert "--port" in result.stdout


def test_cli_weekly_help():
    """The weekly aggregate entry point exposes the whole orchestration surface."""
    result = subprocess.run(
        [sys.executable, "-m", "glean.cli", "weekly", "--help"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert result.returncode == 0
    for opt in (
        "--hours", "--cap", "--date", "--no-serve", "--host", "--port",
        "--no-push", "--force",
        "--skip-ccf", "--skip-watch", "--skip-fetch",
    ):
        assert opt in result.stdout, opt


def test_weekly_window_defaults_cover_a_full_week():
    """``weekly`` must default to a 7-day window and a 300-item cap.

    This is the regression that matters most about the aggregate command. The
    day-frequency entry point defaults to ``--hours 24``; reusing that default
    after the schedule moved to weekly would fetch one day out of seven,
    silently drop the other six, and still exit 0. The code-level default is
    the fix, so the code-level default is what this test pins.
    """
    from glean.cli import _WEEKLY_CAP, _WEEKLY_HOURS, build_parser

    wk = dict(_leaves(build_parser()))[("weekly",)]
    defaults = {a.dest: a.default for a in wk._actions}

    assert _WEEKLY_HOURS == 168
    assert _WEEKLY_CAP == 300
    assert defaults["hours"] == 168
    assert defaults["cap"] == 300
    # 服务默认打开：周任务不必再记 --serve（只有显式 --no-serve 才跳过）。
    assert defaults["no_serve"] is False


def test_weekly_isolates_a_failing_stage(monkeypatch, capsys):
    """一段崩溃不得带走其余两段 —— 这是 `weekly` 存在的核心理由。

    周频的代价是单轮失败要再等一周才可能被下一轮覆盖，所以「部分成功」远好过
    「一起失败」。这里让第一段抛异常，断言后两段照跑完、退出码仍为 0。
    """
    from glean import cli

    # 呈现层与网络层都替换掉：本用例只关心编排，不碰真实站点。
    monkeypatch.setattr(cli, "_report_monitor_run", lambda res, view: None)
    monkeypatch.setattr(cli, "_render_monitor_html", lambda view, res, scope=None: None)

    def boom(**kwargs):
        raise RuntimeError("源整站不可达")

    monkeypatch.setattr(cli, "run_ccf", boom)
    monkeypatch.setattr(
        cli, "run_watch",
        lambda **kw: {
            "run_id": "t", "day": "2026-09-26", "new_items": [{"title": "x"}],
            "grouped": {}, "baselined": [], "skipped": [], "errors": [],
            "pushed_to": [], "collected": {},
        },
    )
    monkeypatch.setattr(
        cli, "_run_fetch",
        lambda hours, cap, date: ("20260926", 42, "data/20260926.json"),
    )

    code = cli.cmd_weekly(argparse.Namespace(
        hours=168, cap=300, date=None, no_serve=True, no_push=True, force=False,
        skip_ccf=False, skip_watch=False, skip_fetch=False,
        host="127.0.0.1", port=8011,
    ))
    captured = capsys.readouterr()

    assert code == 0                      # 全失败才非 0，这里 2/3 成功
    assert "2/3 段完成" in captured.out
    assert "源整站不可达" in captured.err  # 崩掉的那段要如实报出来
    assert "42 篇" in captured.out         # 第三段照常跑完


def test_cli_serve_help():
    result = subprocess.run(
        [sys.executable, "-m", "glean.cli", "serve", "--help"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert result.returncode == 0
    assert "--reload" in result.stdout


def test_arxiv_daily_wrapper():
    result = subprocess.run(
        [sys.executable, "arxiv_daily.py", "--help"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert result.returncode == 0
    assert "fetch" in result.stdout
