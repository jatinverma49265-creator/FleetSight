"""Tests for edge video sources (Local file, Simulated dashcam, and RTSP stream)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from edge.exceptions import RTSPConnectionError, VideoSourceNotFoundError
from edge.interfaces import VideoSource
from edge.sources import FileVideoSource, RTSPVideoSource, SimulatedVideoSource


class TestVideoSources:
    def test_file_source_missing_file_raises_error(self) -> None:
        with pytest.raises(VideoSourceNotFoundError, match="Video file does not exist"):
            FileVideoSource(Path("non_existent_video.mp4"))

    def test_simulated_video_source_protocol_and_generation(self) -> None:
        source = SimulatedVideoSource(
            bus_id="BUS-TEST",
            camera_id="CAM-FRONT",
            fps=20.0,
            width=320,
            height=240,
            total_frames=10,
            defect_interval=5,
        )
        assert isinstance(source, VideoSource)
        assert source.fps == 20.0
        assert source.frame_count == 10
        assert source.is_opened

        frames_read = 0
        while True:
            ok, frame = source.read()
            if not ok:
                break
            assert frame.shape == (240, 320, 3)
            assert frame.dtype == np.uint8
            frames_read += 1

        assert frames_read == 10
        assert source.current_frame_index == 10
        assert source.current_timestamp_s == 0.5  # 10 frames / 20 fps

        # Test EOF
        ok_eof, _ = source.read()
        assert not ok_eof

        # Test reset / open
        source.open("dummy")
        assert source.current_frame_index == 0
        ok_reset, frame_reset = source.read()
        assert ok_reset
        assert frame_reset.shape == (240, 320, 3)

        source.release()
        assert not source.is_opened

    def test_simulated_video_source_generator(self) -> None:
        source = SimulatedVideoSource(total_frames=5)
        frames = list(source.frames())
        assert len(frames) == 5

    def test_rtsp_source_invalid_url_format(self) -> None:
        with pytest.raises(RTSPConnectionError, match="Invalid RTSP URL format"):
            RTSPVideoSource(rtsp_url="ftp://invalid-protocol.com")

    def test_rtsp_source_unreachable_stream_raises_connection_error(self) -> None:
        with pytest.raises(RTSPConnectionError, match="Connection failed"):
            RTSPVideoSource(
                rtsp_url="rtsp://127.0.0.1:9999/live",
                timeout_seconds=0.2,
            )
