"""FastAPI routes for Paper-Glean web interface."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse

from glean import __version__, notify
from glean.config import CATEGORIES
from glean.core import (
    apply_feedback,
    download_paper,
    find_paper,
    list_available_days,
    load_day_data,
    load_interest_entries,
)
from glean.ccf import (
    add_venue,
    load_events as load_ccf_events,
    load_venues,
    remove_venue,
    run as run_ccf,
    set_enabled as set_venue_enabled,
    set_enabled_area,
    sync_catalog,
)
from glean.watch import (
    add_researcher,
    load_events as load_watch_events,
    load_watchlist,
    remove_researcher,
    run as run_watch,
    set_enabled,
)
from glean.web.models import (
    CcfVenue,
    DayInfo,
    FeedbackRequest,
    InterestEntryResponse,
    PaperFilters,
    WatchResearcher,
)
from glean.web.templates_config import templates

router = APIRouter()

# One declaration of the six paper-filter query params, shared by the HTML page,
# the JSON API and the HTMX partial so their parameter lists cannot drift apart.
Filters = Annotated[PaperFilters, Depends()]


# ------------------------------------------------------------------
# HTML Pages
# ------------------------------------------------------------------

@router.get("/digest", response_class=HTMLResponse)
async def digest_page(request: Request, filters: Filters) -> HTMLResponse:
    """Main digest stream page."""
    days = list_available_days()
    current_day = filters.day or (days[0] if days else None)
    data = load_day_data(current_day) if current_day else None
    papers = data.get("papers", []) if data else []

    return templates.TemplateResponse(
        request,
        "digest.html",
        {
            "days": days,
            "current_day": current_day,
            "papers": _filter_papers(papers, filters),
            "categories": CATEGORIES,
            "interests": load_interest_entries(),
            "filter": filters,
        },
    )


@router.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request) -> HTMLResponse:
    """Interest profile page."""
    interests = load_interest_entries()
    star_entries = [e for e in interests if e["section"] == "star"]
    expand_entries = [e for e in interests if e["section"] == "expand"]

    return templates.TemplateResponse(
        request,
        "profile.html",
        {"star_entries": star_entries, "expand_entries": expand_entries},
    )


@router.get("/archive", response_class=HTMLResponse)
async def archive_page(request: Request) -> HTMLResponse:
    """Archive library page."""
    from glean.config import ARXIV_DIR

    pdfs = []
    if ARXIV_DIR.exists():
        pdfs = sorted(ARXIV_DIR.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True)

    return templates.TemplateResponse(
        request,
        "archive.html",
        {"pdfs": pdfs[:100]},  # Limit to recent 100
    )


# ------------------------------------------------------------------
# API Endpoints
# ------------------------------------------------------------------

@router.get("/api/ping")
async def api_ping() -> dict:
    """Liveness probe.

    Used by the daily scheduler (``arxiv-daily daily --serve``) and by
    ``glean.serve.ensure`` to decide whether the local web app is already
    online before spawning a new process. Keep this dependency-free and cheap.
    """
    return {
        "status": "ok",
        "service": "paper-glean",
        "version": __version__,
        "time": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/api/days")
async def api_days() -> list[DayInfo]:
    """List available days with paper counts."""
    result = []
    for day in list_available_days():
        data = load_day_data(day)
        count = len(data.get("papers", [])) if data else 0
        result.append(DayInfo(day=day, paper_count=count))
    return result


@router.get("/api/papers")
async def api_papers(
    filters: Filters,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> dict:
    """List papers with filtering and pagination."""
    days = list_available_days()
    current_day = filters.day or (days[0] if days else None)
    data = load_day_data(current_day) if current_day else None
    papers = data.get("papers", []) if data else []

    filtered = _filter_papers(papers, filters)

    return {
        "papers": filtered[offset : offset + limit],
        "total": len(filtered),
        "day": current_day,
        "limit": limit,
        "offset": offset,
    }


@router.get("/api/papers/{paper_id}")
async def api_paper_detail(paper_id: str) -> dict:
    """Get single paper detail."""
    paper, day = _require_paper(paper_id)
    return {"paper": paper, "day": day}


@router.get("/api/interests")
async def api_interests() -> list[InterestEntryResponse]:
    """Get interest profile entries."""
    return [InterestEntryResponse(**e) for e in load_interest_entries()]


@router.post("/api/feedback")
async def api_feedback(req: FeedbackRequest) -> dict:
    """Submit feedback for a paper."""
    paper, day = _require_paper(req.id)
    record = apply_feedback(paper, day, stars=req.stars, curiosity=req.curiosity)
    return {"success": True, "record": record}


@router.post("/api/download/{paper_id}")
async def api_download(paper_id: str) -> dict:
    """Download a paper PDF."""
    dest = download_paper(paper_id)
    if not dest:
        raise HTTPException(status_code=500, detail="Download failed")
    return {"success": True, "path": str(dest)}


# ------------------------------------------------------------------
# Watch (researcher monitoring) — pages
# ------------------------------------------------------------------

@router.get("/watch", response_class=HTMLResponse)
async def watch_page(request: Request) -> HTMLResponse:
    """Monitoring dashboard: who we watch + what's new."""
    return templates.TemplateResponse(
        request,
        "watch.html",
        {
            "researchers": load_watchlist(),
            "new_items": notify.load_new(),
            "events": load_watch_events(limit=30),
            "channels": notify.enabled_channels(),
        },
    )


# ------------------------------------------------------------------
# Watch — API
# ------------------------------------------------------------------

@router.get("/api/watch/researchers")
async def api_watch_researchers() -> list[WatchResearcher]:
    """List every monitored researcher (enabled and paused)."""
    return [WatchResearcher(**e) for e in load_watchlist()]


@router.post("/api/watch/researchers")
async def api_watch_add(
    name: str = Form(...),
    homepage: str = Form(""),
    dblp: str = Form(""),
    s2: str = Form(""),
    tags: str = Form(""),
) -> dict:
    """Add a researcher to watchlist.md (form-encoded; the page uses HTMX)."""
    tag_list = [t.strip() for t in tags.split(";") if t.strip()]
    try:
        entry = add_researcher(
            name, homepage or None, dblp or None, s2 or None, tag_list
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"success": True, "researcher": entry}


@router.delete("/api/watch/researchers/{key}")
async def api_watch_remove(key: str) -> dict:
    """Remove a researcher (and forget their seen-state)."""
    target = _require_entry(load_watchlist(), key, "researcher")
    return {"success": remove_researcher(target["name"])}


@router.post("/api/watch/researchers/{key}/toggle")
async def api_watch_toggle(key: str, enabled: bool = True) -> dict:
    """Pause / resume one researcher."""
    target = _require_entry(load_watchlist(), key, "researcher")
    return {"success": set_enabled(target["name"], enabled), "enabled": enabled}


@router.get("/api/watch/new")
async def api_watch_new() -> dict:
    """Unacknowledged new items — what the UI badges as NEW."""
    items = notify.load_new()
    return {"count": len(items), "items": items}


@router.post("/api/watch/ack")
async def api_watch_ack() -> dict:
    """Clear the NEW badges."""
    return {"success": True, "cleared": notify.ack_all()}


@router.get("/api/watch/events")
async def api_watch_events(limit: int = Query(50, ge=1, le=500)) -> list[dict]:
    """Push history, newest first."""
    return load_watch_events(limit=limit)


@router.post("/api/watch/run")
async def api_watch_run(only: str | None = None, force: bool = False) -> dict:
    """Trigger a scan. Runs in a worker thread — it does network I/O."""
    result = await asyncio.to_thread(
        run_watch, only, use_network=True, force=force, push=True
    )
    return _run_summary(result)


# ------------------------------------------------------------------
# CCF-A venue monitoring
# ------------------------------------------------------------------

@router.get("/ccf", response_class=HTMLResponse)
async def ccf_page(request: Request) -> HTMLResponse:
    """CCF-A venue dashboard: what is ticked, and what just changed."""
    return templates.TemplateResponse(
        request,
        "ccf.html",
        {
            "venues": load_venues(),
            "new_items": notify.load_new("ccf"),
            "events": load_ccf_events(limit=30),
            "channels": notify.enabled_channels(),
        },
    )


@router.get("/api/ccf/venues")
async def api_ccf_venues(
    area: str | None = None,
    enabled: bool | None = None,
) -> list[CcfVenue]:
    """List monitored venues, optionally filtered by area / tick state."""
    rows = load_venues()
    if area:
        needle = area.lower()
        rows = [v for v in rows if needle in (v.get("area") or "").lower()]
    if enabled is not None:
        rows = [v for v in rows if bool(v.get("enabled", True)) is enabled]
    return [CcfVenue(**v) for v in rows]


@router.post("/api/ccf/venues")
async def api_ccf_add(
    name: str = Form(...),
    homepage: str = Form(...),
    kind: str = Form("conference"),
    full: str = Form(""),
    area: str = Form(""),
    dblp: str = Form(""),
    ccf: str = Form("A"),
    issn: str = Form(""),
) -> dict:
    """Add a venue the built-in catalogue does not cover."""
    try:
        entry = add_venue(
            name,
            kind="journal" if kind == "journal" else "conference",
            full=full,
            area=area,
            homepage=homepage,
            dblp=dblp,
            ccf=ccf,
            issn=issn,
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"success": True, "venue": entry}


@router.delete("/api/ccf/venues/{key}")
async def api_ccf_remove(key: str) -> dict:
    """Remove a venue (and forget its seen-state)."""
    target = _require_entry(load_venues(), key, "venue")
    return {"success": remove_venue(target["name"])}


@router.post("/api/ccf/venues/{key}/toggle")
async def api_ccf_toggle(key: str, enabled: bool = True) -> dict:
    """Tick / untick one venue."""
    target = _require_entry(load_venues(), key, "venue")
    set_venue_enabled(target["name"], enabled)
    return {"success": True, "enabled": enabled}


@router.post("/api/ccf/venues/toggle-area")
async def api_ccf_toggle_area(area: str = Form(...), enabled: bool = Form(True)) -> dict:
    """Bulk tick / untick a whole CCF area (the list is long — bulk matters)."""
    touched = set_enabled_area(area, enabled)
    return {"success": True, "area": area, "enabled": enabled, "count": len(touched),
            "names": touched}


@router.post("/api/ccf/refresh")
async def api_ccf_refresh(default_enabled: bool = True) -> dict:
    """Re-merge the built-in catalogue into ccf.md, keeping current ticks."""
    added, updated = sync_catalog(default_enabled=default_enabled)
    return {"success": True, "added": added, "updated": updated}


@router.get("/api/ccf/new")
async def api_ccf_new() -> dict:
    """Unacknowledged CCF updates — what the UI badges as NEW."""
    items = notify.load_new("ccf")
    return {"count": len(items), "items": items}


@router.post("/api/ccf/ack")
async def api_ccf_ack() -> dict:
    """Clear the CCF NEW badges (does not touch the researcher ones)."""
    return {"success": True, "cleared": notify.ack_all("ccf")}


@router.get("/api/ccf/events")
async def api_ccf_events(limit: int = Query(50, ge=1, le=500)) -> list[dict]:
    """Push history, newest first."""
    return load_ccf_events(limit=limit)


@router.post("/api/ccf/run")
async def api_ccf_run(only: str | None = None, force: bool = False) -> dict:
    """Trigger a CCF scan. Runs in a worker thread — it does network I/O."""
    result = await asyncio.to_thread(
        run_ccf, only, use_network=True, force=force, push=True
    )
    return _run_summary(result)


# ------------------------------------------------------------------
# HTMX Partials
# ------------------------------------------------------------------

@router.get("/htmx/paper-card/{paper_id}", response_class=HTMLResponse)
async def htmx_paper_card(request: Request, paper_id: str) -> HTMLResponse:
    """HTMX partial: single paper card."""
    paper, _ = _require_paper(paper_id)
    return templates.TemplateResponse(
        request,
        "partials/paper_card.html",
        {"paper": paper, "interests": load_interest_entries()},
    )


@router.get("/htmx/paper-detail/{paper_id}", response_class=HTMLResponse)
async def htmx_paper_detail(request: Request, paper_id: str) -> HTMLResponse:
    """HTMX partial: paper detail panel."""
    paper, day = _require_paper(paper_id)
    return templates.TemplateResponse(
        request,
        "partials/paper_detail.html",
        {"paper": paper, "day": day},
    )


@router.get("/htmx/paper-list", response_class=HTMLResponse)
async def htmx_paper_list(request: Request, filters: Filters) -> HTMLResponse:
    """HTMX partial: filtered paper list."""
    days = list_available_days()
    current_day = filters.day or (days[0] if days else None)
    data = load_day_data(current_day) if current_day else None
    papers = data.get("papers", []) if data else []

    return templates.TemplateResponse(
        request,
        "partials/paper_list.html",
        {
            "papers": _filter_papers(papers, filters),
            "interests": load_interest_entries(),
            "current_day": current_day,
        },
    )


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _require_paper(paper_id: str) -> tuple[dict, str | None]:
    """Look a paper up by id, or answer 404."""
    paper, day = find_paper(paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper, day


def _require_entry(rows: list[dict], key: str, what: str) -> dict:
    """Pick the entry whose ``key`` matches, or answer 404.

    ``rows`` is a freshly loaded watchlist / venue list; the caller then mutates
    by *name* because that is what the markdown writers key on.
    """
    target = next((r for r in rows if r["key"] == key), None)
    if target is None:
        raise HTTPException(status_code=404, detail=f"{what} not found")
    return target


def _run_summary(result: dict) -> dict:
    """Shape a monitor run result for the JSON API: counts, never payloads."""
    return {
        "run_id": result["run_id"],
        "new_count": len(result["new_items"]),
        "grouped": {k: len(v) for k, v in result["grouped"].items()},
        "baselined": result["baselined"],
        "errors": result["errors"],
        "pushed_to": result["pushed_to"],
    }


def _hit_visible(paper: dict, filters: PaperFilters) -> bool:
    """Should this paper survive the star / expand / other checkboxes?

    A paper is ranked by its strongest hit: starring wins over expanding, and a
    paper with no hits at all is only shown when "Other" is ticked.
    """
    if paper.get("hits_star"):
        return filters.show_star
    if paper.get("hits_expand"):
        return filters.show_expand
    return filters.show_other


def _filter_papers(papers: list[dict], filters: PaperFilters) -> list[dict]:
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

    result = [p for p in result if _hit_visible(p, filters)]

    # Sort by score (star + expand) descending
    return sorted(result, key=lambda p: -(p.get("score_star", 0) + p.get("score_expand", 0)))
