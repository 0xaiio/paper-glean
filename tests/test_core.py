"""Tests for glean/core.py"""

from __future__ import annotations

import pytest

from glean.core import (
    annotate_hits,
    excerpt,
    find_paper,
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
