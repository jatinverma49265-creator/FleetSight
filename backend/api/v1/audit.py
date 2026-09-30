"""
API v1 – Audit Log router.

Provides access to the immutable audit log for administrative and law-enforcement compliance.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from backend.analytics.store import store
from backend.api.v1.auth import require_roles
from backend.schemas import AuditLogEntry, User, UserRole

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get(
    "/",
    response_model=list[AuditLogEntry],
    summary="List immutable audit trail (Admin & Police only)",
)
async def list_audit_logs(
    limit: int = Query(default=100, ge=1, le=500),
    current_user: Annotated[User, Depends(require_roles([UserRole.ADMIN, UserRole.POLICE]))] = None,
) -> list[AuditLogEntry]:
    """Return chronological audit log of security events and state changes."""
    return store.get_audit_logs(limit=limit)
