"""FastAPI routes for Paper-Glean web interface."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Form, HTTPException, Query, Request
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
    WatchResearcher,
)
from glean.web.templates_config import templates

router = APIRouter()


# ------------------------------------------------------------------
# HTML Pages
# ------------------------------------------------------------------

@router.get("/digest", response_class=HTMLResponse)
async def digest_page(
    request: Request,
    day: str | None = None,
    category: str | None = None,
    search: str | None = None,
    show_star: bool = True,
    show_expand: bool = True,
    show_other: bool = False,
) -> HTMLResponse:
    """Main digest stream page."""
    days = list_available_days()
    if not days:
        return templates.TemplateResponse(
            "digest.html",
            {
                "request": request,
                "days": [],
                "current_day": None,
                "papers": [],
                "categories": CATEGORIES,
                "interests": [],
                "filter": {
                    "day": day,
                    "category": category,
                    "search": search,
                    "show_star": show_star,
                    "show_expand": show_expand,
                    "show_other": show_other,
                },
            },
        )

    current_day = day or days[0]
    data = load_day_data(current_day)
    papers = data.get("papers", []) if data else []
    interests = load_interest_entries()

    # Apply filters
    filtered = _filter_papers(papers, category, search, show_star, show_expand, show_other)

    return templates.TemplateResponse(
        "digest.html",
        {
            "request": request,
            "days": days,
            "current_day": current_day,
            "papers": filtered,
            "categories": CATEGORIES,
            "interests": interests,
            "filter": {
                "day": day,
                "category": category,
                "search": search,
                "show_star": show_star,
                "show_expand": show_expand,
                "show_other": show_other,
            },
        },
    )


@router.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request) -> HTMLResponse:
    """Interest profile page."""
    interests = load_interest_entries()
    star_entries = [e for e in interests if e["section"] == "star"]
    expand_entries = [e for e in interests if e["section"] == "expand"]

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "star_entries": star_entries,
            "expand_entries": expand_entries,
        },
    )


@router.get("/archive", response_class=HTMLResponse)
async def archive_page(request: Request) -> HTMLResponse:
    """Archive library page."""
    from glean.config import ARXIV_DIR

    pdfs = []
    if ARXIV_DIR.exists():
        pdfs = sorted(ARXIV_DIR.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True)

    return templates.TemplateResponse(
        "archive.html",
        {
            "request": request,
            "pdfs": pdfs[:100],  # Limit to recent 100
        },
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
    days = list_available_days()
    result = []
    for day in days:
        data = load_day_data(day)
        count = len(data.get("papers", [])) if data else 0
        result.append(DayInfo(day=day, paper_count=count))
    return result


@router.get("/api/papers")
async def api_papers(
    day: str | None = None,
    category: str | None = None,
    search: str | None = None,
    show_star: bool = True,
    show_expand: bool = True,
    show_other: bool = False,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> dict:
    """List papers with filtering and pagination."""
    days = list_available_days()
    if not days:
        return {"papers": [], "total": 0, "day": None}

    current_day = day or days[0]
    data = load_day_data(current_day)
    papers = data.get("papers", []) if data else []

    filtered = _filter_papers(papers, category, search, show_star, show_expand, show_other)
    total = len(filtered)
    paginated = filtered[offset : offset + limit]

    return {
        "papers": paginated,
        "total": total,
        "day": current_day,
        "limit": limit,
        "offset": offset,
    }


@router.get("/api/papers/{paper_id}")
async def api_paper_detail(paper_id: str) -> dict:
    """Get single paper detail."""
    paper, day = find_paper(paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return {"paper": paper, "day": day}


@router.get("/api/interests")
async def api_interests() -> list[InterestEntryResponse]:
    """Get interest profile entries."""
    entries = load_interest_entries()
    return [InterestEntryResponse(**e) for e in entries]


@router.post("/api/feedback")
async def api_feedback(req: FeedbackRequest) -> dict:
    """Submit feedback for a paper."""
    paper, day = find_paper(req.id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

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
    entries = load_watchlist()
    new_items = notify.load_new()
    events = load_watch_events(limit=30)
    return templates.TemplateResponse(
        "watch.html",
        {
            "request": request,
            "researchers": entries,
            "new_items": new_items,
            "events": events,
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
    entries = load_watchlist()
    target = next((e for e in entries if e["key"] == key), None)
    if target is None:
        raise HTTPException(status_code=404, detail="not found")
    return {"success": remove_researcher(target["name"])}


@router.post("/api/watch/researchers/{key}/toggle")
async def api_watch_toggle(key: str, enabled: bool = True) -> dict:
    """Pause / resume one researcher."""
    entries = load_watchlist()
    target = next((e for e in entries if e["key"] == key), None)
    if target is None:
        raise HTTPException(status_code=404, detail="not found")
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
    import asyncio

    result = await asyncio.to_thread(
        run_watch, only, **{"use_network": True, "force": force, "push": True}
    )
    return {
        "run_id": result["run_id"],
        "new_count": len(result["new_items"]),
        "grouped": {k: len(v) for k, v in result["grouped"].items()},
        "baselined": result["baselined"],
        "errors": result["errors"],
        "pushed_to": result["pushed_to"],
    }


# ------------------------------------------------------------------
# CCF-A venue monitoring
# ------------------------------------------------------------------

@router.get("/ccf", response_class=HTMLResponse)
async def ccf_page(request: Request) -> HTMLResponse:
    """CCF-A venue dashboard: what is ticked, and what just changed."""
    venues = load_venues()
    return templates.TemplateResponse(
        "ccf.html",
        {
            "request": request,
            "venues": venues,
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
    target = next((v for v in load_venues() if v["key"] == key), None)
    if target is None:
        raise HTTPException(status_code=404, detail="not found")
    return {"success": remove_venue(target["name"])}


@router.post("/api/ccf/venues/{key}/toggle")
async def api_ccf_toggle(key: str, enabled: bool = True) -> dict:
    """Tick / untick one venue."""
    target = next((v for v in load_venues() if v["key"] == key), None)
    if target is None:
        raise HTTPException(status_code=404, detail="not found")
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
    import asyncio

    result = await asyncio.to_thread(
        run_ccf, only, **{"use_network": True, "force": force, "push": True}
    )
    return {
        "run_id": result["run_id"],
        "new_count": len(result["new_items"]),
        "grouped": {k: len(v) for k, v in result["grouped"].items()},
        "baselined": result["baselined"],
        "errors": result["errors"],
        "pushed_to": result["pushed_to"],
    }


# ------------------------------------------------------------------
# HTMX Partials
# ------------------------------------------------------------------

@router.get("/htmx/paper-card/{paper_id}", response_class=HTMLResponse)
async def htmx_paper_card(request: Request, paper_id: str) -> HTMLResponse:
    """HTMX partial: single paper card."""
    paper, _ = find_paper(paper_id)
    if not paper:
        raise HTTPException(status_code=404)
    interests = load_interest_entries()
    return templates.TemplateResponse(
        "partials/paper_card.html",
        {"request": request, "paper": paper, "interests": interests},
    )


@router.get("/htmx/paper-detail/{paper_id}", response_class=HTMLResponse)
async def htmx_paper_detail(request: Request, paper_id: str) -> HTMLResponse:
    """HTMX partial: paper detail panel."""
    paper, day = find_paper(paper_id)
    if not paper:
        raise HTTPException(status_code=404)
    interests = load_interest_entries()
    return templates.TemplateResponse(
        "partials/paper_detail.html",
        {"request": request, "paper": paper, "day": day, "interests": interests},
    )


@router.get("/htmx/paper-list", response_class=HTMLResponse)
async def htmx_paper_list(
    request: Request,
    day: str | None = None,
    category: str | None = None,
    search: str | None = None,
    show_star: bool = True,
    show_expand: bool = True,
    show_other: bool = False,
) -> HTMLResponse:
    """HTMX partial: filtered paper list."""
    days = list_available_days()
    current_day = day or (days[0] if days else None)
    data = load_day_data(current_day) if current_day else None
    papers = data.get("papers", []) if data else []
    interests = load_interest_entries()

    filtered = _filter_papers(papers, category, search, show_star, show_expand, show_other)

    return templates.TemplateResponse(
        "partials/paper_list.html",
        {
            "request": request,
            "papers": filtered,
            "interests": interests,
            "current_day": current_day,
        },
    )


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _filter_papers(
    papers: list[dict],
    category: str | None,
    search: str | None,
    show_star: bool,
    show_expand: bool,
    show_other: bool,
) -> list[dict]:
    """Filter papers by category, search, and hit type."""
    result = papers

    # Category filter
    if category:
        result = [p for p in result if p.get("primary") == category or category in p.get("categories", [])]

    # Search filter (case-insensitive in title/abstract)
    if search:
        search_lower = search.lower()
        result = [
            p
            for p in result
            if search_lower in p.get("title", "").lower()
            or search_lower in p.get("abstract", "").lower()
        ]

    # Hit type filter
    if not show_star or not show_expand or not show_other:
        filtered = []
        for p in result:
            has_star = bool(p.get("hits_star"))
            has_expand = bool(p.get("hits_expand"))
            is_other = not has_star and not has_expand

            if show_star and has_star:
                filtered.append(p)
            elif show_expand and has_expand and not has_star:
                filtered.append(p)
            elif show_other and is_other:
                filtered.append(p)
        result = filtered

    # Sort by score (star + expand) descending
    result = sorted(result, key=lambda p: -(p.get("score_star", 0) + p.get("score_expand", 0)))

    return result
