"""Tests for ML detector interfaces, registry, and edge interfaces."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import numpy as np
import pytest

from edge.interfaces import (
    GPSReading,
    TrackedDetection,
    VideoSource,
)
from ml.detector import Detection, Detector, FrameResult
from ml.registry import available_detectors, create_detector, register_detector

# ---------------------------------------------------------------------------
# Stub implementations to verify Protocol compliance
# ---------------------------------------------------------------------------


class DummyDetector:
    """Minimal detector stub fulfilling the Detector protocol."""

    @property
    def model_name(self) -> str:
        return "dummy-model"

    @property
    def model_version(self) -> str:
        return "dummy-v0.1.0"

    def load(self, weights_path: Path, device: str = "cpu") -> None:
        pass

    def predict(
        self,
        frame: np.ndarray,
        confidence_threshold: float = 0.25,
    ) -> FrameResult:
        det = Detection(
            class_id=0,
            class_name="pothole",
            confidence=0.9,
            x1=10.0,
            y1=20.0,
            x2=100.0,
            y2=120.0,
        )
        return FrameResult(detections=[det], inference_time_ms=12.5)

    def warmup(self, imgsz: tuple[int, int] = (640, 640)) -> None:
        pass


class DummyVideoSource:
    def open(self, source: str | int | Path) -> None:
        pass

    def read(self) -> tuple[bool, np.ndarray]:
        return True, np.zeros((480, 640, 3), dtype=np.uint8)

    def release(self) -> None:
        pass

    def frames(self) -> Iterator[np.ndarray]:
        yield np.zeros((480, 640, 3), dtype=np.uint8)


# ---------------------------------------------------------------------------
# Test ML detector & registry
# ---------------------------------------------------------------------------


class TestMLDetectorAndRegistry:
    def test_detector_protocol_conformance(self) -> None:
        detector = DummyDetector()
        assert isinstance(detector, Detector)
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        result = detector.predict(frame)
        assert len(result.detections) == 1
        assert result.detections[0].class_name == "pothole"
        assert result.inference_time_ms > 0

    def test_register_and_create_detector(self) -> None:
        register_detector("dummy", DummyDetector)
        assert "dummy" in available_detectors()

        instance = create_detector("dummy")
        assert isinstance(instance, Detector)
        assert instance.model_name == "dummy-model"

    def test_unknown_detector_raises_key_error(self) -> None:
        with pytest.raises(KeyError, match="Unknown detector 'nonexistent'"):
            create_detector("nonexistent")

    def test_missing_weights_raises_file_not_found(self) -> None:
        register_detector("dummy_with_weights", DummyDetector)
        with pytest.raises(FileNotFoundError, match="Weights not found"):
            create_detector("dummy_with_weights", weights="non_existent_weights.pt")


# ---------------------------------------------------------------------------
# Test Edge protocols
# ---------------------------------------------------------------------------


class TestEdgeProtocols:
    def test_video_source_protocol(self) -> None:
        src = DummyVideoSource()
        assert isinstance(src, VideoSource)
        ok, frame = src.read()
        assert ok
        assert frame.shape == (480, 640, 3)

    def test_gps_reading_dataclass(self) -> None:
        gps = GPSReading(latitude=26.9124, longitude=75.7873, speed_kmh=42.0)
        assert gps.latitude == 26.9124
        assert gps.longitude == 75.7873
        assert gps.speed_kmh == 42.0
        assert gps.altitude_m is None

    def test_tracked_detection_dataclass(self) -> None:
        det = Detection(
            class_id=1,
            class_name="vehicle",
            confidence=0.85,
            x1=0,
            y1=0,
            x2=50,
            y2=50,
        )
        tracked = TrackedDetection(detection=det, track_id="track-42")
        assert tracked.track_id == "track-42"
        assert tracked.detection.class_name == "vehicle"
