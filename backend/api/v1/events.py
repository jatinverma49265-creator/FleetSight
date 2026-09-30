"""
API v1 – Events router.

Provides endpoints for ingesting and retrieving detection events.
"""

from __future__ import annotations

from fastapi import APIRouter, Query, status

from backend.analytics.store import store
from backend.logging_config import get_logger
from backend.schemas import DetectionEvent, EventCreateResponse

logger = get_logger("api.v1.events")

router = APIRouter(prefix="/events", tags=["events"])


@router.post(
    "/",
    response_model=EventCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Ingest a detection event",
)
async def create_event(event: DetectionEvent) -> EventCreateResponse:
    """Accept and store a single detection event from an edge device, dispatching to corroborator."""
    store.ingest_event(event)
    logger.info(
        "Event ingested: id=%s class=%s origin=%s bus=%s",
        event.event_id,
        event.detection_class.value,
        event.data_origin.value,
        event.bus_id,
    )
    return EventCreateResponse(event_id=event.event_id)


@router.get(
    "/",
    response_model=list[DetectionEvent],
    summary="List recent events",
)
async def list_events(limit: int = Query(default=50, ge=1, le=500)) -> list[DetectionEvent]:
    """Return the most recent detection events."""
    return store.events[-limit:]
