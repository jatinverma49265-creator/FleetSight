"""
Edge Pipeline Orchestrator.

Central coordinating engine on the bus edge compute unit.
Chains:
  VideoSource
  → Frame Sampler (5-10 FPS downsampling)
  → ML Inference Adapter (Detector Protocol)
  → Centroid Tracking (cross-frame association)
  → Spatial/Temporal Deduplication
  → Privacy Filter Hook (de-identification BEFORE storage)
  → Canonical Event Construction
  → Offline SQLite Event Cache

Uses strict dependency injection: decouples all computer vision, hardware, and persistence backends.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np

from edge.cache import SQLiteEventCache
from edge.deduplication import SpatialTemporalDeduplicator
from edge.event_builder import DefaultEventBuilder
from edge.exceptions import EdgeError
from edge.gps import UnavailableGPSAdapter
from edge.interfaces import (
    EventBuilder,
    EventCache,
    GPSAdapter,
    PrivacyFilter,
    TrackerAdapter,
    VideoSource,
)
from edge.privacy import NoOpPrivacyFilter
from edge.sampling import FrameSampler, SamplingConfig
from edge.telemetry import PipelineTelemetry
from edge.tracking import CentroidTracker
from ml.detector import Detection, Detector, FrameResult

logger = logging.getLogger(__name__)


class EdgePipelineOrchestrator:
    """
    Coordinates edge inference, tracking, deduplication, and caching on an on-bus device.
    """

    def __init__(
        self,
        source: VideoSource,
        detector: Detector,
        sampler: FrameSampler | None = None,
        tracker: TrackerAdapter | None = None,
        deduplicator: SpatialTemporalDeduplicator | None = None,
        privacy_filter: PrivacyFilter | None = None,
        event_builder: EventBuilder | None = None,
        cache: EventCache | None = None,
        gps: GPSAdapter | None = None,
        bus_id: str = "BUS-001",
        camera_id: str = "CAM-FRONT-01",
        confidence_threshold: float = 0.25,
        evidence_dir: Path | str | None = None,
    ) -> None:
        self.source = source
        self.detector = detector
        self.sampler = sampler or FrameSampler(SamplingConfig(target_fps=6.0, source_fps=30.0))
        self.tracker = tracker or CentroidTracker()
        self.deduplicator = deduplicator or SpatialTemporalDeduplicator()
        self.privacy_filter = privacy_filter or NoOpPrivacyFilter()
        self.event_builder = event_builder or DefaultEventBuilder()
        self.cache = cache or SQLiteEventCache()
        self.gps = gps or UnavailableGPSAdapter()

        self.bus_id = bus_id
        self.camera_id = camera_id
        self.confidence_threshold = confidence_threshold
        self.evidence_dir = Path(evidence_dir) if evidence_dir else None
        if self.evidence_dir:
            self.evidence_dir.mkdir(parents=True, exist_ok=True)

        self.telemetry = PipelineTelemetry()

    def process_frame(
        self,
        frame: np.ndarray,
        frame_index: int,
        timestamp_s: float,
    ) -> list[dict[str, Any]]:
        """
        Process a single video frame through the complete edge ingestion pipeline.

        Returns:
            List of newly created, novel, and cached event payloads for this frame.
        """
        self.telemetry.frames_received += 1

        # 1. Frame Sampling / Throttling
        if not self.sampler.should_sample(frame_index=frame_index, timestamp_s=timestamp_s):
            return []

        self.telemetry.frames_sampled += 1

        try:
            # 2. ML Detector Forward Pass
            self.telemetry.inference_calls += 1
            frame_result: FrameResult = self.detector.predict(
                frame, confidence_threshold=self.confidence_threshold
            )
            raw_detections: Sequence[Detection] = frame_result.detections
            self.telemetry.detections_found += len(raw_detections)

            # 3. Cross-Frame Tracking Association
            tracked_detections = self.tracker.update(raw_detections)

            # 4. GPS Reading Attachment
            gps_reading = self.gps.latest()
            lat = gps_reading.latitude if gps_reading else None
            lon = gps_reading.longitude if gps_reading else None

            # 5. Spatial-Temporal Deduplication
            novel_tracked = []
            for item in tracked_detections:
                should_emit = self.deduplicator.should_emit(
                    detection_class=item.detection.class_name,
                    track_id=item.track_id,
                    timestamp_s=timestamp_s,
                    latitude=lat,
                    longitude=lon,
                )
                if should_emit:
                    novel_tracked.append(item)
                else:
                    self.telemetry.deduplicated_events += 1

            if not novel_tracked:
                return []

            # 6. Privacy Filter Hook (Obfuscation strictly BEFORE evidence caching)
            evidence_regions = [
                (d.detection.x1, d.detection.y1, d.detection.x2, d.detection.y2)
                for d in novel_tracked
            ]
            anonymized_frame = self.privacy_filter.filter(frame, evidence_regions)

            # Save evidence frame snippet if evidence_dir configured
            evidence_path_str: str | None = None
            if self.evidence_dir and anonymized_frame.size > 0:
                evidence_file = self.evidence_dir / f"ev_{self.bus_id}_{frame_index:06d}.jpg"
                evidence_path_str = str(evidence_file)
                # In production or with opencv, cv2.imwrite(str(evidence_file), anonymized_frame)

            # 7. Canonical Event Construction
            events = self.event_builder.build(
                tracked=novel_tracked,
                gps=gps_reading,
                camera_id=self.camera_id,
                bus_id=self.bus_id,
            )
            self.telemetry.candidate_events += len(events)

            # 8. Local SQLite Cache Persistence
            for ev in events:
                if evidence_path_str and "evidence_uri" in ev:
                    ev["evidence_uri"] = evidence_path_str
                self.cache.push(ev)
                self.telemetry.cached_events += 1

            return events

        except Exception as e:
            self.telemetry.processing_errors += 1
            logger.error("Error processing edge frame %d: %s", frame_index, e, exc_info=True)
            raise EdgeError(f"Orchestration failure at frame {frame_index}: {e}") from e

    def step(self) -> list[dict[str, Any]]:
        """
        Pull one frame from the video source and process it.

        Returns empty list if frame was skipped, duplicate, or on EOF.
        """
        ok, frame = self.source.read()
        if not ok:
            return []

        frame_index = getattr(self.source, "current_frame_index", self.telemetry.frames_received)
        fps = getattr(self.source, "fps", 30.0)
        timestamp_s = frame_index / fps if fps > 0.0 else 0.0

        return self.process_frame(frame, frame_index=frame_index, timestamp_s=timestamp_s)

    def run(self, max_frames: int | None = None) -> PipelineTelemetry:
        """
        Run the pipeline over the video source until exhausted or max_frames reached.

        Returns telemetry counters.
        """
        frames_processed = 0
        while True:
            if max_frames is not None and frames_processed >= max_frames:
                break
            ok, frame = self.source.read()
            if not ok:
                break

            frame_index = getattr(self.source, "current_frame_index", frames_processed)
            fps = getattr(self.source, "fps", 30.0)
            timestamp_s = frame_index / fps if fps > 0.0 else 0.0

            self.process_frame(frame, frame_index=frame_index, timestamp_s=timestamp_s)
            frames_processed += 1

        return self.telemetry
