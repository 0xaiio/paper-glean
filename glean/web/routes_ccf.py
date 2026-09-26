"""Routes for CCF-A venue monitoring (the ``ccf`` namespace)."""

from __future__ import annotations

import asyncio

from fastapi import APIRouter, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse

from glean import notify
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
from glean.web.common import require_entry, run_summary
from glean.web.models import AckResult, CcfVenue, NewItems, RunSummary
from glean.web.templates_config import templates

router = APIRouter(tags=["ccf"])


# ------------------------------------------------------------------
# Page
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


# ------------------------------------------------------------------
# API
# ------------------------------------------------------------------

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
    target = require_entry(load_venues(), key, "venue")
    return {"success": remove_venue(target["name"])}


@router.post("/api/ccf/venues/{key}/toggle")
async def api_ccf_toggle(key: str, enabled: bool = True) -> dict:
    """Tick / untick one venue."""
    target = require_entry(load_venues(), key, "venue")
    return {"success": set_venue_enabled(target["name"], enabled), "enabled": enabled}


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
async def api_ccf_new() -> NewItems:
    """Unacknowledged CCF updates — what the UI badges as NEW."""
    items = notify.load_new("ccf")
    return NewItems(count=len(items), items=items)


@router.post("/api/ccf/ack")
async def api_ccf_ack() -> AckResult:
    """Clear the CCF NEW badges (does not touch the researcher ones)."""
    return AckResult(success=True, cleared=notify.ack_all("ccf"))


@router.get("/api/ccf/events")
async def api_ccf_events(limit: int = Query(50, ge=1, le=500)) -> list[dict]:
    """Push history, newest first."""
    return load_ccf_events(limit=limit)


@router.post("/api/ccf/run")
async def api_ccf_run(only: str | None = None, force: bool = False) -> RunSummary:
    """Trigger a CCF scan. Runs in a worker thread — it does network I/O."""
    result = await asyncio.to_thread(
        run_ccf, only, use_network=True, force=force, push=True
    )
    return run_summary(result)
