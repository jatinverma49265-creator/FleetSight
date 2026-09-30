"""Tests for spatial-temporal event deduplication."""

from __future__ import annotations

import pytest

from edge.deduplication import (
    DeduplicationConfig,
    SpatialTemporalDeduplicator,
    haversine_distance_m,
)


class TestHaversine:
    def test_same_point_is_zero(self) -> None:
        assert haversine_distance_m(26.9, 75.8, 26.9, 75.8) == pytest.approx(0.0, abs=1e-6)

    def test_known_distance_approximate(self) -> None:
        # ~111 km per degree latitude at equator
        d = haversine_distance_m(0.0, 0.0, 1.0, 0.0)
        assert 110_000 < d < 112_000

    def test_direction_symmetry(self) -> None:
        d1 = haversine_distance_m(26.9, 75.8, 26.91, 75.81)
        d2 = haversine_distance_m(26.91, 75.81, 26.9, 75.8)
        assert d1 == pytest.approx(d2, rel=1e-6)

    def test_small_distance_metres(self) -> None:
        # ~1m step in latitude ≈ 0.000009 degrees
        d = haversine_distance_m(0.0, 0.0, 0.000009, 0.0)
        assert 0.5 < d < 2.0


class TestSpatialTemporalDeduplicator:
    def test_first_detection_is_novel(self) -> None:
        dedup = SpatialTemporalDeduplicator()
        assert dedup.should_emit("pothole", "trk_0001", 0.0) is True

    def test_same_track_within_window_is_suppressed(self) -> None:
        dedup = SpatialTemporalDeduplicator(DeduplicationConfig(temporal_window_s=5.0))
        dedup.should_emit("pothole", "trk_0001", 0.0)
        # Same track_id, same class, within temporal window
        assert dedup.should_emit("pothole", "trk_0001", 2.0) is False

    def test_different_class_same_track_is_novel(self) -> None:
        dedup = SpatialTemporalDeduplicator()
        dedup.should_emit("pothole", "trk_0001", 0.0)
        # Different class — new event type
        assert dedup.should_emit("car", "trk_0001", 1.0) is True

    def test_same_class_outside_temporal_window_is_novel(self) -> None:
        dedup = SpatialTemporalDeduplicator(DeduplicationConfig(temporal_window_s=3.0))
        dedup.should_emit("pothole", "trk_0001", 0.0)
        # 5 seconds later — outside the 3s window → novel
        assert dedup.should_emit("pothole", "trk_0001", 5.0) is True

    def test_spatial_proximity_suppression(self) -> None:
        cfg = DeduplicationConfig(
            spatial_threshold_m=15.0,
            temporal_window_s=10.0,
            deduplicate_by_track=False,
        )
        dedup = SpatialTemporalDeduplicator(cfg)
        # First detection at a location
        dedup.should_emit("pothole", None, 0.0, latitude=26.9, longitude=75.8)
        # Same location (within 15m), different track_id
        result = dedup.should_emit("pothole", None, 2.0, latitude=26.9, longitude=75.8)
        assert result is False

    def test_spatially_distant_detection_is_novel(self) -> None:
        cfg = DeduplicationConfig(spatial_threshold_m=15.0, temporal_window_s=10.0)
        dedup = SpatialTemporalDeduplicator(cfg)
        dedup.should_emit("pothole", "trk_0001", 0.0, latitude=26.9, longitude=75.8)
        # >200m away — completely novel
        result = dedup.should_emit("pothole", "trk_0002", 2.0, latitude=26.902, longitude=75.802)
        assert result is True

    def test_suppressed_count_increments(self) -> None:
        dedup = SpatialTemporalDeduplicator()
        dedup.should_emit("pothole", "trk_0001", 0.0)
        dedup.should_emit("pothole", "trk_0001", 1.0)
        dedup.should_emit("pothole", "trk_0001", 2.0)
        assert dedup.suppressed_count == 2
        assert dedup.evaluated_count == 3

    def test_reset_clears_history(self) -> None:
        dedup = SpatialTemporalDeduplicator()
        dedup.should_emit("pothole", "trk_0001", 0.0)
        dedup.reset()
        # After reset, same detection should be novel again
        assert dedup.should_emit("pothole", "trk_0001", 0.5) is True

    def test_no_gps_no_spatial_dedup(self) -> None:
        """Without GPS coords, spatial deduplication cannot fire."""
        cfg = DeduplicationConfig(
            spatial_threshold_m=5.0, temporal_window_s=10.0, deduplicate_by_track=False
        )
        dedup = SpatialTemporalDeduplicator(cfg)
        dedup.should_emit("pothole", None, 0.0, latitude=None, longitude=None)
        # No spatial record → second one with same None coords cannot match → novel
        result = dedup.should_emit("pothole", None, 2.0, latitude=None, longitude=None)
        assert result is True
