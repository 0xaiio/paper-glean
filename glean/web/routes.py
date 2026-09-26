"""Route aggregation — the single router ``create_app`` includes.

One module per surface (papers / watch / ccf / ...). Adding a surface means
writing its route module and adding one line here; nothing else has to grow.

Paths, operation ids and response shapes are unchanged by the split: the
sub-routers are mounted without a prefix.
"""

from __future__ import annotations

from fastapi import APIRouter

from glean.web.routes_ccf import router as ccf_router
from glean.web.routes_papers import router as papers_router
from glean.web.routes_watch import router as watch_router

router = APIRouter()
router.include_router(papers_router)
router.include_router(watch_router)
router.include_router(ccf_router)

__all__ = ["router"]
