"""
Edge Pipeline Telemetry & Observability.

Internal execution counters tracking pipeline progression without fabricating
external real-world benchmark metrics.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PipelineTelemetry(BaseModel):
    """Execution telemetry counters for an edge orchestrator session."""

    frames_received: int = Field(default=0, description="Total raw frames from video source")
    frames_sampled: int = Field(default=0, description="Frames selected for inference")
    inference_calls: int = Field(default=0, description="Total detector inference calls")
    detections_found: int = Field(default=0, description="Raw bounding boxes above threshold")
    candidate_events: int = Field(default=0, description="Candidate detection events built")
    deduplicated_events: int = Field(default=0, description="Duplicate events suppressed")
    cached_events: int = Field(default=0, description="Events committed to SQLite cache")
    sync_attempts: int = Field(default=0, description="Batches/events attempted to sync")
    sync_successes: int = Field(default=0, description="Events acknowledged by transport")
    processing_errors: int = Field(default=0, description="Recoverable pipeline errors")

    model_config = ConfigDict(extra="ignore")

    def reset(self) -> None:
        """Reset all counters to zero."""
        self.frames_received = 0
        self.frames_sampled = 0
        self.inference_calls = 0
        self.detections_found = 0
        self.candidate_events = 0
        self.deduplicated_events = 0
        self.cached_events = 0
        self.sync_attempts = 0
        self.sync_successes = 0
        self.processing_errors = 0
