"""
API v1 – Work Orders router.

Provides endpoints for managing the ranked work order candidate queue with RBAC enforcement.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from backend.analytics.store import store
from backend.api.v1.auth import get_current_user, require_roles
from backend.schemas import (
    User,
    UserRole,
    WorkOrder,
    WorkOrderStatus,
    WorkOrderUpdateRequest,
)

router = APIRouter(prefix="/work-orders", tags=["work-orders"])


@router.get(
    "/",
    response_model=list[WorkOrder],
    summary="List ranked work order candidates",
)
async def list_work_orders(
    status_filter: WorkOrderStatus | None = Query(default=None, alias="status"),
) -> list[WorkOrder]:
    """Return all ranked work orders sorted by explainable priority score descending."""
    return store.get_work_orders(status=status_filter)


@router.get(
    "/{work_order_id}",
    response_model=WorkOrder,
    summary="Get work order detail",
)
async def get_work_order(work_order_id: str) -> WorkOrder:
    """Retrieve complete work order candidate metadata, explainability factors, and audit history."""
    wo = store.get_work_order_by_id(work_order_id)
    if not wo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work order with ID '{work_order_id}' not found.",
        )
    return wo


@router.patch(
    "/{work_order_id}",
    response_model=WorkOrder,
    summary="Update work order status or assignment (Engineer / Admin only)",
)
async def update_work_order(
    work_order_id: str,
    req: WorkOrderUpdateRequest,
    current_user: Annotated[User, Depends(require_roles([UserRole.ENGINEER, UserRole.ADMIN]))],
) -> WorkOrder:
    """
    Approve, assign, escalate, or close a work order.

    Restricted strictly to Engineers and Municipal Admins via RBAC.
    """
    updated = store.update_work_order(
        work_order_id=work_order_id,
        user=current_user,
        status=req.status,
        assigned_to=req.assigned_to,
        comment=req.comment,
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work order with ID '{work_order_id}' not found.",
        )
    return updated
