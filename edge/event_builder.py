"""
Edge Event Builder Subsystem.

Transforms raw tracked detections and GPS telemetry into standardized,
strongly-typed FleetSight event dictionaries compatible with the central API schema.
"""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from backend.schemas import DataOrigin, DetectionClass, DetectionType
from edge.interfaces import EventBuilder, GPSReading, TrackedDetection

# Maps fine-grained DetectionClass to top-level DetectionType
CLASS_TO_TYPE_MAP: dict[DetectionClass, DetectionType] = {
    DetectionClass.POTHOLE: DetectionType.ROAD_DAMAGE,
    DetectionClass.LONGITUDINAL_CRACK: DetectionType.ROAD_DAMAGE,
    DetectionClass.TRANSVERSE_CRACK: DetectionType.ROAD_DAMAGE,
    DetectionClass.ALLIGATOR_CRACK: DetectionType.ROAD_DAMAGE,
    DetectionClass.WATERLOGGING: DetectionType.ROAD_DAMAGE,
    DetectionClass.DAMAGED_SIGN: DetectionType.INFRASTRUCTURE,
    DetectionClass.MISSING_SIGN: DetectionType.INFRASTRUCTURE,
    DetectionClass.SIGNBOARD: DetectionType.INFRASTRUCTURE,
    DetectionClass.ZEBRA_CROSSING: DetectionType.INFRASTRUCTURE,
    DetectionClass.DAMAGED_BARRIER: DetectionType.INFRASTRUCTURE,
    DetectionClass.VEHICLE: DetectionType.TRAFFIC,
    DetectionClass.CAR: DetectionType.TRAFFIC,
    DetectionClass.BUS: DetectionType.TRAFFIC,
    DetectionClass.TRUCK: DetectionType.TRAFFIC,
    DetectionClass.TWO_WHEELER: DetectionType.TRAFFIC,
    DetectionClass.AUTO_RICKSHAW: DetectionType.TRAFFIC,
    DetectionClass.PEDESTRIAN: DetectionType.PEDESTRIAN,
    DetectionClass.OTHER: DetectionType.OTHER,
}


class EdgeDetectionEvent(BaseModel):
    """Strongly-typed edge detection event model."""

    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    detection_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    bus_id: str
    camera_id: str
    frame_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    detection_class: str
    detection_type: str = "road_damage"
    confidence: float
    bbox: dict[str, float] | None = None
    latitude: float | None = None
    longitude: float | None = None
    model_version: str = "yolo11-v0.1.0"
    data_origin: str = "measured"
    track_id: str | None = None
    evidence_path: str | None = None

    model_config = ConfigDict(extra="ignore")

    def to_api_dict(self) -> dict[str, Any]:
        """Convert to dict matching backend.schemas.DetectionEvent wire contract."""
        data: dict[str, Any] = {
            "event_id": self.event_id,
            "type": self.detection_type,
            "class": self.detection_class,
            "confidence": self.confidence,
            "latitude": self.latitude if self.latitude is not None else 0.0,
            "longitude": self.longitude if self.longitude is not None else 0.0,
            "timestamp": self.timestamp.isoformat(),
            "camera_id": self.camera_id,
            "bus_id": self.bus_id,
            "model_version": self.model_version,
            "data_origin": self.data_origin,
            "track_id": self.track_id,
            "evidence_uri": self.evidence_path,
        }
        if self.bbox:
            data["bbox"] = self.bbox
        return data


class DefaultEventBuilder(EventBuilder):
    """
    Standard event builder converting tracked detections and GPS into event payloads.
    """

    def __init__(
        self,
        model_version: str = "yolo11-v0.1.0",
        frame_width: int = 640,
        frame_height: int = 480,
        is_simulation: bool = False,
    ) -> None:
        self.model_version = model_version
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.is_simulation = is_simulation

    def _resolve_detection_type(self, class_name: str) -> DetectionType:
        """Resolve top-level DetectionType from class name."""
        try:
            det_class = DetectionClass(class_name.lower())
            return CLASS_TO_TYPE_MAP.get(det_class, DetectionType.OTHER)
        except ValueError:
            return DetectionType.OTHER

    def build(
        self,
        tracked: Sequence[TrackedDetection],
        gps: GPSReading | None,
        camera_id: str,
        bus_id: str,
        frame_id: str = "",
        evidence_path: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Assemble canonical event dictionaries from tracked detections and GPS reading.
        """
        events: list[dict[str, Any]] = []
        origin = DataOrigin.SIMULATED.value if self.is_simulation else DataOrigin.MEASURED.value

        for item in tracked:
            det = item.detection
            det_type = self._resolve_detection_type(det.class_name)

            # Compute normalized bounding box (x, y, w, h in [0.0, 1.0])
            norm_x = max(0.0, min(det.x1 / self.frame_width, 1.0))
            norm_y = max(0.0, min(det.y1 / self.frame_height, 1.0))
            norm_w = max(0.0, min((det.x2 - det.x1) / self.frame_width, 1.0))
            norm_h = max(0.0, min((det.y2 - det.y1) / self.frame_height, 1.0))

            event = EdgeDetectionEvent(
                bus_id=bus_id,
                camera_id=camera_id,
                frame_id=frame_id or str(uuid.uuid4()),
                detection_class=det.class_name,
                detection_type=det_type.value,
                confidence=round(det.confidence, 4),
                bbox={"x": norm_x, "y": norm_y, "w": norm_w, "h": norm_h},
                latitude=gps.latitude if gps else None,
                longitude=gps.longitude if gps else None,
                model_version=self.model_version,
                data_origin=origin,
                track_id=item.track_id,
                evidence_path=evidence_path,
            )
            events.append(event.to_api_dict())

        return events
