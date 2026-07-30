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
