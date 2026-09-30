"""
API v1 router aggregator.

Collects all v1 sub-routers into a single router mounted at /api/v1.
"""

from __future__ import annotations

from fastapi import APIRouter

from backend.api.v1.audit import router as audit_router
from backend.api.v1.auth import router as auth_router
from backend.api.v1.demo import router as demo_router
from backend.api.v1.events import router as events_router
from backend.api.v1.issues import router as issues_router
from backend.api.v1.kpis import router as kpis_router
from backend.api.v1.traffic import router as traffic_router
from backend.api.v1.work_orders import router as work_orders_router

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(auth_router)
v1_router.include_router(demo_router)
v1_router.include_router(events_router)
v1_router.include_router(issues_router)
v1_router.include_router(work_orders_router)
v1_router.include_router(traffic_router)
v1_router.include_router(kpis_router)
v1_router.include_router(audit_router)
