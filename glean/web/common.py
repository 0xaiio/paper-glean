"""Building blocks shared by every route module (papers / watch / ccf).

These live apart from the routes so the three surfaces cannot drift: one way to
resolve "which day", one way to answer 404, one way to filter, one shape for a
monitor run.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException

from glean.core import find_paper, list_available_days, load_day_data
from glean.web.models import PaperFilters, RunSummary

# One declaration of the six paper-filter query params, shared by the HTML page,
# the JSON API and the HTMX partial so their parameter lists cannot drift apart.
Filters = Annotated[PaperFilters, Depends()]


def current_papers(filters: PaperFilters) -> tuple[str | None, list[dict]]:
    """Resolve which day a request is about, and return that day's papers.

    Every paper listing — page, JSON API and HTMX partial — starts here, so
    "which day do we show when none is asked for" has exactly one answer: the
    newest day that has data at all.
    """
    days = list_available_days()
    day = filters.day or (days[0] if days else None)
    data = load_day_data(day) if day else None
    return day, (data.get("papers", []) if data else [])


def require_paper(paper_id: str) -> tuple[dict, str | None]:
    """Look a paper up by id, or answer 404."""
    paper, day = find_paper(paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper, day


def require_entry(rows: list[dict], key: str, what: str) -> dict:
    """Pick the entry whose ``key`` matches, or answer 404.

    ``rows`` is a freshly loaded watchlist / venue list; the caller then mutates
    by *name* because that is what the markdown writers key on.
    """
    target = next((r for r in rows if r["key"] == key), None)
    if target is None:
        raise HTTPException(status_code=404, detail=f"{what} not found")
    return target


def run_summary(result: dict) -> RunSummary:
    """Shape a monitor run result for the JSON API: counts, never payloads."""
    return RunSummary(
        run_id=result["run_id"],
        new_count=len(result["new_items"]),
        grouped={k: len(v) for k, v in result["grouped"].items()},
        baselined=result["baselined"],
        errors=result["errors"],
        pushed_to=result["pushed_to"],
    )


def hit_visible(paper: dict, filters: PaperFilters) -> bool:
    """Should this paper survive the star / expand / other checkboxes?

    A paper is ranked by its strongest hit: starring wins over expanding, and a
    paper with no hits at all is only shown when "Other" is ticked.
    """
    if paper.get("hits_star"):
        return filters.show_star
    if paper.get("hits_expand"):
        return filters.show_expand
    return filters.show_other


def filter_papers(papers: list[dict], filters: PaperFilters) -> list[dict]:
    """Apply category / search / hit-type filters, then rank by score."""
    result = papers

    if filters.category:
        result = [
            p
            for p in result
            if p.get("primary") == filters.category
            or filters.category in p.get("categories", [])
        ]

    if filters.search:
        needle = filters.search.lower()
        result = [
            p
            for p in result
            if needle in p.get("title", "").lower()
            or needle in p.get("abstract", "").lower()
        ]

    result = [p for p in result if hit_visible(p, filters)]

    # Sort by score (star + expand) descending
    return sorted(result, key=lambda p: -(p.get("score_star", 0) + p.get("score_expand", 0)))
