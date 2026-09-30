"""
Lightweight Centroid Object Tracker.

Associates object and road defect detections across consecutive frames using
spatial Euclidean distance between bounding box centroids.
Prevents duplicate event triggers when a road hazard is visible across multiple frames.
Designed as an interchangeable TrackerAdapter so production ByteTrack can be dropped in later.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

from edge.interfaces import TrackedDetection, TrackerAdapter
from ml.detector import Detection


@dataclass
class TrackerConfig:
    """Hyperparameters governing cross-frame association."""

    max_distance_px: float = 60.0
    max_disappeared: int = 5
    min_hits: int = 1


@dataclass
class TrackState:
    """State tracking for a single persistent visual entity."""

    track_id: str
    class_id: int
    class_name: str
    centroid_x: float
    centroid_y: float
    bbox: tuple[float, float, float, float]
    hits: int = 1
    disappeared: int = 0
    last_detection: Detection | None = None


class CentroidTracker(TrackerAdapter):
    """
    Associates bounding boxes across frames using centroid proximity.
    """

    def __init__(self, config: TrackerConfig | None = None) -> None:
        self.config = config or TrackerConfig()
        self._next_id: int = 1
        self._tracks: dict[str, TrackState] = {}

    @property
    def active_track_count(self) -> int:
        return len(self._tracks)

    def reset(self) -> None:
        """Clear all active tracks and reset counter."""
        self._tracks.clear()
        self._next_id = 1

    def _register(self, det: Detection, cx: float, cy: float) -> str:
        tid = f"trk_{self._next_id:04d}"
        self._next_id += 1
        self._tracks[tid] = TrackState(
            track_id=tid,
            class_id=det.class_id,
            class_name=det.class_name,
            centroid_x=cx,
            centroid_y=cy,
            bbox=(det.x1, det.y1, det.x2, det.y2),
            hits=1,
            disappeared=0,
            last_detection=det,
        )
        return tid

    def _deregister(self, track_id: str) -> None:
        self._tracks.pop(track_id, None)

    def update(self, detections: Sequence[Detection]) -> Sequence[TrackedDetection]:
        """
        Accept current frame detections and update track associations.

        Returns:
            List of TrackedDetection objects enriched with persistent track_ids.
        """
        if not detections:
            # Mark all active tracks as disappeared
            for tid in list(self._tracks.keys()):
                self._tracks[tid].disappeared += 1
                if self._tracks[tid].disappeared > self.config.max_disappeared:
                    self._deregister(tid)
            return []

        # Calculate centroids for input detections
        input_centroids: list[tuple[float, float]] = []
        for d in detections:
            cx = (d.x1 + d.x2) / 2.0
            cy = (d.y1 + d.y2) / 2.0
            input_centroids.append((cx, cy))

        # If no active tracks, register all detections
        if not self._tracks:
            results: list[TrackedDetection] = []
            for d, (cx, cy) in zip(detections, input_centroids, strict=False):
                tid = self._register(d, cx, cy)
                results.append(TrackedDetection(detection=d, track_id=tid))
            return results

        # Match existing tracks with input detections
        track_ids = list(self._tracks.keys())
        track_centroids = [
            (self._tracks[tid].centroid_x, self._tracks[tid].centroid_y) for tid in track_ids
        ]

        # Compute Euclidean distance matrix
        distances: list[tuple[float, int, int]] = []
        for t_idx, (tx, ty) in enumerate(track_centroids):
            tid = track_ids[t_idx]
            for d_idx, (dx, dy) in enumerate(input_centroids):
                det = detections[d_idx]
                # Class compatibility check
                if det.class_id != self._tracks[tid].class_id:
                    continue
                dist = math.hypot(tx - dx, ty - dy)
                if dist <= self.config.max_distance_px:
                    distances.append((dist, t_idx, d_idx))

        # Sort by ascending distance (greedy matching)
        distances.sort(key=lambda x: x[0])

        used_tracks: set[int] = set()
        used_detections: set[int] = set()
        results_map: dict[int, TrackedDetection] = {}

        for _dist, t_idx, d_idx in distances:
            if t_idx in used_tracks or d_idx in used_detections:
                continue

            tid = track_ids[t_idx]
            det = detections[d_idx]
            cx, cy = input_centroids[d_idx]

            # Update matched track
            track = self._tracks[tid]
            track.centroid_x = cx
            track.centroid_y = cy
            track.bbox = (det.x1, det.y1, det.x2, det.y2)
            track.hits += 1
            track.disappeared = 0
            track.last_detection = det

            used_tracks.add(t_idx)
            used_detections.add(d_idx)
            results_map[d_idx] = TrackedDetection(detection=det, track_id=tid)

        # Handle unmatched existing tracks
        for t_idx, tid in enumerate(track_ids):
            if t_idx not in used_tracks:
                self._tracks[tid].disappeared += 1
                if self._tracks[tid].disappeared > self.config.max_disappeared:
                    self._deregister(tid)

        # Register unmatched new detections
        for d_idx, det in enumerate(detections):
            if d_idx not in used_detections:
                cx, cy = input_centroids[d_idx]
                tid = self._register(det, cx, cy)
                results_map[d_idx] = TrackedDetection(detection=det, track_id=tid)

        # Return ordered by original detection index
        return [results_map[i] for i in range(len(detections)) if i in results_map]
