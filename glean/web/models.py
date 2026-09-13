"""Pydantic models for the web API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PaperResponse(BaseModel):
    """Paper data for API responses."""

    id: str
    title: str
    authors: list[str]
    abstract: str
    primary: str
    categories: list[str]
    published: str
    abs_url: str
    pdf_url: str
    hits_star: list[str] = Field(default_factory=list)
    hits_expand: list[str] = Field(default_factory=list)
    score_star: int = 0
    score_expand: int = 0


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


class FilterState(BaseModel):
    """Current filter state."""

    day: str | None = None
    category: str | None = None
    search: str | None = None
    show_star: bool = True
    show_expand: bool = True
    show_other: bool = False


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
