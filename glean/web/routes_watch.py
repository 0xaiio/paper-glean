"""Routes for researcher monitoring (the ``watch`` namespace)."""

from __future__ import annotations

import asyncio

from fastapi import APIRouter, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse

from glean import notify
from glean.resolve import resolve
from glean.watch import (
    add_researcher,
    load_events as load_watch_events,
    load_watchlist,
    remove_researcher,
    run as run_watch,
    set_enabled,
)
from glean.web.common import require_entry, run_summary
from glean.web.models import (
    AckResult,
    NewItems,
    ResolveResult,
    RunSummary,
    WatchResearcher,
)
from glean.web.templates_config import templates

router = APIRouter(tags=["watch"])


# ------------------------------------------------------------------
# Page
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
# API
# ------------------------------------------------------------------

@router.get("/api/watch/researchers")
async def api_watch_researchers() -> list[WatchResearcher]:
    """List every monitored researcher (enabled and paused)."""
    return [WatchResearcher(**e) for e in load_watchlist()]


@router.post("/api/watch/researchers")
async def api_watch_add(
    name: str = Form(""),
    homepage: str = Form(""),
    dblp: str = Form(""),
    s2: str = Form(""),
    tags: str = Form(""),
) -> dict:
    """Add a researcher to watchlist.md (form-encoded; the page uses HTMX).

    ``name`` is optional: when it is blank we ask :mod:`glean.resolve` who the
    other sources belong to. Only the *name* is taken from that proposal — an
    inferred DBLP id or S2 id is never written silently, because a wrong id
    would quietly point future scans at the wrong publication list. Use the
    「解析监控对象」 button first if you want the ids filled in for review.
    """
    tag_list = [t.strip() for t in tags.split(";") if t.strip()]
    resolved_name = ""
    if not name.strip():
        if not any(v.strip() for v in (homepage, dblp, s2)):
            raise HTTPException(
                status_code=400,
                detail="姓名为空时，至少还要给一项：个人主页 / DBLP / Semantic Scholar id",
            )
        info = await asyncio.to_thread(resolve, name, homepage, dblp, s2)
        resolved_name = (info.get("resolved") or {}).get("name") or ""
        if not resolved_name:
            raise HTTPException(
                status_code=400,
                detail="无法从所填信息推断出姓名，请补一个姓名（或先点「解析监控对象」核对）",
            )
        name = resolved_name
    try:
        entry = add_researcher(
            name, homepage or None, dblp or None, s2 or None, tag_list
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"success": True, "researcher": entry, "resolved_name": resolved_name}


@router.post("/api/watch/resolve")
async def api_watch_resolve(
    name: str = Form(""),
    homepage: str = Form(""),
    dblp: str = Form(""),
    s2: str = Form(""),
) -> ResolveResult:
    """Propose a full identity from any one of the four inputs.

    Network I/O (homepage fetch + Semantic Scholar), so it runs in a worker
    thread. Nothing is written — the answer is a proposal the user reviews.
    """
    if not any(v.strip() for v in (name, homepage, dblp, s2)):
        raise HTTPException(
            status_code=400,
            detail="请至少填写一项：姓名 / 个人主页 / DBLP / Semantic Scholar",
        )
    info = await asyncio.to_thread(resolve, name, homepage, dblp, s2)
    return ResolveResult(**info)


@router.delete("/api/watch/researchers/{key}")
async def api_watch_remove(key: str) -> dict:
    """Remove a researcher (and forget their seen-state)."""
    target = require_entry(load_watchlist(), key, "researcher")
    return {"success": remove_researcher(target["name"])}


@router.post("/api/watch/researchers/{key}/toggle")
async def api_watch_toggle(key: str, enabled: bool = True) -> dict:
    """Pause / resume one researcher."""
    target = require_entry(load_watchlist(), key, "researcher")
    return {"success": set_enabled(target["name"], enabled), "enabled": enabled}


@router.get("/api/watch/new")
async def api_watch_new() -> NewItems:
    """Unacknowledged new items — what the UI badges as NEW."""
    items = notify.load_new()
    return NewItems(count=len(items), items=items)


@router.post("/api/watch/ack")
async def api_watch_ack() -> AckResult:
    """Clear the NEW badges."""
    return AckResult(success=True, cleared=notify.ack_all())


@router.get("/api/watch/events")
async def api_watch_events(limit: int = Query(50, ge=1, le=500)) -> list[dict]:
    """Push history, newest first."""
    return load_watch_events(limit=limit)


@router.post("/api/watch/run")
async def api_watch_run(only: str | None = None, force: bool = False) -> RunSummary:
    """Trigger a scan. Runs in a worker thread — it does network I/O."""
    result = await asyncio.to_thread(
        run_watch, only, use_network=True, force=force, push=True
    )
    return run_summary(result)
