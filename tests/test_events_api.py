"""Tests for the /api/v1/events endpoints."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from fastapi.testclient import TestClient

from backend.schemas import DataOrigin, DetectionClass, DetectionType


def _valid_event_payload(**overrides: object) -> dict[str, Any]:
    base = {
        "event_id": str(uuid.uuid4()),
        "type": DetectionType.ROAD_DAMAGE.value,
        "class": DetectionClass.POTHOLE.value,
        "confidence": 0.91,
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


class TestCreateEvent:
    def test_create_returns_201(self, client: TestClient) -> None:
        resp = client.post("/api/v1/events/", json=_valid_event_payload())
        assert resp.status_code == 201
        body = resp.json()
        assert body["status"] == "accepted"
        assert "event_id" in body

    def test_create_invalid_payload_returns_422(self, client: TestClient) -> None:
        resp = client.post("/api/v1/events/", json={"bad": "data"})
        assert resp.status_code == 422

    def test_create_out_of_range_confidence(self, client: TestClient) -> None:
        resp = client.post(
            "/api/v1/events/",
            json=_valid_event_payload(confidence=5.0),
        )
        assert resp.status_code == 422


class TestListEvents:
    def test_list_empty(self, client: TestClient) -> None:
        resp = client.get("/api/v1/events/")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
