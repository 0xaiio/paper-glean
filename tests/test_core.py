"""Tests for glean/core.py"""

from __future__ import annotations

import email.message
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


# ------------------------------------------------------------------
# One HTTP entry point, one User-Agent policy
# ------------------------------------------------------------------

class _FakeResponse:
    """Just enough of ``http.client.HTTPResponse`` for the two helpers."""

    def __init__(self, body: bytes, content_type: str | None = None) -> None:
        self._body = body
        self.headers = email.message.Message()
        if content_type is not None:
            self.headers["Content-Type"] = content_type

    def read(self) -> bytes:
        return self._body

    def __enter__(self) -> _FakeResponse:
        return self

    def __exit__(self, *exc: object) -> bool:
        return False


@pytest.fixture
def http_stub(monkeypatch):
    """Capture outbound requests instead of hitting the network.

    Returns ``(calls, replies)``; the test queues one reply per expected call.
    """
    from glean import core

    calls: list[tuple[object, int | None]] = []
    replies: list[_FakeResponse] = []

    def fake_urlopen(req, timeout=None):
        calls.append((req, timeout))
        return replies.pop(0)

    monkeypatch.setattr(core.urllib.request, "urlopen", fake_urlopen)
    return calls, replies


def test_http_helpers_share_one_request_factory(http_stub):
    """``http_get`` / ``http_get_text`` must not drift into two UA policies.

    Both arXiv / DBLP / Semantic Scholar and the homepage+venue scrapers used to
    build their own ``Request``; they now share ``_http_request``.
    """
    from glean import core

    calls, replies = http_stub
    replies.append(_FakeResponse(b"%PDF-1.4"))
    replies.append(_FakeResponse(b"<html/>", "text/html; charset=utf-8"))

    core.http_get("https://example.org/paper.pdf", timeout=5)
    core.http_get_text("https://example.org/home")

    assert [req.full_url for req, _ in calls] == [
        "https://example.org/paper.pdf",
        "https://example.org/home",
    ]
    assert [req.get_header("User-agent") for req, _ in calls] == [core.UA, core.UA]
    assert [timeout for _, timeout in calls] == [5, 60]  # default timeout kept


def test_http_get_text_honours_content_type_charset(http_stub):
    from glean import core

    _, replies = http_stub
    replies.append(
        _FakeResponse("数据库与形式化验证".encode("gb18030"), "text/html; charset=gb18030")
    )

    assert core.http_get_text("https://example.org/gbk") == "数据库与形式化验证"


def test_http_get_text_degrades_instead_of_raising_on_bad_charset(http_stub):
    """An unknown or absent charset must fall back to UTF-8, not abort a scan."""
    from glean import core

    _, replies = http_stub
    replies.append(_FakeResponse("bogus — ok".encode(), "text/html; charset=no-such-codec"))
    replies.append(_FakeResponse("plain — ok".encode()))

    assert core.http_get_text("https://example.org/a") == "bogus — ok"
    assert core.http_get_text("https://example.org/b") == "plain — ok"


def test_homeparse_fetch_html_delegates_to_core(monkeypatch):
    """Homepage scraping shares the core request path — no second ``urlopen``."""
    from glean import homeparse

    seen: list[tuple[str, int]] = []

    def fake_get_text(url, timeout=60):
        seen.append((url, timeout))
        return "<html>hi</html>"

    monkeypatch.setattr(homeparse, "http_get_text", fake_get_text)

    assert homeparse.fetch_html("https://example.org/", timeout=7) == "<html>hi</html>"
    assert seen == [("https://example.org/", 7)]
