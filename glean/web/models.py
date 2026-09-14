"""Models for the web API: wire schemas (Pydantic) plus shared query groups."""

from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel, Field


@dataclass
class PaperFilters:
    """The query-string filter group shared by every paper listing.

    ``/digest``, ``/api/papers`` and ``/htmx/paper-list`` all accept exactly
    these six parameters and all feed them to the same filter function, so the
    group is declared once here and injected with ``Depends()``.  A plain
    dataclass (not a Pydantic model) is what lets FastAPI read each field from
    the query string rather than from a request body.
    """

    day: str | None = None
    category: str | None = None
    search: str | None = None
    show_star: bool = True
    show_expand: bool = True
    show_other: bool = False


class FeedbackRequest(BaseModel):
    """Feedback submission request."""

    id: str
    stars: int | None = Field(None, ge=0, le=5)
    curiosity: int | None = Field(None, ge=0, le=5)


class InterestEntryResponse(BaseModel):
    """Interest profile entry."""

    section: str
    title: str
    keywords: list[str]
    weight: int


class DayInfo(BaseModel):
    """Available day info."""

    day: str
    paper_count: int


class CcfVenue(BaseModel):
    """One monitored CCF venue (mirrors a ccf.md entry)."""

    key: str
    name: str
    kind: str = "conference"
    full: str = ""
    area: str = ""
    homepage: str = ""
    dblp: str = ""
    ccf: str = "A"
    issn: str = ""
    enabled: bool = True


class WatchResearcher(BaseModel):
    """One monitored researcher (mirrors a watchlist.md entry)."""

    key: str
    name: str
    homepage: str | None = None
    dblp: str | None = None
    s2: str | None = None
    tags: list[str] = Field(default_factory=list)
    enabled: bool = True
    note: str = ""
