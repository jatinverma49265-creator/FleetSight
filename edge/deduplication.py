"""
Spatial-Temporal Event Deduplication Subsystem.

Suppresses redundant event creation when the same road distress or obstacle
is observed repeatedly across consecutive frames or within close spatial/temporal bounds.
Single-bus edge deduplication only (multi-bus corroboration belongs to backend loops).
"""

from __future__ import annotations

import math
from dataclasses import dataclass


def haversine_distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Compute great-circle distance between two GPS coordinates in meters."""
    r = 6371000.0  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return r * c


@dataclass
class DeduplicationConfig:
    """Configurable boundaries for duplicate hazard suppression."""

    spatial_threshold_m: float = 15.0
    temporal_window_s: float = 5.0
    deduplicate_by_track: bool = True


@dataclass
class EmittedEventRecord:
    """Historical footprint of an emitted candidate event."""

    detection_class: str
    track_id: str | None
    timestamp_s: float
    latitude: float | None
    longitude: float | None


class SpatialTemporalDeduplicator:
    """
    Filters candidate detections to eliminate duplicate event generation.
    """

    def __init__(self, config: DeduplicationConfig | None = None) -> None:
        self.config = config or DeduplicationConfig()
        self._history: list[EmittedEventRecord] = []
        self._evaluated_count: int = 0
        self._suppressed_count: int = 0

    @property
    def evaluated_count(self) -> int:
        return self._evaluated_count

    @property
    def suppressed_count(self) -> int:
        return self._suppressed_count

    def reset(self) -> None:
        """Clear event emission history."""
        self._history.clear()
        self._evaluated_count = 0
        self._suppressed_count = 0

    def should_emit(
        self,
        detection_class: str,
        track_id: str | None,
        timestamp_s: float,
        latitude: float | None = None,
        longitude: float | None = None,
    ) -> bool:
        """
        Evaluate if a candidate detection is novel or a duplicate of a recent event.

        Returns:
            True if event is novel and should be emitted; False if duplicate.
        """
        self._evaluated_count += 1

        # Purge stale records outside the temporal window
        cutoff_time = timestamp_s - self.config.temporal_window_s
        self._history = [r for r in self._history if r.timestamp_s >= cutoff_time]

        for record in self._history:
            if record.detection_class != detection_class:
                continue

            # 1. Track ID match within window
            if (
                self.config.deduplicate_by_track
                and track_id is not None
                and record.track_id == track_id
            ):
                self._suppressed_count += 1
                return False

            # 2. Spatial proximity match within temporal window
            if (
                latitude is not None
                and longitude is not None
                and record.latitude is not None
                and record.longitude is not None
            ):
                dist_m = haversine_distance_m(
                    latitude, longitude, record.latitude, record.longitude
                )
                if dist_m <= self.config.spatial_threshold_m:
                    self._suppressed_count += 1
                    return False

        # Novel event: record and approve emission
        self._history.append(
            EmittedEventRecord(
                detection_class=detection_class,
                track_id=track_id,
                timestamp_s=timestamp_s,
                latitude=latitude,
                longitude=longitude,
            )
        )
        return True
