"""Shared template configuration for Paper-Glean web interface."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from starlette.templating import _TemplateResponse


class NoCacheJinja2Templates(Jinja2Templates):
    """Custom Jinja2Templates that avoids caching issues with unhashable dict objects.

    The default starlette Jinja2Templates passes template context as 'globals' to
    jinja2.get_template(), which uses it as part of the cache key. When context
    contains dict objects (like paper data), this causes TypeError: unhashable type.

    This implementation overrides TemplateResponse to not pass globals to get_template.
    """

    def __init__(self, directory: str) -> None:
        self.env = Environment(
            loader=FileSystemLoader(directory),
            autoescape=True,
        )

    def TemplateResponse(
        self,
        name: str,
        context: dict,
        status_code: int = 200,
        headers: dict | None = None,
        media_type: str | None = None,
        background=None,
    ) -> _TemplateResponse:
        """Render a template with the given context."""
        # Don't pass context as globals - just get the template by name
        template = self.env.get_template(name)
        return _TemplateResponse(
            template,
            context,
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )


# Shared templates instance
templates_dir = Path(__file__).resolve().parent.parent / "templates"
templates = NoCacheJinja2Templates(directory=str(templates_dir))

# Add custom filters
def format_timestamp(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")

templates.env.filters["format_timestamp"] = format_timestamp
