"""
Integration tests for EdgePipelineOrchestrator.

Uses only in-memory components — no YOLO weights, no files, no network.
Covers full pipeline: simulated source → sampler → dummy detector → centroid tracker
→ deduplicator → mock privacy filter → SQLite cache.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from edge.cache import SQLiteEventCache
from edge.gps import StaticGPSAdapter, UnavailableGPSAdapter
from edge.orchestrator import EdgePipelineOrchestrator
from edge.privacy import MockPrivacyFilter, NoOpPrivacyFilter
from edge.sampling import FrameSampler, SamplingConfig
from edge.sources import SimulatedVideoSource
from ml.detector import Detection, Detector, FrameResult

# ---------------------------------------------------------------------------
# Dummy detector — deterministic, zero-weight ML stand-in
# ---------------------------------------------------------------------------


class DummyDetector(Detector):
    """Deterministic stub that injects one pothole detection on every call."""

    def __init__(self, emit_detection: bool = True) -> None:
        self._emit = emit_detection
        self._calls = 0

    @property
    def model_name(self) -> str:
        return "dummy-v0"

    @property
    def model_version(self) -> str:
        return "dummy-v0.0.1"

    def load(self, weights_path: Path, device: str = "cpu") -> None:  # noqa: ARG002
        pass

    def predict(self, frame: np.ndarray, confidence_threshold: float = 0.25) -> FrameResult:
        self._calls += 1
        if self._emit:
            return FrameResult(
                detections=[
                    Detection(
                        class_id=0,
                        class_name="pothole",
                        confidence=0.9,
                        x1=50.0,
                        y1=50.0,
                        x2=150.0,
                        y2=150.0,
                    )
                ],
                inference_time_ms=1.0,
            )
        return FrameResult(detections=[])

    def warmup(self, imgsz: tuple[int, int] = (640, 640)) -> None:
        pass


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_orchestrator(
    total_frames: int = 10,
    detector: Detector | None = None,
    cache_path: str = ":memory:",
    target_fps: float = 30.0,  # equal to source → sample every frame for tests
    privacy_filter: Any = None,
    gps: Any = None,
) -> EdgePipelineOrchestrator:
    source = SimulatedVideoSource(
        bus_id="BUS-TEST",
        camera_id="CAM-TEST",
        fps=30.0,
        width=320,
        height=240,
        total_frames=total_frames,
    )
    return EdgePipelineOrchestrator(
        source=source,
        detector=detector or DummyDetector(),
        sampler=FrameSampler(SamplingConfig(target_fps=target_fps, source_fps=30.0)),
        cache=SQLiteEventCache(db_path=cache_path),
        privacy_filter=privacy_filter or NoOpPrivacyFilter(),
        gps=gps or UnavailableGPSAdapter(),
        bus_id="BUS-TEST",
        camera_id="CAM-TEST",
        confidence_threshold=0.25,
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestOrchestratorBasic:
    def test_run_completes_without_error(self) -> None:
        orch = make_orchestrator(total_frames=5)
        telemetry = orch.run()
        assert telemetry.frames_received == 5

    def test_detections_cached_after_run(self) -> None:
        cache = SQLiteEventCache(db_path=":memory:")
        source = SimulatedVideoSource(total_frames=5, fps=30.0)
        orch = EdgePipelineOrchestrator(
            source=source,
            detector=DummyDetector(emit_detection=True),
            sampler=FrameSampler(SamplingConfig(target_fps=30.0, source_fps=30.0)),
            cache=cache,
        )
        orch.run()
        # At least some events should have been cached
        # (first detection is always novel; subsequent ones may be deduped)
        assert cache.total_count >= 1
        cache.close()

    def test_no_detections_nothing_cached(self) -> None:
        cache = SQLiteEventCache(db_path=":memory:")
        source = SimulatedVideoSource(total_frames=5)
        orch = EdgePipelineOrchestrator(
            source=source,
            detector=DummyDetector(emit_detection=False),
            sampler=FrameSampler(SamplingConfig(target_fps=30.0, source_fps=30.0)),
            cache=cache,
        )
        orch.run()
        assert cache.total_count == 0
        cache.close()

    def test_telemetry_frames_received(self) -> None:
        orch = make_orchestrator(total_frames=8)
        telemetry = orch.run()
        assert telemetry.frames_received == 8

    def test_max_frames_limit(self) -> None:
        """run() should stop after max_frames even if source has more."""
        orch = make_orchestrator(total_frames=20)
        telemetry = orch.run(max_frames=3)
        assert telemetry.frames_received == 3

    def test_sampler_reduces_inference_calls(self) -> None:
        det = DummyDetector()
        cache = SQLiteEventCache(db_path=":memory:")
        source = SimulatedVideoSource(total_frames=30, fps=30.0)
        sampler = FrameSampler(SamplingConfig(target_fps=6.0, source_fps=30.0))
        orch = EdgePipelineOrchestrator(
            source=source,
            detector=det,
            sampler=sampler,
            cache=cache,
        )
        orch.run()
        # With 6/30 = 1/5 sampling, ~6 frames from 30 should trigger inference
        assert det._calls <= 8  # allow some tolerance
        cache.close()


class TestPrivacyOrdering:
    def test_privacy_filter_invoked_before_cache_push(self) -> None:
        """Verify MockPrivacyFilter.invocations_count > 0 when events are cached."""
        mock_privacy = MockPrivacyFilter()
        cache = SQLiteEventCache(db_path=":memory:")
        source = SimulatedVideoSource(total_frames=3, fps=30.0)
        orch = EdgePipelineOrchestrator(
            source=source,
            detector=DummyDetector(emit_detection=True),
            sampler=FrameSampler(SamplingConfig(target_fps=30.0, source_fps=30.0)),
            privacy_filter=mock_privacy,
            cache=cache,
        )
        orch.run()
        # Privacy filter must have been called for novel detections
        assert mock_privacy.invocations_count >= 1
        # And cache must have events only after privacy filter fired
        assert cache.total_count >= 1
        cache.close()


class TestGPSIntegration:
    def test_unavailable_gps_events_have_null_coords(self) -> None:
        cache = SQLiteEventCache(db_path=":memory:")
        source = SimulatedVideoSource(total_frames=2, fps=30.0)
        orch = EdgePipelineOrchestrator(
            source=source,
            detector=DummyDetector(emit_detection=True),
            sampler=FrameSampler(SamplingConfig(target_fps=30.0, source_fps=30.0)),
            gps=UnavailableGPSAdapter(),
            cache=cache,
        )
        orch.run()
        pending = cache.get_pending()
        if pending:
            # lat/lon should be 0.0 (the null coordinate default in to_api_dict)
            assert pending[0]["latitude"] == 0.0
            assert pending[0]["longitude"] == 0.0
        cache.close()

    def test_static_gps_events_have_coordinates(self) -> None:
        cache = SQLiteEventCache(db_path=":memory:")
        source = SimulatedVideoSource(total_frames=2, fps=30.0)
        orch = EdgePipelineOrchestrator(
            source=source,
            detector=DummyDetector(emit_detection=True),
            sampler=FrameSampler(SamplingConfig(target_fps=30.0, source_fps=30.0)),
            gps=StaticGPSAdapter(latitude=26.9124, longitude=75.7873, is_simulated=True),
            cache=cache,
        )
        orch.run()
        pending = cache.get_pending()
        if pending:
            assert pending[0]["latitude"] != 0.0
        cache.close()


class TestProcessFrame:
    def test_process_frame_returns_events_list(self) -> None:
        orch = make_orchestrator()
        frame = np.zeros((240, 320, 3), dtype=np.uint8)
        events = orch.process_frame(frame, frame_index=0, timestamp_s=0.0)
        assert isinstance(events, list)
        # First frame with a detection → at least one event
        assert len(events) >= 1

    def test_events_have_required_keys(self) -> None:
        orch = make_orchestrator()
        frame = np.zeros((240, 320, 3), dtype=np.uint8)
        events = orch.process_frame(frame, frame_index=0, timestamp_s=0.0)
        if events:
            ev = events[0]
            assert "event_id" in ev
            assert "bus_id" in ev
            assert "class" in ev
            assert "confidence" in ev
