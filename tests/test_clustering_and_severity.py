"""
Tests for spatial clustering, multi-bus corroboration, and explainable severity scoring.
"""

from datetime import UTC, datetime

import pytest

from backend.analytics.clustering import CorroborationEngine, haversine_distance_meters
from backend.analytics.severity import calculate_severity_breakdown, compute_severity_level
from backend.schemas import (
    BoundingBox,
    DataOrigin,
    DetectionClass,
    DetectionEvent,
    DetectionType,
    IssueStatus,
    SeverityLevel,
)


def test_haversine_distance_calculation():
    """Verify distance calculation between known coordinates."""
    # MI Road Paanch Batti to Ajmeri Gate (~1.0 km)
    d = haversine_distance_meters(26.9180, 75.8180, 26.9165, 75.8095)
    assert 800 < d < 1200


def test_severity_breakdown_explainability():
    """Verify explainable severity scoring formula components."""
    breakdown = calculate_severity_breakdown(
        severity_level=SeverityLevel.HIGH,
        observation_count=2,
        confidence=0.91,
        road_classification="Arterial",
    )
    # Severity High = 32, 2 observations = 20, Arterial = 20, Confidence = 9 -> Score = 81
    assert breakdown.severity_weight == 32
    assert breakdown.recurrence_weight == 20
    assert breakdown.context_weight == 20
    assert breakdown.confidence_weight == 9
    assert breakdown.score == 81
    assert "HIGH" in breakdown.explanation
    assert "Arterial" in breakdown.explanation


def test_corroboration_multi_bus_promotion():
    """Verify that a single bus observation creates a CANDIDATE, and 2nd bus promotes to VERIFIED."""
    engine = CorroborationEngine(cluster_radius_meters=35.0)
    existing_issues = []

    # Bus 1 pass
    event1 = DetectionEvent(
        type=DetectionType.ROAD_DAMAGE,
        detection_class=DetectionClass.POTHOLE,
        confidence=0.88,
        severity=SeverityLevel.HIGH,
        latitude=26.9172,
        longitude=75.8125,
        timestamp=datetime.now(UTC),
        camera_id="CAM-01",
        bus_id="RJ14-01",
        model_version="yolo11-v0.1.0",
        data_origin=DataOrigin.SIMULATED,
    )
    issue1, is_new = engine.process_event(event1, existing_issues)
    assert is_new is True
    assert issue1.status == IssueStatus.CANDIDATE
    assert issue1.observation_count == 1
    assert issue1.bus_ids == ["RJ14-01"]
    initial_score = issue1.priority_score
    existing_issues.append(issue1)

    # Bus 2 pass (~15m away)
    event2 = DetectionEvent(
        type=DetectionType.ROAD_DAMAGE,
        detection_class=DetectionClass.POTHOLE,
        confidence=0.92,
        severity=SeverityLevel.HIGH,
        latitude=26.9173,
        longitude=75.8126,
        timestamp=datetime.now(UTC),
        camera_id="CAM-07",
        bus_id="RJ14-07",
        model_version="yolo11-v0.1.0",
        data_origin=DataOrigin.SIMULATED,
    )
    issue2, is_new2 = engine.process_event(event2, existing_issues)
    assert is_new2 is False
    assert issue2.issue_id == issue1.issue_id
    assert issue2.observation_count == 2
    assert set(issue2.bus_ids) == {"RJ14-01", "RJ14-07"}
    assert issue2.status == IssueStatus.VERIFIED
    assert issue2.priority_score > initial_score
