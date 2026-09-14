"""Tests for :mod:`glean.venueparse` — venue page + ccfddl + Crossref parsing."""

from __future__ import annotations

import json

import pytest

from glean import venueparse

PAGE = """
<html><body>
  <a href="/"><img src="logo.png"></a>
  <a href="/">Home</a>
  <a href="https://2027.sigmod.org/cfp/">Call for Papers</a>
  <a href="technical-program.html">Technical Program</a>
  <a href="accepted-papers.html">Accepted Papers</a>
  <a href="registration.html">Registration</a>
  <a href="mailto:chair@example.org">Contact chair</a>
  <a href="https://twitter.com/sigmod">Twitter</a>
</body></html>
"""

RSS = """<rss><channel>
<item><title>SIGMOD 2027 Abstract Deadline</title><link>https://2027.sigmod.org/</link>
<description>ACM Conference on Management of Data
Deadline (UTC-12): 2026-07-25 23:59:59</description></item>
<item><title>SIGMOD 2027 Deadline</title><link>https://2027.sigmod.org/</link>
<description>ACM Conference on Management of Data
Deadline (UTC-12): 2026-08-01 23:59:59</description></item>
<item><title>SIGMOD 2021 Deadline</title><link>https://2021.sigmod.org/</link>
<description>old
Deadline (UTC-12): 2020-08-01 23:59:59</description></item>
<item><title>PODS 2027 Deadline</title><link>https://2027.sigmod.org/</link>
<description>other venue
Deadline (UTC-12): 2026-09-01 23:59:59</description></item>
<item><title>S&amp;P 2027 Deadline</title><link>https://sp2027.ieee-security.org/</link>
<description>IEEE Symposium on Security &amp; Privacy
Deadline (UTC-12): 2026-09-05 23:59:59</description></item>
</channel></rss>"""

CROSSREF = json.dumps(
    {
        "message": {
            "items": [
                {"DOI": "10.1/a", "volume": "51", "issue": "2",
                 "published": {"date-parts": [[2026, 3, 6]]}},
                {"DOI": "10.1/b", "volume": "51", "issue": "3",
                 "published": {"date-parts": [[2026, 3, 27]]}},
                {"DOI": "10.1/c", "volume": "51", "issue": "3",
                 "published": {"date-parts": [[2026, 4, 1]]}},
                {"DOI": "10.1/d", "volume": "50", "issue": "4",
                 "published": {"date-parts": [[2025, 12, 1]]}},
                {"DOI": "10.1/e", "title": ["no volume or issue"]},
            ]
        }
    }
)


# ------------------------------------------------------------------
# venue homepage
# ------------------------------------------------------------------

def test_parse_venue_page_classifies_the_three_signals():
    items = venueparse.parse_venue_page("https://2027.sigmod.org/", html_text=PAGE)
    by_kind = {}
    for it in items:
        by_kind.setdefault(it["kind"], []).append(it)
    assert set(by_kind) == {"cfp", "program", "papers"}
    assert by_kind["cfp"][0]["title"] == "Call for Papers"
    assert by_kind["program"][0]["title"] == "Technical Program"
    assert by_kind["papers"][0]["title"] == "Accepted Papers"
    assert all(i["source"] == "homepage" for i in items)


def test_parse_venue_page_drops_nav_and_root_links():
    items = venueparse.parse_venue_page("https://2027.sigmod.org/", html_text=PAGE)
    titles = {i["title"].lower() for i in items}
    assert "registration" not in titles
    assert "home" not in titles
    urls = [i["url"] for i in items]
    assert "https://2027.sigmod.org/" not in urls  # bare root = logo


def test_parse_venue_page_makes_urls_absolute():
    items = venueparse.parse_venue_page("https://2027.sigmod.org/index.html", html_text=PAGE)
    assert all(i["url"].startswith("https://2027.sigmod.org/") for i in items)


def test_parse_venue_page_never_raises_on_garbage():
    assert venueparse.parse_venue_page("https://x/", html_text="<<<not html") == []


# ------------------------------------------------------------------
# ccfddl
# ------------------------------------------------------------------

def test_parse_ccfddl_matches_venue_and_reads_deadline():
    items = venueparse.parse_ccfddl(RSS, "SIGMOD")
    assert [i["title"] for i in items] == [
        "SIGMOD 2027 Abstract Deadline",
        "SIGMOD 2027 Deadline",
        "SIGMOD 2021 Deadline",
    ]
    assert items[0]["deadline"] == "2026-07-25 23:59:59"
    assert items[0]["kind"] == "cfp"
    assert items[0]["source"] == "ccfddl"
    assert items[0]["confidence"] == 0.95


def test_parse_ccfddl_honours_min_year():
    items = venueparse.parse_ccfddl(RSS, "SIGMOD", min_year=2026)
    assert all(i["year"] >= 2026 for i in items)
    assert len(items) == 2


def test_parse_ccfddl_unescapes_html_entities():
    """'S&P' arrives as 'S&amp;P' and must still match — it is a CCF-A venue."""
    items = venueparse.parse_ccfddl(RSS, "S&P")
    assert [i["title"] for i in items] == ["S&P 2027 Deadline"]


def test_parse_ccfddl_ignores_other_venues_and_empty_names():
    assert venueparse.parse_ccfddl(RSS, "ICDE") == []
    assert venueparse.parse_ccfddl(RSS, "") == []


# ------------------------------------------------------------------
# Crossref
# ------------------------------------------------------------------

def test_fetch_crossref_issues_groups_by_volume_and_issue(monkeypatch):
    monkeypatch.setattr(venueparse, "fetch_html", lambda *a, **k: CROSSREF)
    items = venueparse.fetch_crossref_issues(
        "0362-5915", "TODS", "https://dl.acm.org/journal/tods"
    )
    assert [i["title"] for i in items] == [
        "TODS Volume 51 Issue 3",
        "TODS Volume 51 Issue 2",
        "TODS Volume 50 Issue 4",
    ]
    assert items[0]["article_count"] == 2
    assert items[0]["kind"] == "papers"
    assert items[0]["source"] == "crossref"


def test_crossref_url_is_the_homepage_so_fingerprints_stay_stable(monkeypatch):
    """All issues share the journal URL: identity = (venue, volume, issue)."""
    monkeypatch.setattr(venueparse, "fetch_html", lambda *a, **k: CROSSREF)
    items = venueparse.fetch_crossref_issues("0362-5915", "TODS", "https://dl.acm.org/journal/tods")
    assert {i["url"] for i in items} == {"https://dl.acm.org/journal/tods"}


@pytest.mark.parametrize("issn", ["", None])
def test_fetch_crossref_issues_without_issn_is_a_noop(issn, monkeypatch):
    called = []
    monkeypatch.setattr(venueparse, "fetch_html", lambda *a, **k: called.append(a) or CROSSREF)
    assert venueparse.fetch_crossref_issues(issn, "TODS") == []
    assert called == []


def test_fetch_crossref_issues_swallows_network_failure(monkeypatch):
    def boom(*a, **k):
        raise OSError("crossref down")

    monkeypatch.setattr(venueparse, "fetch_html", boom)
    assert venueparse.fetch_crossref_issues("0362-5915", "TODS") == []
