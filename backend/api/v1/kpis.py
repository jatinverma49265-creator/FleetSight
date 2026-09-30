"""
API v1 – KPIs router.

Provides fleet operations, defect corroboration, and latency/bandwidth metrics.
"""

from __future__ import annotations

from fastapi import APIRouter

from backend.analytics.store import store
from backend.schemas import KPIResponse

router = APIRouter(prefix="/kpis", tags=["kpis"])


@router.get(
    "/",
    response_model=KPIResponse,
    summary="Get operational and fleet metrics",
)
async def get_kpis() -> KPIResponse:
    """Return operational metrics including active buses, defects corroborated, and bandwidth reduction."""
    return store.get_kpis()
