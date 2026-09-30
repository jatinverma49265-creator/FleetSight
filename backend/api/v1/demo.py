"""
API v1 – Demo Controls & Bus Simulation router.

Provides endpoints to trigger bus passes, test offline store-and-forward caching,
execute re-detection checks, and fetch byte savings comparisons.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query, status
from pydantic import BaseModel

from backend.analytics.store import store
from backend.schemas import DataOrigin

router = APIRouter(prefix="/demo", tags=["demo"])


class SimulatePassRequest(BaseModel):
    """Request payload to trigger a simulated bus pass."""

    pass_number: int = 1
    seed: int = 42
    bus_id: str | None = None


class ReDetectionRequest(BaseModel):
    """Request payload to trigger an automated re-detection survey."""

    bus_id: str = "RJ14-12"
    detected_issue_ids: list[str] = []
    surveyed_segments: list[str] = [
        "MI Road (Ajmeri Gate to Paanch Batti)",
        "Tonk Road (Rambagh to Gandhi Nagar)",
        "JLN Marg (Birla Temple to Jawahar Circle)",
    ]


@router.post(
    "/simulate-pass",
    summary="Trigger a simulated bus corridor pass",
)
async def simulate_pass(req: SimulatePassRequest) -> dict[str, Any]:
    """Execute a simulated bus run along the corridor with deterministic noise and offsets."""
    from scripts.simulate_buses import execute_bus_pass

    result = execute_bus_pass(pass_number=req.pass_number, seed=req.seed, custom_bus_id=req.bus_id)
    return result


@router.post(
    "/redetection-check",
    summary="Execute automated re-detection verification loop",
)
async def redetection_check(req: ReDetectionRequest) -> dict[str, Any]:
    """
    Simulate a re-detection pass over existing work orders.
    Closes work orders where defect is absent; escalates where defect persists.
    """
    result = store.process_redetection_pass(
        bus_id=req.bus_id,
        detected_issue_ids=req.detected_issue_ids,
        surveyed_road_segments=req.surveyed_segments,
    )
    return result


@router.post(
    "/reset",
    summary="Reset demo simulation state deterministically",
)
async def reset_demo(seed: int = Query(default=42)) -> dict[str, Any]:
    """Clear memory store and re-seed clean corridor state."""
    store.reset_state()
    from scripts.seed_demo_data import seed_jaipur_demo_data
    seed_jaipur_demo_data()
    return {
        "status": "reset_complete",
        "seed": seed,
        "issues_count": len(store.issues),
        "work_orders_count": len(store.work_orders),
    }


@router.get(
    "/bytes-comparison",
    summary="Get compact event JSON vs 720p video bandwidth metrics",
)
async def get_bytes_comparison() -> dict[str, Any]:
    """Return measured byte counts and percentage bandwidth reduction."""
    return store.get_bandwidth_comparison()
