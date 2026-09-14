"""FastAPI application factory for Paper-Glean web interface."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from glean import __version__, notify
from glean.web.routes import router
from glean.web.templates_config import templates


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Paper-Glean",
        description="A personal, local-first paper recommendation workbench",
        version=__version__,
    )

    # Template global: how many unread monitored items (nav badge).
    templates.env.globals["watch_new_count"] = lambda: len(notify.load_new("watch"))
    templates.env.globals["ccf_new_count"] = lambda: len(notify.load_new("ccf"))

    # Static files
    static_dir = Path(__file__).resolve().parent.parent.parent / "glean_static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # Include API routes
    app.include_router(router)

    @app.get("/", response_class=HTMLResponse)
    async def root(request: Request) -> HTMLResponse:
        """Redirect to digest page."""
        return templates.TemplateResponse(
            request,
            "redirect.html",
            {"target": "/digest"},
        )

    return app


app = create_app()
