"""
API v1 – Traffic analytics router.

Provides segment vehicle counts, 15-minute congestion estimates, and corridor summaries.
"""

from __future__ import annotations

from fastapi import APIRouter

from backend.analytics.store import store
from backend.schemas import CorridorTrafficSummary

router = APIRouter(prefix="/traffic", tags=["traffic"])


@router.get(
    "/",
    response_model=CorridorTrafficSummary,
    summary="Get corridor traffic summary and heatmap segments",
)
async def get_traffic() -> CorridorTrafficSummary:
    """Return aggregated corridor volumes, time-series, and 15-minute segment heat metrics."""
    return store.get_traffic_summary()
