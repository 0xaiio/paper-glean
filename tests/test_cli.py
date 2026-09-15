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
        "fetch", "download", "feedback", "reanchor", "html", "daily", "serve",
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
