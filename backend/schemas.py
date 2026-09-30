"""
FleetSight data contracts — Pydantic schemas for detection events.

These schemas define the wire format between the edge pipeline and the
backend API.  They are also used for API request/response validation.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

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
# API response wrappers & Extended Schemas for Loops 4, 5, 6
# ---------------------------------------------------------------------------


class UserRole(StrEnum):
    """RBAC user roles."""

    ADMIN = "admin"
    ENGINEER = "engineer"
    POLICE = "police"
    VIEWER = "viewer"


class User(BaseModel):
    """User profile and role."""

    user_id: str
    username: str
    name: str
    role: UserRole


class LoginRequest(BaseModel):
    """Authentication login request."""

    username: str
    password: str = "fleetsight123"


class AuthResponse(BaseModel):
    """Authentication response token."""

    access_token: str
    token_type: str = "bearer"
    user: User


class IssueStatus(StrEnum):
    """Lifecycle status of a road issue."""

    CANDIDATE = "candidate"
    VERIFIED = "verified"
    WORK_ORDER = "work_order"
    REPAIRED = "repaired"
    CLOSED = "closed"


class SeverityBreakdown(BaseModel):
    """Explainable factors contributing to priority score (0-100)."""

    score: int = Field(..., ge=0, le=100)
    severity_level: SeverityLevel
    severity_weight: int = Field(..., description="Base severity score contribution (0-40)")
    recurrence_weight: int = Field(..., description="Observation / bus pass count contribution (0-30)")
    context_weight: int = Field(..., description="Arterial vs Local road context contribution (0-20)")
    confidence_weight: int = Field(..., description="Detector confidence contribution (0-10)")
    road_classification: str = Field(default="Arterial", description="Arterial | Collector | Local")
    explanation: str


class ClusteredIssue(BaseModel):
    """
    Spatially clustered road defect / infrastructure issue.

    Formed by corroborating events within a spatial radius (<=35m).
    Promoted from candidate to verified when observed by 2+ distinct buses.
    """

    issue_id: str = Field(default_factory=lambda: f"ISSUE-{uuid.uuid4().hex[:8].upper()}")
    type: DetectionType
    detection_class: DetectionClass
    status: IssueStatus = IssueStatus.CANDIDATE
    severity: SeverityLevel
    priority_score: int = Field(..., ge=0, le=100)
    severity_breakdown: SeverityBreakdown
    latitude: float
    longitude: float
    road_segment: str
    first_detected_at: datetime
    last_detected_at: datetime
    observation_count: int = 1
    bus_ids: list[str] = Field(default_factory=list)
    camera_ids: list[str] = Field(default_factory=list)
    event_ids: list[str] = Field(default_factory=list)
    evidence_uri: str | None = None
    data_origin: DataOrigin = DataOrigin.SIMULATED


class WorkOrderStatus(StrEnum):
    """Operational status of a maintenance work order."""

    CANDIDATE = "candidate"
    ACKNOWLEDGED = "acknowledged"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CLOSED = "closed"
    ESCALATED = "escalated"


class WorkOrderHistoryItem(BaseModel):
    """Audit item for work order state transition."""

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    action: str
    user_id: str
    username: str
    role: UserRole
    comment: str | None = None


class WorkOrder(BaseModel):
    """Ranked work order candidate for municipal maintenance engineers."""

    work_order_id: str = Field(default_factory=lambda: f"WO-{uuid.uuid4().hex[:8].upper()}")
    issue_id: str
    title: str
    description: str
    detection_class: DetectionClass
    severity: SeverityLevel
    priority_score: int = Field(..., ge=0, le=100)
    severity_breakdown: SeverityBreakdown
    status: WorkOrderStatus = WorkOrderStatus.CANDIDATE
    assigned_to: str | None = None
    latitude: float
    longitude: float
    road_segment: str
    observation_count: int = 1
    corroborating_buses: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    evidence_uri: str | None = None
    data_origin: DataOrigin = DataOrigin.SIMULATED
    history: list[WorkOrderHistoryItem] = Field(default_factory=list)


class WorkOrderUpdateRequest(BaseModel):
    """Request to update work order status or assignment."""

    status: WorkOrderStatus | None = None
    assigned_to: str | None = None
    comment: str | None = None


class TrafficSegment(BaseModel):
    """Vehicle counts per road segment per 15-minute interval."""

    segment_id: str
    road_name: str
    latitude: float
    longitude: float
    interval_start: datetime
    interval_end: datetime
    vehicle_count: int
    car_count: int = 0
    bus_count: int = 0
    truck_count: int = 0
    two_wheeler_count: int = 0
    auto_rickshaw_count: int = 0
    congestion_level: str = "moderate"  # low | moderate | heavy | severe
    data_origin: DataOrigin = DataOrigin.SIMULATED


class CorridorTrafficSummary(BaseModel):
    """Corridor volume time series and segment counts."""

    corridor_name: str
    total_vehicles: int
    time_series: list[dict[str, Any]]
    segments: list[TrafficSegment]


class KPIResponse(BaseModel):
    """Operational and fleet analytics metrics."""

    buses_active: int
    km_surveyed: float
    defects_detected: int
    defects_verified: int
    defects_corroborated: int
    work_orders_created: int
    work_orders_acknowledged: int
    work_orders_closed: int
    median_latency_seconds: float
    bandwidth_saved_pct: float
    false_positive_rate_pct: float | None = None  # None / null if not yet measured
    data_origin: DataOrigin = DataOrigin.SIMULATED


class AuditLogEntry(BaseModel):
    """Immutable log entry for system actions and data access."""

    audit_id: str = Field(default_factory=lambda: f"AUD-{uuid.uuid4().hex[:8].upper()}")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    user_id: str
    username: str
    role: UserRole
    action: str
    resource_type: str
    resource_id: str
    details: str
    ip_address: str = "127.0.0.1"


class EventCreateResponse(BaseModel):
    """Returned after successfully ingesting an event."""

    event_id: str
    status: str = "accepted"


class HealthResponse(BaseModel):
    """Response schema for GET /health."""

    status: str = "ok"
    version: str
    environment: str

