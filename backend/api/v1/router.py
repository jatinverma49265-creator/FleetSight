"""
API v1 router aggregator.

Collects all v1 sub-routers into a single router mounted at /api/v1.
"""

from __future__ import annotations

from fastapi import APIRouter

from backend.api.v1.events import router as events_router

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(events_router)
