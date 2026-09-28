"""Tests for identity resolution (``glean.resolve``).

Everything here is offline: the network is always faked, because the point of
these tests is the *decision rules* (what may be auto-filled, what must be
handed to the user, how a failure is described), not the sources themselves.
"""

from __future__ import annotations

import pathlib

import pytest

from glean import resolve


# --- offline: title -> name ------------------------------------------------

@pytest.mark.parametrize(
    "title,expected",
    [
        ("Hengfeng Wei (魏恒峰)", "Hengfeng Wei (魏恒峰)"),
        ("Alexey Gotsman's Home Page", "Alexey Gotsman"),
        ("Alice Lin | University of X", "Alice Lin"),
        ("魏恒峰", "魏恒峰"),
        ("Publications", None),
        ("Home", None),
        ("SIGMOD 2026", None),
    ],
)
def test_name_from_title(title, expected):
    assert resolve.name_from_title(title) == expected


def test_name_from_homepage_prefers_h1_and_says_where_it_came_from():
    page = "<html><head><title>Some Site</title></head><body><h1>Alice Lin</h1></body></html>"
    name, where = resolve.name_from_homepage(page)
    assert (name, where) == ("Alice Lin", "h1")


# --- offline: input normalisation ------------------------------------------

@pytest.mark.parametrize(
    "value,expected",
    [
        ("pid/00/0000", "pid/00/0000"),
        ("https://dblp.org/pid/12/3456.html", "pid/12/3456"),
        ("12/3456", "pid/12/3456"),
        ("Hengfeng Wei", None),  # a name is not a pid
    ],
)
def test_normalize_dblp(value, expected):
    assert resolve.normalize_dblp(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("2294609531", ("2294609531", None)),
        # The id is the trailing numeric segment; the slug is a *name*. Taking
        # the first alphanumeric run yields "Hengfeng", which the API 404s on.
        ("https://www.semanticscholar.org/author/Hengfeng-Wei/3068641", ("3068641", None)),
        ("https://www.semanticscholar.org/author/3068641", ("3068641", None)),
        ("Hengfeng Wei", (None, "Hengfeng Wei")),
    ],
)
def test_normalize_s2(value, expected):
    assert resolve.normalize_s2(value) == expected


def test_dblp_is_never_requested():
    """DBLP answers every request with an Anubis bot check.

    So no request line may mention it: a failed fetch would be indistinguishable
    from "no such person", and the module must say that out loud instead.
    """
    src = pathlib.Path(resolve.__file__).read_text(encoding="utf-8")
    for line in src.splitlines():
        if "http_get" in line:
            assert "dblp" not in line.lower(), line
    assert "DBLP 已启用反爬" in src


# --- decision rules -------------------------------------------------------

def _candidate(name, s2, papers):
    return {
        "name": name, "s2": s2, "affiliations": [], "paper_count": papers,
        "homepage": None, "dblp_name": None,
    }


def _fake_search(candidates, warning=None):
    return lambda *a, **k: (candidates, warning)


def test_ambiguous_name_search_is_never_auto_selected(monkeypatch):
    """Two same-named people must not become a silent coin flip.

    Auto-filling the wrong namesake's id points every future scan at the wrong
    publication list — the failure is invisible until the digests look wrong.
    """
    monkeypatch.setattr(resolve, "s2_search", _fake_search([
        _candidate("Alexey Gotsman", "2", 3),
        _candidate("Alexey Gotsman", "1", 60),
    ]))

    out = resolve.resolve(name="Alexey Gotsman")

    assert out["resolved"]["s2"] is None
    assert out["needs_review"] is True
    assert any("候选" in w for w in out["warnings"])
    # Most prolific first, so the likely target is the one to eyeball first.
    assert [a["s2"] for a in out["alternates"]] == ["1", "2"]


def test_a_single_candidate_is_adopted(monkeypatch):
    """One unambiguous hit may be filled in — but it is still marked for review."""
    monkeypatch.setattr(resolve, "s2_search", _fake_search([_candidate("Unique Person", "7", 12)]))
    out = resolve.resolve(name="Unique Person")
    assert out["resolved"]["s2"] == "7"
    assert out["resolved"]["name"] == "Unique Person"
    assert out["needs_review"] is True  # the id was inferred, not typed


def test_a_rate_limit_is_not_reported_as_no_such_person(monkeypatch):
    monkeypatch.setattr(resolve, "s2_search", _fake_search([], resolve.S2_RATE_LIMITED))
    out = resolve.resolve(name="Someone")
    assert resolve.S2_RATE_LIMITED in out["warnings"]
    assert out["resolved"]["name"] == "Someone"


def test_empty_input_yields_no_name_and_still_explains_itself():
    out = resolve.resolve()
    assert out["resolved"]["name"] == ""
    assert out["needs_review"] is True
    assert any("未能推断出姓名" in w for w in out["warnings"])


def test_dblp_input_is_recorded_but_flagged_as_unverifiable():
    out = resolve.resolve(dblp="pid/00/0000")
    assert out["resolved"]["dblp"] == "pid/00/0000"
    assert resolve.DBLP_UNFETCHABLE in out["warnings"]
    assert out["needs_review"] is True


def test_homepage_supplies_the_name_and_the_ids_it_links_to(monkeypatch):
    page = (
        "<html><head><title>Alice Lin</title></head><body>"
        '<a href="https://dblp.org/pid/12/3456.html">DBLP</a>'
        '<a href="https://www.semanticscholar.org/author/Alice-Lin/999">S2</a>'
        "</body></html>"
    )
    monkeypatch.setattr(resolve, "http_get_text", lambda url, timeout=0: page)

    out = resolve.resolve(homepage="https://example.edu/~alice")

    assert out["resolved"]["name"] == "Alice Lin"
    assert out["resolved"]["dblp"] == "pid/12/3456"
    assert out["resolved"]["s2"] == "999"
    # Still flagged: the name came off a web page, not out of the user's hands.
    assert out["needs_review"] is True


def test_an_unreachable_homepage_becomes_a_warning_not_an_exception(monkeypatch):
    def boom(url, timeout=0):
        raise OSError("Tunnel connection failed: 502 Bad Gateway")

    monkeypatch.setattr(resolve, "http_get_text", boom)
    # Guard: nothing in this path should reach the search, but if that changes we
    # do not want the test silently hitting the network.
    monkeypatch.setattr(resolve, "s2_search", _fake_search([]))

    out = resolve.resolve(homepage="https://unreachable.example/x")

    assert any("个人主页抓取失败" in w for w in out["warnings"])
    assert out["resolved"]["homepage"] == "https://unreachable.example/x"
