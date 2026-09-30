"""
API v1 – Clustered Issues router.

Provides endpoints for listing, filtering, and inspecting corroborated road issues.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from backend.analytics.store import store
from backend.api.v1.auth import get_current_user
from backend.schemas import ClusteredIssue, IssueStatus, User

router = APIRouter(prefix="/issues", tags=["issues"])


@router.get(
    "/",
    response_model=list[ClusteredIssue],
    summary="List corroborated road issues",
)
async def list_issues(
    status_filter: IssueStatus | None = Query(default=None, alias="status"),
    detection_class: str | None = Query(default=None, alias="class"),
) -> list[ClusteredIssue]:
    """Return all clustered road issues with optional status and class filtering."""
    return store.get_issues(status=status_filter, detection_class=detection_class)


@router.get(
    "/{issue_id}",
    response_model=ClusteredIssue,
    summary="Get issue detail by ID",
)
async def get_issue(
    issue_id: str,
    user: Annotated[User, Depends(get_current_user)],
) -> ClusteredIssue:
    """Retrieve detailed observation trail and severity breakdown for an issue."""
    issue = store.get_issue_by_id(issue_id)
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Issue with ID '{issue_id}' not found.",
        )
    return issue
