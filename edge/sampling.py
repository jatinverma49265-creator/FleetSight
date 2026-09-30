"""
Frame Sampling Subsystem.

Downsamples high-FPS camera streams (e.g. 30 or 60 FPS) to an edge-sustainable
processing rate (target 5-10 FPS) while preserving exact original frame indices
and timestamps without duplicate time drift.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from pydantic import BaseModel, ConfigDict, Field, field_validator

from edge.exceptions import FrameSamplingError


class SamplingConfig(BaseModel):
    """Configuration governing frame sampling and edge throttling."""

    target_fps: float = Field(
        default=6.0,
        gt=0.0,
        description="Desired inference processing rate in frames per second (target 5-10 FPS)",
    )
    source_fps: float = Field(
        default=30.0,
        gt=0.0,
        description="Assumed or reported native camera/video frame rate",
    )
    enabled: bool = Field(default=True, description="Whether to apply downsampling")
    drop_duplicate_timestamps: bool = Field(
        default=True,
        description="Skip frame if timestamp is identical to the previously sampled frame",
    )

    model_config = ConfigDict(extra="ignore")

    @field_validator("target_fps", "source_fps")
    @classmethod
    def validate_positive_fps(cls, v: float) -> float:
        if v <= 0.0:
            raise FrameSamplingError(f"FPS rate must be positive and non-zero; got {v}")
        return v


@dataclass(frozen=True, slots=True)
class SampledFrame:
    """Enriched container for a selected frame passed down the pipeline."""

    frame: np.ndarray
    original_frame_index: int
    timestamp_s: float
    is_sampled: bool = True


class FrameSampler:
    """
    Decides which incoming frames should be forwarded to the ML inference stage.

    Supports both regular frame-index step calculation and timestamp-based interval tracking.
    """

    def __init__(self, config: SamplingConfig | None = None) -> None:
        self.config = config or SamplingConfig()
        self._last_sampled_timestamp: float | None = None
        self._last_sampled_index: int = -1
        self._frames_evaluated: int = 0
        self._frames_selected: int = 0

    @property
    def frames_evaluated(self) -> int:
        return self._frames_evaluated

    @property
    def frames_selected(self) -> int:
        return self._frames_selected

    def reset(self) -> None:
        """Clear internal temporal state."""
        self._last_sampled_timestamp = None
        self._last_sampled_index = -1
        self._frames_evaluated = 0
        self._frames_selected = 0

    def should_sample(
        self,
        frame_index: int,
        timestamp_s: float | None = None,
    ) -> bool:
        """
        Determine whether the frame at `frame_index` / `timestamp_s` should be sampled.
        """
        self._frames_evaluated += 1

        if not self.config.enabled:
            self._frames_selected += 1
            return True

        # If target FPS meets or exceeds source FPS, sample every frame
        if self.config.target_fps >= self.config.source_fps:
            self._frames_selected += 1
            return True

        interval_s = 1.0 / self.config.target_fps

        if timestamp_s is not None:
            # Handle duplicate timestamps
            if (
                self.config.drop_duplicate_timestamps
                and self._last_sampled_timestamp is not None
                and timestamp_s <= self._last_sampled_timestamp
            ):
                return False

            if self._last_sampled_timestamp is None:
                self._last_sampled_timestamp = timestamp_s
                self._last_sampled_index = frame_index
                self._frames_selected += 1
                return True

            # Use time-based windowing with slight floating-point tolerance (10% of frame duration)
            tolerance = 0.1 * (1.0 / self.config.source_fps)
            elapsed = timestamp_s - self._last_sampled_timestamp
            if elapsed >= (interval_s - tolerance):
                self._last_sampled_timestamp = timestamp_s
                self._last_sampled_index = frame_index
                self._frames_selected += 1
                return True
            return False

        # Fallback to index-based deterministic step
        step = round(self.config.source_fps / self.config.target_fps)
        if step <= 1:
            self._frames_selected += 1
            return True

        if frame_index % step == 0:
            self._last_sampled_index = frame_index
            self._frames_selected += 1
            return True

        return False

    def process_frame(
        self,
        frame: np.ndarray,
        frame_index: int,
        timestamp_s: float,
    ) -> SampledFrame | None:
        """
        Evaluate frame; if selected, return SampledFrame, else None.
        """
        if self.should_sample(frame_index=frame_index, timestamp_s=timestamp_s):
            return SampledFrame(
                frame=frame,
                original_frame_index=frame_index,
                timestamp_s=timestamp_s,
                is_sampled=True,
            )
        return None
