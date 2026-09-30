"""
FleetSight data contracts — Pydantic schemas for detection events.

These schemas define the wire format between the edge pipeline and the
backend API.  They are also used for API request/response validation.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class DetectionType(StrEnum):
    """Top-level categories of detectable objects."""

    ROAD_DAMAGE = "road_damage"
    INFRASTRUCTURE = "infrastructure"
    TRAFFIC = "traffic"
    PEDESTRIAN = "pedestrian"
    OTHER = "other"


class DetectionClass(StrEnum):
    """Fine-grained detection classes across all models."""

    # Road damage (aligned with RDD2022 taxonomy)
    POTHOLE = "pothole"
    LONGITUDINAL_CRACK = "longitudinal_crack"
    TRANSVERSE_CRACK = "transverse_crack"
    ALLIGATOR_CRACK = "alligator_crack"
    WATERLOGGING = "waterlogging"

    # Infrastructure
    DAMAGED_SIGN = "damaged_sign"
    MISSING_SIGN = "missing_sign"
    SIGNBOARD = "signboard"
    ZEBRA_CROSSING = "zebra_crossing"
    DAMAGED_BARRIER = "damaged_barrier"

    # Traffic
    VEHICLE = "vehicle"
    CAR = "car"
    BUS = "bus"
    TRUCK = "truck"
    TWO_WHEELER = "two_wheeler"
    AUTO_RICKSHAW = "auto_rickshaw"

    # Pedestrian
    PEDESTRIAN = "pedestrian"

    # Catch-all
    OTHER = "other"


class SeverityLevel(StrEnum):
    """Severity levels — later computed by the backend severity engine."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DataOrigin(StrEnum):
    """Provenance tag so simulated data is never confused with real."""

    MEASURED = "measured"
    SIMULATED = "simulated"
    ILLUSTRATIVE = "illustrative"


# ---------------------------------------------------------------------------
# Core event schema
# ---------------------------------------------------------------------------


class BoundingBox(BaseModel):
    """Normalised bounding box (0-1 range, COCO-style xywh)."""

    x: float = Field(..., ge=0.0, le=1.0)
    y: float = Field(..., ge=0.0, le=1.0)
    w: float = Field(..., ge=0.0, le=1.0)
    h: float = Field(..., ge=0.0, le=1.0)


class DetectionEvent(BaseModel):
    """
    Canonical FleetSight detection event.

    Created on the edge device and ingested by the backend API.
    """

    event_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Globally unique event identifier",
    )
    type: DetectionType
    detection_class: DetectionClass = Field(
        ..., alias="class", description="Fine-grained detection class"
    )
    confidence: float = Field(..., ge=0.0, le=1.0)
    severity: SeverityLevel | None = Field(
        default=None,
        description="Populated by backend severity engine; may be null from edge",
    )

    # Geolocation
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)

    # Temporal
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="UTC timestamp of the detection",
    )

    # Source metadata
    camera_id: str = Field(..., min_length=1, max_length=64)
    bus_id: str = Field(..., min_length=1, max_length=64)
    model_version: str = Field(..., min_length=1, max_length=64, description="e.g. yolo11-v0.1.0")
    evidence_uri: str | None = Field(
        default=None,
        description="URI to cropped frame / video snippet (access-controlled)",
    )
    bbox: BoundingBox | None = Field(
        default=None, description="Detection bounding box in the source frame"
    )

    # Provenance
    data_origin: DataOrigin = Field(
        default=DataOrigin.MEASURED,
        description="Must be set to 'simulated' for demo/synthetic data",
    )

    # Tracking
    track_id: str | None = Field(
        default=None,
        description="Cross-frame track identifier (populated by tracker)",
    )

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("confidence")
    @classmethod
    def round_confidence(cls, v: float) -> float:
        return round(v, 4)


# ---------------------------------------------------------------------------
# API response wrappers
# ---------------------------------------------------------------------------


class EventCreateResponse(BaseModel):
    """Returned after successfully ingesting an event."""

    event_id: str
    status: str = "accepted"


class HealthResponse(BaseModel):
    """Response schema for GET /health."""

    status: str = "ok"
    version: str
    environment: str
