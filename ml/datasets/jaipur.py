"""
Jaipur Local Municipal Bus Dataset Structure & Metadata Specification.

Defines the directory layout, frame metadata schemas, privacy prerequisites,
and collection specifications for locally gathered dashcam footage (200-500 target frames)
from Jaipur City Transport Service Limited (JCTSL) bus routes.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Final

from pydantic import BaseModel, ConfigDict, Field

from backend.schemas import DetectionClass

# Canonical directory structure relative to the Jaipur dataset root
JAIPUR_SUBDIRECTORIES: Final[list[str]] = [
    "raw",  # Raw un-anonymized 1080p clips/frames (airgapped / local only)
    "processed",  # Anonymized frames (faces and license plates blurred)
    "images",  # Image symlinks/copies ready for training/eval
    "labels",  # YOLO format .txt annotations
    "splits",  # Route/day partitioned split indices (train.txt, val.txt, test.txt)
    "metadata",  # JSON frame-level telemetry and environmental conditions
]

# Supported target classes for Jaipur custom domain adaptation
JAIPUR_CLASSES: Final[list[DetectionClass]] = [
    DetectionClass.POTHOLE,
    DetectionClass.LONGITUDINAL_CRACK,
    DetectionClass.TRANSVERSE_CRACK,
    DetectionClass.ALLIGATOR_CRACK,
    DetectionClass.WATERLOGGING,
    DetectionClass.DAMAGED_SIGN,
    DetectionClass.ZEBRA_CROSSING,
    DetectionClass.VEHICLE,
    DetectionClass.PEDESTRIAN,
]

JAIPUR_CLASS_TO_ID: Final[dict[DetectionClass, int]] = {
    cls: idx for idx, cls in enumerate(JAIPUR_CLASSES)
}
JAIPUR_ID_TO_CLASS: Final[dict[int, DetectionClass]] = {
    idx: cls for idx, cls in enumerate(JAIPUR_CLASSES)
}


class JaipurFrameMetadata(BaseModel):
    """Metadata contract for a single collected dashcam frame in Jaipur."""

    frame_id: str = Field(
        ..., min_length=1, description="Unique frame identifier (e.g. jpr_r1_20260929_00123)"
    )
    route_id: str = Field(
        ..., min_length=1, description="Bus route identifier (e.g. Route-9A, AC-1)"
    )
    bus_id: str = Field(..., min_length=1, description="Vehicle fleet ID (e.g. RJ14-PA-1234)")
    timestamp: datetime = Field(..., description="Timestamp of recording")
    capture_day: str = Field(..., description="YYYY-MM-DD grouping key for route-day splitting")

    # Geolocation & Telemetry
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    speed_kmh: float = Field(default=0.0, ge=0.0)

    # Environmental & Operational Context
    weather: str = Field(default="clear", description="clear, dusty, overcast, rain")
    lighting: str = Field(default="daylight", description="daylight, golden_hour, night_artificial")

    # Privacy & Consent Compliance
    privacy_face_blurred: bool = Field(
        default=False, description="Must be True before moving to processed/images"
    )
    privacy_plate_blurred: bool = Field(
        default=False, description="Must be True before moving to processed/images"
    )
    consent_verified: bool = Field(
        default=False, description="Municipal transport pilot authorization confirmed"
    )

    model_config = ConfigDict(extra="ignore")


@dataclass(frozen=True)
class JaipurDatasetLayout:
    """Helper to inspect and initialize the Jaipur local dataset directories."""

    root_path: Path

    @property
    def raw_dir(self) -> Path:
        return self.root_path / "raw"

    @property
    def processed_dir(self) -> Path:
        return self.root_path / "processed"

    @property
    def images_dir(self) -> Path:
        return self.root_path / "images"

    @property
    def labels_dir(self) -> Path:
        return self.root_path / "labels"

    @property
    def splits_dir(self) -> Path:
        return self.root_path / "splits"

    @property
    def metadata_dir(self) -> Path:
        return self.root_path / "metadata"

    def initialize_structure(self) -> None:
        """Create the canonical directory hierarchy without populating data."""
        for subdir in JAIPUR_SUBDIRECTORIES:
            (self.root_path / subdir).mkdir(parents=True, exist_ok=True)

    def is_structure_valid(self) -> bool:
        """Check if all expected subdirectories exist."""
        return all((self.root_path / subdir).exists() for subdir in JAIPUR_SUBDIRECTORIES)
