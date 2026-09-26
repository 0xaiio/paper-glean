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


# --- The contract shared by both monitoring surfaces (watch / ccf) -----------
#
# These three are typed because they are the *only* payloads produced by the
# shared monitoring kernel: if `watch` and `ccf` answered `/new`, `/ack` or
# `/run` with different shapes, the two front-ends would have to duplicate
# code again. Declaring them once keeps that from happening.

class RunSummary(BaseModel):
    """What a monitor run reports: counts, never payloads."""

    run_id: str
    new_count: int
    grouped: dict[str, int]
    baselined: list[str]
    errors: list[str]
    pushed_to: list[str]


class NewItems(BaseModel):
    """Unacknowledged items — what the UI badges as NEW."""

    count: int
    items: list[dict]


class AckResult(BaseModel):
    """Result of clearing the NEW badges."""

    success: bool
    cleared: int
