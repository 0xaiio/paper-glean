"""Best-effort extraction of CFP / program / accepted-paper links from a venue page.

Why this exists
---------------
"Did SIGMOD publish its program yet?" is a question no paper-index answers —
DBLP and Semantic Scholar only know about *accepted papers*, and only after the
fact. The venue's own site is the only place where a Call for Papers, a
technical program and an accepted-papers list appear, so a homepage parser is
unavoidable for the monitoring scope「CFP / Program / 接收论文列表」.

Two sources, deliberately asymmetric
------------------------------------
``ccfddl``   ccfddl.com's RSS announces every submission deadline with its CCF
             rank. That is a *structured, high-confidence* CFP signal — far
             better than scraping — so CFP detection is driven by it.
``homepage`` Everything else. Same heuristic discipline as
             :mod:`glean.homeparse`: prefer missing an item over inventing one,
             and stamp every item with a ``confidence``.

Known limits
------------
* **DBLP is unusable for scraping**: as of 2026-09 every dblp.org endpoint
  (HTML *and* API) answers with an Anubis "Making sure you're not a bot!"
  interstitial. ``dblp`` URLs are therefore kept as *human reference links*
  only and are never fetched.
* JavaScript-rendered venue sites yield nothing.
"""

from __future__ import annotations

import html
import json
import re
import urllib.parse
from datetime import datetime

from glean.config import CCFDDL_RSS, CCF_TIMEOUT
from glean.homeparse import _AnchorParser, _clean, fetch_html

# --- classification tables -------------------------------------------------

_CFP_HINTS = (
    "cfp", "call-for-paper", "call_for_paper", "callforpaper", "call for paper",
    "submission", "submit", "author-instruction", "author instruction", "征稿",
)
_PROGRAM_HINTS = (
    "program", "schedule", "timetable", "agenda", "technical-session",
    "session", "keynote", "日程", "程序",
)
_PAPERS_HINTS = (
    "accepted", "accept-paper", "proceeding", "paper", "toc",
    "table-of-content", "award", "best-paper", "content",
)
# Journal-specific: a new issue/volume is the periodical analogue of a
# conference's accepted-papers list.
_ISSUE_HINTS = (
    "current-issue", "current_issue", "latest-issue", "issue", "volume",
    "articles-in-press", "articles in press", "advance-access", "online-first",
)

_NAV_TEXT = {
    "home", "index", "main", "registration", "register", "venue", "travel",
    "accommodation", "hotel", "committee", "organizers", "organisers",
    "sponsors", "sponsor", "contact", "about", "login", "visa", "dates",
    "important dates", "call for participation", "workshops", "tutorials",
    "demo", "poster", "doctoral symposium", "grant", "student", "code of conduct",
    "privacy", "terms", "sitemap", "past", "archive", "photos", "gallery",
}

_YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")


def _classify(href: str, text: str) -> tuple[str, float]:
    """Return ``(kind, confidence)`` for one candidate anchor."""
    low_href = href.lower()
    low_text = text.lower()
    joined = low_text + " " + low_href

    # Order matters: "call for papers" contains "paper", so CFP is tested first.
    if any(h in joined for h in _CFP_HINTS):
        return "cfp", 0.9 if any(h in low_text for h in _CFP_HINTS) else 0.75
    if any(h in joined for h in _PROGRAM_HINTS):
        return "program", 0.85 if any(h in low_text for h in _PROGRAM_HINTS) else 0.7
    if any(h in joined for h in _PAPERS_HINTS):
        return "papers", 0.85 if any(h in low_text for h in _PAPERS_HINTS) else 0.7
    if any(h in joined for h in _ISSUE_HINTS):
        return "papers", 0.6
    return "other", 0.3


def _title_from_href(href: str) -> str:
    name = urllib.parse.unquote(href.rstrip("/").rsplit("/", 1)[-1])
    name = re.sub(r"\.(pdf|html?|php|aspx)$", "", name, flags=re.I)
    name = name.replace("_", " ").replace("-", " ").replace("%20", " ")
    return _clean(name)


def parse_venue_page(
    url: str,
    html_text: str | None = None,
    min_confidence: float = 0.5,
) -> list[dict]:
    """Extract CFP / program / accepted-paper items from a venue homepage.

    Never raises — network and parse failures yield ``[]``.
    """
    if html_text is None:
        try:
            html_text = fetch_html(url, timeout=CCF_TIMEOUT)
        except Exception:
            return []

    parser = _AnchorParser()
    try:
        parser.feed(html_text)
    except Exception:  # malformed HTML is the norm
        pass

    items: list[dict] = []
    seen: set[str] = set()

    for href, text in parser.anchors:
        if not href or href.startswith(("#", "mailto:", "javascript:", "tel:")):
            continue
        abs_url = urllib.parse.urljoin(url, href)
        parsed = urllib.parse.urlparse(abs_url)
        if not parsed.path.strip("/"):  # bare site root = logo, never content
            continue

        label = _clean(text)
        if label.lower().strip("[]() ") in _NAV_TEXT:
            continue
        if not label or len(label) < 3:
            label = _title_from_href(href)
            if len(label) < 3:
                continue
        if label.lower() in _NAV_TEXT:
            continue

        kind, confidence = _classify(abs_url, label)
        if kind == "other" or confidence < min_confidence:
            continue

        key = re.sub(r"[^a-z0-9]+", "", (label + parsed.path).lower())[:100]
        if not key or key in seen:
            continue
        seen.add(key)

        year_match = _YEAR_RE.search(label) or _YEAR_RE.search(abs_url)
        year = int(year_match.group()) if year_match else None

        items.append(
            {
                "title": label[:160],
                "url": abs_url,
                "kind": kind,
                "year": year,
                "deadline": "",
                "venue": "",
                "source": "homepage",
                "confidence": round(confidence, 2),
            }
        )
    return items


# ------------------------------------------------------------------
# Crossref — journal volumes/issues
# ------------------------------------------------------------------

CROSSREF_JOURNAL_WORKS = "https://api.crossref.org/journals/{issn}/works"


def fetch_crossref_issues(
    issn: str,
    venue: str,
    homepage: str = "",
    *,
    since_year: int | None = None,
    rows: int = 100,
    max_issues: int = 8,
    timeout: int = CCF_TIMEOUT,
) -> list[dict]:
    """Return the newest (volume, issue) pairs Crossref has indexed for a journal.

    Why Crossref and not the publisher: ACM DL and IEEE Xplore render their
    tables of contents in JavaScript, and DBLP is behind an anti-bot wall, so
    Crossref's open API is the only machine-readable "what has this journal
    published" signal left.

    The identity of an item is ``(venue, volume, issue)`` — deliberately *not*
    the article count or date, so a steady trickle of articles into an already
    announced issue does not re-announce it.
    """
    if not issn:
        return []
    year = since_year or (datetime.now().year - 1)
    url = (
        CROSSREF_JOURNAL_WORKS.format(issn=urllib.parse.quote(issn))
        + f"?filter=from-pub-date:{year}-01-01&rows={rows}"
        + "&select=DOI,volume,issue,published,title"
    )
    try:
        data = json.loads(fetch_html(url, timeout=timeout))
    except Exception:
        return []

    groups: dict[tuple[str, str], dict[str, Any]] = {}
    for work in data.get("message", {}).get("items", []):
        volume = (work.get("volume") or "").strip()
        issue = (work.get("issue") or "").strip()
        if not volume and not issue:
            continue
        parts = (work.get("published") or {}).get("date-parts") or [[None]]
        ymd = parts[0] if parts else [None]
        try:
            pub_year = int(ymd[0])
        except (TypeError, ValueError, IndexError):
            pub_year = None
        key = (volume, issue)
        rec = groups.setdefault(
            key, {"volume": volume, "issue": issue, "count": 0, "year": pub_year}
        )
        rec["count"] += 1
        if pub_year and (rec["year"] is None or pub_year > rec["year"]):
            rec["year"] = pub_year

    def sort_key(rec: dict[str, Any]) -> tuple[int, int, int]:
        def as_int(value: str) -> int:
            return int(re.sub(r"\D", "", value) or 0)

        return (rec["year"] or 0, as_int(rec["volume"]), as_int(rec["issue"]))

    ordered = sorted(groups.values(), key=sort_key, reverse=True)[:max_issues]
    items: list[dict] = []
    for rec in ordered:
        label = f"{venue} Volume {rec['volume']}" if rec["volume"] else venue
        if rec["issue"]:
            label += f" Issue {rec['issue']}"
        items.append(
            {
                "title": label,
                # The homepage (not a DOI) keeps the fingerprint stable: a DOI
                # of "the first article" changes as Crossref's ordering shifts.
                "url": homepage,
                "kind": "papers",
                "year": rec["year"],
                "deadline": "",
                "venue": venue,
                "source": "crossref",
                "confidence": 0.95,
                "article_count": rec["count"],
            }
        )
    return items


# ------------------------------------------------------------------
# ccfddl — structured CFP announcements
# ------------------------------------------------------------------

def fetch_rss(url: str = CCFDDL_RSS, timeout: int = CCF_TIMEOUT) -> str:
    """Download the ccfddl RSS feed. Raises on failure (caller decides)."""
    return fetch_html(url, timeout=timeout)


def parse_ccfddl(xml_text: str, venue: str, min_year: int | None = None) -> list[dict]:
    """Return the CFP announcements ccfddl lists for ``venue``.

    ``venue`` must match the feed's own spelling ("SIGMOD", "S&P", "ACM MM",
    "UbiComp/ISWC", ...). Matching is exact and case-insensitive on the part of
    the title before the year, which is how the catalogue stores names.
    """
    target = (venue or "").strip().lower()
    if not target:
        return []

    items: list[dict] = []
    for block in re.findall(r"<item>(.*?)</item>", xml_text or "", re.S):
        title_m = re.search(r"<title>(.*?)</title>", block, re.S)
        link_m = re.search(r"<link>(.*?)</link>", block, re.S)
        desc_m = re.search(r"<description>(.*?)</description>", block, re.S)
        if not title_m:
            continue
        title = _clean(html.unescape(title_m.group(1)))
        m = re.match(r"^(.*?)\s+((?:19|20)\d{2})\b", title)
        if not m or m.group(1).strip().lower() != target:
            continue
        year = int(m.group(2))
        if min_year is not None and year < min_year:
            continue

        lines = [
            _clean(ln)
            for ln in html.unescape(desc_m.group(1)).splitlines()
            if ln.strip()
        ] if desc_m else []
        deadline = ""
        for ln in lines:
            if ln.lower().startswith("deadline"):
                deadline = ln.split(":", 1)[1].strip() if ":" in ln else ln
                break

        items.append(
            {
                "title": title,
                "url": (link_m.group(1).strip() if link_m else ""),
                "kind": "cfp",
                "year": year,
                "deadline": deadline,
                "venue": venue,
                "source": "ccfddl",
                "confidence": 0.95,
            }
        )
    return items
