"""
API v1 – Events router.

Provides endpoints for ingesting and retrieving detection events.
"""

from __future__ import annotations

from fastapi import APIRouter, status

from backend.logging_config import get_logger
from backend.schemas import DetectionEvent, EventCreateResponse

logger = get_logger("api.v1.events")

router = APIRouter(prefix="/events", tags=["events"])

# In-memory store for Loop 1.  Will be replaced by PostgreSQL/PostGIS.
_event_store: list[DetectionEvent] = []


@router.post(
    "/",
    response_model=EventCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Ingest a detection event",
)
async def create_event(event: DetectionEvent) -> EventCreateResponse:
    """Accept and store a single detection event from an edge device."""
    _event_store.append(event)
    logger.info(
        "Event ingested: id=%s class=%s origin=%s",
        event.event_id,
        event.detection_class.value,
        event.data_origin.value,
    )
    return EventCreateResponse(event_id=event.event_id)


@router.get(
    "/",
    response_model=list[DetectionEvent],
    summary="List recent events",
)
async def list_events(limit: int = 50) -> list[DetectionEvent]:
    """Return the most recent events (placeholder; will use DB query later)."""
    return _event_store[-limit:]
