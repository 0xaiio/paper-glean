"""Best-effort extraction of "works" from a researcher's homepage.

Why this module exists
----------------------
Semantic Scholar and DBLP only index **papers**. Talks, tutorial videos and
technical reports (TR) live on a person's homepage and nowhere else, so a
homepage parser is required to honour the monitoring scope
「论文 / 视频 / 技术报告」.

This is deliberately a **heuristic** parser: homepages have no schema. It looks
for anchors whose ``href`` or text smells like a work, and it prefers to *miss*
an item over emitting noise — a false "new paper" push is far more costly than
a missed one. Every returned item carries a ``confidence`` so downstream code
and the UI can surface doubt.

Zero third-party dependencies (stdlib ``html.parser`` only), in keeping with
the project principle「CLI 永远是 fallback / 零外部依赖」.

Known limits
------------
* Homepages that render publications via JavaScript will yield nothing.
* Very terse homepages (bare link lists, no titles) yield low-confidence items.
* These are accepted trade-offs: DBLP / Semantic Scholar act as the fallback
  (see :mod:`glean.watch`), and the Web UI marks low-confidence items.
"""

from __future__ import annotations

import html
import re
import urllib.parse
from html.parser import HTMLParser

from glean.config import UA, WATCH_TIMEOUT

# --- classification tables -------------------------------------------------

_VIDEO_HINTS = ("youtube.com", "youtu.be", "bilibili.com", "vimeo.com", "youku.com")
_REPORT_HINTS = (
    "technical report", "tech report", "techreport", "technical memo",
    "tr-", "tr ", " arxiv:", "arxiv.org/abs", "report no",
)
_TALK_HINTS = ("talk", "tutorial", "keynote", "webinar", "lecture", "seminar", "报告")
_PAPER_HINTS = (
    ".pdf", "arxiv.org", "doi.org", "dblp.org", "openreview.net",
    "aclanthology.org", "dl.acm.org", "link.springer.com", "ieeexplore.ieee.org",
    "proceedings", "pmlr.press", "jmlr.org",
)

_NAV_TEXT = {
    "home", "publications", "publication", "papers", "paper", "teaching",
    "teach", "cv", "resume", "bio", "about", "contact", "students", "group",
    "research", "software", "code", "talks", "blog", "news", "links", "pdf",
    "abstract", "slides", "bibtex", "doi", "link", "homepage", "index",
    "service", "awards", "grants", "projects", "project",
}

_YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")
# CS venues often abbreviate the year to two digits in filenames (sigmod26.pdf).
_VENUE_YEAR_RE = re.compile(
    r"\b(sigmod|pvldb|vldb|icde|sosp|osdi|podc|disc|opodis|eurosys|nsdi|pods|"
    r"icdt|tods|toplas|pldi|popl|icfp|cav|tacas|fmcad|atva|concur|lmcs|jacm|"
    r"atc|fast|sc|hpca|isca|micro|asplos|ccs|ndss|uss|www|kdd|aaai|ijcai|nips|"
    r"neurips|icml|iclr|acl|emnlp|naacl|cvpr|iccv|eccv|siggraph|chi|uist|ubicomp)"
    r"[\s\-_']?(\d{2})\b",
    re.I,
)
_WS_RE = re.compile(r"\s+")


def _extract_year(text: str, url: str) -> int | None:
    """Best-effort year: prefer an explicit 4-digit year, else venue+2-digit."""
    m = _YEAR_RE.search(text) or _YEAR_RE.search(url)
    if m:
        y = int(m.group())
        return y if 1900 <= y <= 2100 else None
    m = _VENUE_YEAR_RE.search(text) or _VENUE_YEAR_RE.search(url)
    if m:
        two = int(m.group(2))
        return 2000 + two if two < 70 else 1900 + two
    return None


def _clean(text: str) -> str:
    """Collapse whitespace and unescape HTML entities."""
    return _WS_RE.sub(" ", html.unescape(text or "")).strip()


class _AnchorParser(HTMLParser):
    """Collect ``(href, text)`` pairs for every ``<a>`` in the document."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.anchors: list[tuple[str, str]] = []
        self._href: str | None = None
        self._buf: list[str] = []

    def handle_starttag(self, tag, attrs):  # noqa: D102 - HTMLParser hook
        if tag == "a" and self._href is None:
            self._href = dict(attrs).get("href", "") or ""
            self._buf = []

    def handle_endtag(self, tag):  # noqa: D102 - HTMLParser hook
        if tag == "a" and self._href is not None:
            self.anchors.append((self._href, _clean("".join(self._buf))))
            self._href = None
            self._buf = []

    def handle_data(self, data):  # noqa: D102 - HTMLParser hook
        if self._href is not None:
            self._buf.append(data)


def fetch_html(url: str, timeout: int = WATCH_TIMEOUT) -> str:
    """Download ``url`` and return decoded text (never raises on bad charset)."""
    from urllib.request import Request, urlopen

    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        charset = resp.headers.get_content_charset() or "utf-8"
    try:
        return raw.decode(charset, errors="replace")
    except LookupError:
        return raw.decode("utf-8", errors="replace")


def _classify(href: str, text: str) -> tuple[str, float]:
    """Return ``(kind, confidence)`` for a candidate anchor."""
    low_href = href.lower()
    low_text = text.lower()
    fname = low_href.rsplit("/", 1)[-1]

    if any(h in low_href for h in _VIDEO_HINTS) or re.search(r"\bvideo\b", low_text):
        return "video", 0.9
    if "arxiv" in low_href or "arxiv" in low_text:
        return "paper", 0.85
    # Tech report: flagged in the anchor text, or encoded in the filename
    # (...-TR.pdf, ..._techreport.pdf, .../tr-2025-01.pdf).
    if any(h in low_text for h in _REPORT_HINTS) or re.search(
        r"[-_](tr|tech|techreport|report)\b|[-_]tr[-_.]|(^|[-_/])tr\d", fname
    ):
        return "report", 0.8
    if any(h in low_text for h in _TALK_HINTS):
        return "talk", 0.6
    if any(h in low_href for h in _PAPER_HINTS):
        return "paper", 0.8
    return "other", 0.4


def _title_from_href(href: str) -> str:
    """Derive a readable title from a filename-ish URL."""
    name = urllib.parse.unquote(href.rstrip("/").rsplit("/", 1)[-1])
    name = re.sub(r"\.(pdf|html?|pptx?|mp4)$", "", name, flags=re.I)
    name = name.replace("_", " ").replace("-", " ").replace("%20", " ")
    return _clean(name)


def _looks_like_title(text: str) -> bool:
    """A work title is reasonably long and has more than one word."""
    if len(text) < 12:
        return False
    return " " in text or "." in text


def parse_homepage(
    url: str,
    html_text: str | None = None,
    lookback_years: int = 2,
    min_confidence: float = 0.5,
) -> list[dict]:
    """Extract work items from a homepage.

    ``min_confidence`` (default 0.5) drops the long tail of homepage noise —
    affiliation logos, "research interests" blurbs, ``Abstract.md`` twins of a
    paper — that would otherwise generate false pushes. Lower it only if you
    would rather see everything and filter by hand.

    Returns a list of dicts with keys: ``title``, ``url``, ``kind``, ``year``,
    ``confidence``, ``source``. Never raises — network/parse failures yield ``[]``.
    """
    if html_text is None:
        try:
            html_text = fetch_html(url)
        except Exception:
            return []

    parser = _AnchorParser()
    try:
        parser.feed(html_text)
    except Exception:  # malformed HTML is the norm on personal pages
        pass

    cutoff_year = 0
    if lookback_years and lookback_years > 0:
        from datetime import datetime

        cutoff_year = datetime.now().year - lookback_years

    items: list[dict] = []
    seen: set[str] = set()

    for href, text in parser.anchors:
        if not href or href.startswith(("#", "mailto:", "javascript:", "tel:")):
            continue
        abs_url = urllib.parse.urljoin(url, href)
        # A bare site root is a logo/affiliation link, never a work.
        if not urllib.parse.urlparse(abs_url).path.strip("/"):
            continue

        title = text
        derived = False
        # Generic link labels carry no title; fall back to the filename.
        if _clean(text).lower().strip("[]() ") in _NAV_TEXT or not _looks_like_title(text):
            if not _looks_like_title(text):
                title = _title_from_href(href)
                derived = True
                if not _looks_like_title(title):
                    continue
            else:
                continue
        if _clean(title).lower() in _NAV_TEXT:
            continue

        kind, confidence = _classify(abs_url, text or title)
        if derived:
            confidence = max(0.3, confidence - 0.2)
        if confidence < min_confidence:
            continue

        year = _extract_year(text, abs_url)
        if year is not None and year < cutoff_year:
            continue

        key = re.sub(r"[^a-z0-9]+", "", title.lower())[:80]
        if not key or key in seen:
            continue
        seen.add(key)

        items.append(
            {
                "title": title,
                "url": abs_url,
                "kind": kind,
                "year": year,
                "venue": "",
                "authors": [],
                "abstract": "",
                "source": "homepage",
                "confidence": round(confidence, 2),
            }
        )

    return items
