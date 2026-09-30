"""
RTSP Network Video Stream Source Adapter.

Safe boundary adapter for network IP / on-bus RTSP camera streams.
Handles connection setup, timeouts, and explicit error reporting without
requiring a physical RTSP server in test/development environments.
"""

from __future__ import annotations

import contextlib
import os
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import numpy as np

from edge.exceptions import RTSPConnectionError, VideoSourceError
from edge.interfaces import VideoSource


class RTSPVideoSource(VideoSource):
    """Network camera source reading an RTSP video stream."""

    def __init__(
        self,
        rtsp_url: str = "",
        timeout_seconds: float = 3.0,
        reconnect_attempts: int = 1,
    ) -> None:
        self._rtsp_url = rtsp_url
        self._timeout_seconds = timeout_seconds
        self._reconnect_attempts = reconnect_attempts
        self._cap: Any = None
        self._fps: float = 30.0
        self._current_index: int = 0
        self._is_opened: bool = False

        if rtsp_url:
            self.open(rtsp_url)

    @property
    def fps(self) -> float:
        return self._fps

    @property
    def current_frame_index(self) -> int:
        return self._current_index

    @property
    def is_opened(self) -> bool:
        return self._is_opened

    def open(self, source: str | int | Path) -> None:
        """
        Connect to an RTSP stream.

        Raises:
            RTSPConnectionError: If network stream cannot be reached or times out.
            VideoSourceError: If OpenCV is not available.
        """
        self.release()
        url = str(source)
        if not url.startswith(("rtsp://", "rtsps://", "http://", "https://")):
            raise RTSPConnectionError(
                f"Invalid RTSP URL format '{url}'. Expected rtsp:// or rtsps://"
            )

        try:
            import cv2

            # Configure OpenCV FFMPEG network timeout via environment/properties
            os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = (
                f"timeout;{int(self._timeout_seconds * 1000000)}"
            )

            self._cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
            if not self._cap.isOpened():
                raise RTSPConnectionError(
                    f"Connection failed: unable to establish RTSP stream to '{url}' "
                    f"within {self._timeout_seconds}s timeout."
                )

            raw_fps = float(self._cap.get(cv2.CAP_PROP_FPS))
            self._fps = raw_fps if raw_fps > 0.0 else 30.0
            self._rtsp_url = url
            self._current_index = 0
            self._is_opened = True
        except ImportError:
            raise VideoSourceError("OpenCV (cv2) is required for RTSP video capture.")
        except RTSPConnectionError:
            raise
        except Exception as e:
            raise RTSPConnectionError(f"RTSP connection error on '{url}': {e}") from e

    def read(self) -> tuple[bool, np.ndarray]:
        """Read latest frame from network stream."""
        if not self._is_opened or self._cap is None:
            return False, np.zeros((0, 0, 3), dtype=np.uint8)

        ret, frame = self._cap.read()
        if not ret or frame is None:
            return False, np.zeros((0, 0, 3), dtype=np.uint8)

        self._current_index += 1
        return True, frame

    def release(self) -> None:
        """Close RTSP connection and release sockets."""
        if self._cap is not None:
            with contextlib.suppress(Exception):
                self._cap.release()
            self._cap = None
        self._is_opened = False
        self._current_index = 0

    def frames(self) -> Iterator[np.ndarray]:
        """Stream frames sequentially until closed or disconnected."""
        while self._is_opened:
            ok, frame = self.read()
            if not ok:
                break
            yield frame
