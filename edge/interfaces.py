"""
Edge pipeline interfaces (adapters / ports).

Each interface below defines a contract for one stage of the on-bus
processing pipeline.  Concrete implementations will be plugged in as
development proceeds.

Pipeline flow::

    VideoSource → InferenceAdapter → TrackerAdapter
                                          ↓
                                   EventBuilder  ← GPSAdapter
                                          ↓
                                    EventCache
                                          ↓
                                  (upload to backend)

All interfaces use Python's ``Protocol`` for structural subtyping so that
concrete classes do not need to inherit from a base class.
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

import numpy as np

from ml.detector import Detection, FrameResult

# ---------------------------------------------------------------------------
# Video input
# ---------------------------------------------------------------------------


@runtime_checkable
class VideoSource(Protocol):
    """Yields BGR frames from a camera or video file."""

    def open(self, source: str | int | Path) -> None:
        """Open a video file path, RTSP URL, or device index."""
        ...

    def read(self) -> tuple[bool, np.ndarray]:
        """Return (success, frame).  Frame is H×W×3 BGR uint8."""
        ...

    def release(self) -> None:
        """Release the underlying capture resource."""
        ...

    def frames(self) -> Iterator[np.ndarray]:
        """Convenience generator that yields frames until exhausted."""
        ...


# ---------------------------------------------------------------------------
# Inference adapter
# ---------------------------------------------------------------------------


@runtime_checkable
class InferenceAdapter(Protocol):
    """Wraps a ``Detector`` and applies it to frames from the pipeline."""

    def infer(self, frame: np.ndarray) -> FrameResult:
        """Run detection on a single frame."""
        ...


# ---------------------------------------------------------------------------
# Tracker adapter
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TrackedDetection:
    """A detection enriched with a persistent track ID."""

    detection: Detection
    track_id: str


@runtime_checkable
class TrackerAdapter(Protocol):
    """Assigns persistent IDs to detections across frames."""

    def update(self, detections: Sequence[Detection]) -> Sequence[TrackedDetection]:
        """Accept current-frame detections, return tracked detections."""
        ...

    def reset(self) -> None:
        """Clear tracker state (e.g. on route change)."""
        ...


# ---------------------------------------------------------------------------
# GPS adapter
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class GPSReading:
    """A single GPS fix."""

    latitude: float
    longitude: float
    altitude_m: float | None = None
    speed_kmh: float | None = None
    heading_deg: float | None = None
    timestamp: datetime | None = None
    hdop: float | None = None


@runtime_checkable
class GPSAdapter(Protocol):
    """Provides the latest GPS fix."""

    def latest(self) -> GPSReading | None:
        """Return the most recent reading, or None if unavailable."""
        ...


# ---------------------------------------------------------------------------
# Event builder
# ---------------------------------------------------------------------------


@runtime_checkable
class EventBuilder(Protocol):
    """Combines tracked detections + GPS into ``DetectionEvent`` objects."""

    def build(
        self,
        tracked: Sequence[TrackedDetection],
        gps: GPSReading | None,
        camera_id: str,
        bus_id: str,
    ) -> list[dict[str, Any]]:
        """
        Return a list of ``DetectionEvent`` dicts ready for API submission.

        The return type is ``list[dict[str, Any]]`` to avoid coupling the edge
        package to ``backend.schemas`` at import time.
        """
        ...


# ---------------------------------------------------------------------------
# Local event cache
# ---------------------------------------------------------------------------


@runtime_checkable
class EventCache(Protocol):
    """
    Persists events locally when connectivity is unavailable.

    Events are stored as JSON-lines files in a configurable directory and
    flushed to the backend when the connection resumes.
    """

    def push(self, event: dict[str, Any]) -> None:
        """Append an event to the local cache."""
        ...

    def flush(self) -> list[dict[str, Any]]:
        """Return and remove all cached events."""
        ...

    @property
    def size(self) -> int:
        """Number of events currently cached."""
        ...


# ---------------------------------------------------------------------------
# Privacy filter
# ---------------------------------------------------------------------------


@runtime_checkable
class PrivacyFilter(Protocol):
    """Obfuscates privacy-sensitive elements (faces, license plates) on edge frames."""

    def filter(
        self,
        frame: np.ndarray,
        regions: Sequence[tuple[float, float, float, float]] | None = None,
    ) -> np.ndarray:
        """
        Return an anonymized copy of the input frame.

        Parameters
        ----------
        frame:
            Input BGR frame (H×W×3 uint8).
        regions:
            Optional sequence of (x1, y1, x2, y2) pixel bounding boxes to blur.
        """
        ...


# ---------------------------------------------------------------------------
# Store-and-forward sync transport
# ---------------------------------------------------------------------------


@runtime_checkable
class SyncTransport(Protocol):
    """Dispatches cached events to central ingestion when connectivity is available."""

    def sync_event(self, event: dict[str, Any]) -> bool:
        """Transmit a single event. Returns True if accepted, False otherwise."""
        ...

    def sync_batch(
        self, events: Sequence[dict[str, Any]]
    ) -> tuple[list[str], list[str]]:
        """
        Transmit a batch of events.

        Returns (successful_event_ids, failed_event_ids).
        """
        ...

