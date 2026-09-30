"""Tests for edge frame sampling subsystem."""

from __future__ import annotations

import numpy as np
import pytest

from edge.exceptions import FrameSamplingError
from edge.sampling import FrameSampler, SampledFrame, SamplingConfig


class TestSamplingConfig:
    def test_default_config_is_valid(self) -> None:
        cfg = SamplingConfig()
        assert cfg.target_fps == 6.0
        assert cfg.source_fps == 30.0
        assert cfg.enabled is True
        assert cfg.drop_duplicate_timestamps is True

    def test_custom_config(self) -> None:
        cfg = SamplingConfig(target_fps=10.0, source_fps=25.0)
        assert cfg.target_fps == 10.0
        assert cfg.source_fps == 25.0

    def test_zero_target_fps_raises(self) -> None:
        with pytest.raises((ValueError, FrameSamplingError)):
            SamplingConfig(target_fps=0.0)

    def test_negative_source_fps_raises(self) -> None:
        with pytest.raises((ValueError, FrameSamplingError)):
            SamplingConfig(source_fps=-5.0)


class TestFrameSampler:
    def test_basic_downsampling_index_mode(self) -> None:
        """30 fps source, 6 fps target → sample every 5th frame."""
        sampler = FrameSampler(SamplingConfig(target_fps=6.0, source_fps=30.0))
        selected = [i for i in range(30) if sampler.should_sample(i)]
        # At step=5, frames 0,5,10,15,20,25 should be selected
        assert len(selected) == 6
        assert 0 in selected

    def test_target_fps_equals_source_fps_samples_all(self) -> None:
        sampler = FrameSampler(SamplingConfig(target_fps=15.0, source_fps=15.0))
        sampler.reset()
        selected = [i for i in range(15) if sampler.should_sample(i)]
        assert len(selected) == 15

    def test_target_fps_exceeds_source_samples_all(self) -> None:
        """If target > source, every frame should be sampled."""
        sampler = FrameSampler(SamplingConfig(target_fps=30.0, source_fps=10.0))
        sampler.reset()
        selected = [i for i in range(10) if sampler.should_sample(i)]
        assert len(selected) == 10

    def test_disabled_sampling_passes_all_frames(self) -> None:
        sampler = FrameSampler(SamplingConfig(target_fps=1.0, source_fps=30.0, enabled=False))
        selected = [i for i in range(30) if sampler.should_sample(i)]
        assert len(selected) == 30

    def test_timestamp_based_sampling(self) -> None:
        """With timestamps: 6 fps target from 30 fps source → accept every ~0.167s."""
        sampler = FrameSampler(SamplingConfig(target_fps=6.0, source_fps=30.0))
        sampler.reset()
        selected = []
        for i in range(30):
            ts = i / 30.0
            if sampler.should_sample(i, timestamp_s=ts):
                selected.append(i)
        # Should select approximately 6 frames over 1 second
        assert 5 <= len(selected) <= 8

    def test_duplicate_timestamps_rejected(self) -> None:
        sampler = FrameSampler(
            SamplingConfig(target_fps=6.0, source_fps=30.0, drop_duplicate_timestamps=True)
        )
        sampler.reset()
        # Frame 0, timestamp 0.0 — should be selected
        assert sampler.should_sample(0, timestamp_s=0.0)
        # Same timestamp again — should be rejected
        assert not sampler.should_sample(1, timestamp_s=0.0)

    def test_reset_clears_state(self) -> None:
        sampler = FrameSampler()
        sampler.should_sample(0, timestamp_s=0.0)
        sampler.reset()
        assert sampler.frames_evaluated == 0
        assert sampler.frames_selected == 0

    def test_process_frame_returns_sampled_frame(self) -> None:
        sampler = FrameSampler(SamplingConfig(target_fps=30.0, source_fps=30.0))
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        result = sampler.process_frame(frame, frame_index=0, timestamp_s=0.0)
        assert result is not None
        assert isinstance(result, SampledFrame)
        assert result.original_frame_index == 0
        assert result.is_sampled is True

    def test_process_frame_returns_none_when_skipped(self) -> None:
        sampler = FrameSampler(SamplingConfig(target_fps=1.0, source_fps=30.0))
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # First frame is always sampled; subsequent ones within the interval are skipped
        sampler.process_frame(frame, 0, timestamp_s=0.0)
        result = sampler.process_frame(frame, 1, timestamp_s=0.01)
        assert result is None

    def test_telemetry_counters(self) -> None:
        sampler = FrameSampler(SamplingConfig(target_fps=6.0, source_fps=30.0))
        for i in range(30):
            sampler.should_sample(i)
        assert sampler.frames_evaluated == 30
        assert sampler.frames_selected > 0
        assert sampler.frames_selected <= 30
