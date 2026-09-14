"""Shared Jinja2 template environment for the Paper-Glean web interface."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from fastapi.templating import Jinja2Templates

# Starlette's Jinja2Templates already builds the environment this project needs:
# a FileSystemLoader over the template directory plus HTML autoescaping
# (``jinja2.select_autoescape()``), and ``TemplateResponse`` injects ``request``
# into the context itself.
#
# Historical note: an earlier revision subclassed it as ``NoCacheJinja2Templates``
# to dodge a Starlette bug that hashed the render context into the template cache
# key (``TypeError: unhashable type: 'dict'``) and had to import the private
# ``starlette.templating._TemplateResponse``. Starlette now resolves the template
# by name only, so the workaround — and that private dependency — is gone.
templates_dir = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))


def format_timestamp(ts: float) -> str:
    """Render a Unix timestamp as ``YYYY-MM-DD HH:MM`` in local time."""
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")


templates.env.filters["format_timestamp"] = format_timestamp
