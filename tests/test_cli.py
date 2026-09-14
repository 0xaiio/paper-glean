"""Tests for CLI commands."""

from __future__ import annotations

import subprocess
import sys


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
