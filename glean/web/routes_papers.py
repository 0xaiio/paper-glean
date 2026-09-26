"""Routes for the paper stream: digest page, profile, archive and their APIs."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import HTMLResponse

from glean import __version__, config
from glean.core import (
    apply_feedback,
    download_paper,
    list_available_days,
    load_day_data,
    load_interest_entries,
)
from glean.web.common import Filters, current_papers, filter_papers, require_paper
from glean.web.models import (
    DayInfo,
    FeedbackRequest,
    InterestEntryResponse,
)
from glean.web.templates_config import templates

router = APIRouter(tags=["papers"])


# ------------------------------------------------------------------
# HTML Pages
# ------------------------------------------------------------------

@router.get("/digest", response_class=HTMLResponse)
async def digest_page(request: Request, filters: Filters) -> HTMLResponse:
    """Main digest stream page."""
    current_day, papers = current_papers(filters)

    return templates.TemplateResponse(
        request,
        "digest.html",
        {
            "days": list_available_days(),
            "current_day": current_day,
            "papers": filter_papers(papers, filters),
            "categories": config.CATEGORIES,
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
    pdfs = []
    # Read the path off the module (not a from-import) so it is resolved when
    # the request arrives — the download directory can be redirected per run.
    if config.ARXIV_DIR.exists():
        pdfs = sorted(
            config.ARXIV_DIR.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True
        )

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
    current_day, papers = current_papers(filters)
    filtered = filter_papers(papers, filters)

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
    paper, day = require_paper(paper_id)
    return {"paper": paper, "day": day}


@router.get("/api/interests")
async def api_interests() -> list[InterestEntryResponse]:
    """Get interest profile entries."""
    return [InterestEntryResponse(**e) for e in load_interest_entries()]


@router.post("/api/feedback")
async def api_feedback(req: FeedbackRequest) -> dict:
    """Submit feedback for a paper."""
    paper, day = require_paper(req.id)
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
# HTMX Partials
# ------------------------------------------------------------------

@router.get("/htmx/paper-card/{paper_id}", response_class=HTMLResponse)
async def htmx_paper_card(request: Request, paper_id: str) -> HTMLResponse:
    """HTMX partial: single paper card."""
    paper, _ = require_paper(paper_id)
    return templates.TemplateResponse(
        request,
        "partials/paper_card.html",
        {"paper": paper, "interests": load_interest_entries()},
    )


@router.get("/htmx/paper-detail/{paper_id}", response_class=HTMLResponse)
async def htmx_paper_detail(request: Request, paper_id: str) -> HTMLResponse:
    """HTMX partial: paper detail panel."""
    paper, day = require_paper(paper_id)
    return templates.TemplateResponse(
        request,
        "partials/paper_detail.html",
        {"paper": paper, "day": day},
    )


@router.get("/htmx/paper-list", response_class=HTMLResponse)
async def htmx_paper_list(request: Request, filters: Filters) -> HTMLResponse:
    """HTMX partial: filtered paper list."""
    current_day, papers = current_papers(filters)

    return templates.TemplateResponse(
        request,
        "partials/paper_list.html",
        {
            "papers": filter_papers(papers, filters),
            "interests": load_interest_entries(),
            "current_day": current_day,
        },
    )
