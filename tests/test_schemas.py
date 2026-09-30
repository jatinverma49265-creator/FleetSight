"""Tests for DetectionEvent schema validation."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from backend.schemas import (
    DataOrigin,
    DetectionClass,
    DetectionEvent,
    DetectionType,
    SeverityLevel,
)


def _valid_event_data(**overrides: object) -> dict[str, Any]:
    """Return a minimal valid event payload, with optional overrides."""
    base = {
        "event_id": str(uuid.uuid4()),
        "type": DetectionType.ROAD_DAMAGE.value,
        "class": DetectionClass.POTHOLE.value,
        "confidence": 0.87,
        "latitude": 26.9124,
        "longitude": 75.7873,
        "timestamp": datetime.now(UTC).isoformat(),
        "camera_id": "cam-front-01",
        "bus_id": "JR-BUS-042",
        "model_version": "yolo11-v0.1.0",
        "data_origin": DataOrigin.MEASURED.value,
    }
    base.update(overrides)
    return base


# ---- Happy path ----


class TestValidEvents:
    def test_minimal_valid_event(self) -> None:
        """A well-formed payload should parse without errors."""
        event = DetectionEvent(**_valid_event_data())
        assert event.detection_class == DetectionClass.POTHOLE
        assert event.data_origin == DataOrigin.MEASURED

    def test_confidence_rounded(self) -> None:
        """Confidence is rounded to 4 decimal places."""
        event = DetectionEvent(**_valid_event_data(confidence=0.876543))
        assert event.confidence == 0.8765

    def test_severity_defaults_to_none(self) -> None:
        """Edge devices may omit severity; it defaults to None."""
        event = DetectionEvent(**_valid_event_data())
        assert event.severity is None

    def test_severity_can_be_set(self) -> None:
        """Backend can populate severity."""
        event = DetectionEvent(**_valid_event_data(severity=SeverityLevel.HIGH.value))
        assert event.severity == SeverityLevel.HIGH

    def test_simulated_origin(self) -> None:
        """Simulated events must be explicitly tagged."""
        event = DetectionEvent(**_valid_event_data(data_origin=DataOrigin.SIMULATED.value))
        assert event.data_origin == DataOrigin.SIMULATED


# ---- Validation failures ----


class TestInvalidEvents:
    def test_confidence_above_one(self) -> None:
        with pytest.raises(ValidationError):
            DetectionEvent(**_valid_event_data(confidence=1.5))

    def test_confidence_below_zero(self) -> None:
        with pytest.raises(ValidationError):
            DetectionEvent(**_valid_event_data(confidence=-0.1))

    def test_latitude_out_of_range(self) -> None:
        with pytest.raises(ValidationError):
            DetectionEvent(**_valid_event_data(latitude=100.0))

    def test_longitude_out_of_range(self) -> None:
        with pytest.raises(ValidationError):
            DetectionEvent(**_valid_event_data(longitude=200.0))

    def test_empty_camera_id(self) -> None:
        with pytest.raises(ValidationError):
            DetectionEvent(**_valid_event_data(camera_id=""))

    def test_empty_bus_id(self) -> None:
        with pytest.raises(ValidationError):
            DetectionEvent(**_valid_event_data(bus_id=""))

    def test_missing_required_field(self) -> None:
        data = _valid_event_data()
        del data["class"]
        with pytest.raises(ValidationError):
            DetectionEvent(**data)

    def test_invalid_detection_type(self) -> None:
        with pytest.raises(ValidationError):
            DetectionEvent(**_valid_event_data(type="not_a_type"))

    def test_invalid_detection_class(self) -> None:
        with pytest.raises(ValidationError):
            DetectionEvent(**_valid_event_data(**{"class": "not_a_class"}))
