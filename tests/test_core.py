"""Tests for glean/core.py"""

from __future__ import annotations

import json

import pytest

from glean.core import (
    annotate_hits,
    excerpt,
    find_paper,
    list_available_days,
    load_interest_entries,
    match_keywords,
    sanitize_title,
)


def test_excerpt_short_text():
    text = "Hello world. This is a test."
    result = excerpt(text, limit=400)
    assert result == "Hello world. This is a test."


def test_excerpt_long_text():
    text = "A" * 500
    result = excerpt(text, limit=100)
    assert len(result) <= 104  # 100 + " …"
    assert result.endswith(" …")


def test_sanitize_title():
    assert sanitize_title("Hello: World?") == "Hello World"
    assert sanitize_title("Test $100") == "Test 100"


def test_match_keywords():
    paper = {"title": "Consensus Protocols", "abstract": "We study consensus and BFT."}
    hits = match_keywords(paper, ["consensus", "BFT", "learning"])
    assert "consensus" in hits
    assert "BFT" in hits
    assert "learning" not in hits


def test_load_interest_entries():
    entries = load_interest_entries()
    assert isinstance(entries, list)
    if entries:
        assert "section" in entries[0]
        assert "title" in entries[0]
        assert "keywords" in entries[0]
        assert "weight" in entries[0]


def test_find_paper_existing():
    paper, day = find_paper("2607.25916")
    assert paper is not None
    assert day is not None
    assert paper["id"] == "2607.25916"


def test_find_paper_nonexistent():
    paper, day = find_paper("9999.99999")
    assert paper is None
    assert day is None


# ------------------------------------------------------------------
# data/ enumerates *days*, not every JSON living in that directory
# ------------------------------------------------------------------

def _day_payload(day: str, *ids: str) -> str:
    return json.dumps(
        {"day": day, "window_utc": ["", ""], "papers": [{"id": i} for i in ids]}
    )


@pytest.fixture
def isolated_data_dir(tmp_path, monkeypatch):
    """A data/ directory holding one real day plus monitor state files.

    ``watch_state.json`` / ``ccf_state.json`` / ``watch_new.json`` live in the
    same directory by design (see docs/developer-guide/data-schema.md).
    """
    from glean import core

    (tmp_path / "20260729.json").write_text(
        _day_payload("20260729", "2607.25916"), encoding="utf-8"
    )
    (tmp_path / "20260801.json").write_text(
        _day_payload("20260801", "2608.00001"), encoding="utf-8"
    )
    for name in ("watch_state.json", "ccf_state.json", "watch_new.json"):
        (tmp_path / name).write_text('{"version": 1}', encoding="utf-8")
    monkeypatch.setattr(core, "DATA_DIR", tmp_path)
    return tmp_path


def test_list_available_days_ignores_monitor_state(isolated_data_dir):
    """Regression: globbing data/*.json surfaced ``watch_state`` and friends as
    days, so the web UI defaulted to a "day" with zero papers."""
    assert list_available_days() == ["20260801", "20260729"]


def test_list_available_days_is_empty_without_data_dir(tmp_path, monkeypatch):
    from glean import core

    monkeypatch.setattr(core, "DATA_DIR", tmp_path / "missing")
    assert list_available_days() == []


def test_find_paper_skips_monitor_state_files(isolated_data_dir):
    """The state files carry no ``papers`` key; searching must not choke on them."""
    assert find_paper("2607.25916") == ({"id": "2607.25916"}, "20260729")
    assert find_paper("nope") == (None, None)
