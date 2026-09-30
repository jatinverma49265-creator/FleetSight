"""
Local Video File Source.

Reads MP4, AVI, and other standard video formats using OpenCV, exposing frames
sequentially with frame indices and timestamp estimation.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any

import numpy as np

from edge.exceptions import VideoSourceError, VideoSourceNotFoundError
from edge.interfaces import VideoSource


class FileVideoSource(VideoSource):
    """Sequential frame source for local video recordings."""

    def __init__(self, file_path: str | Path | None = None) -> None:
        self._source_path: Path | None = None
        self._cap: Any = None
        self._fps: float = 30.0
        self._frame_count: int = 0
        self._current_index: int = 0
        self._is_opened: bool = False

        if file_path is not None:
            self.open(file_path)

    @property
    def fps(self) -> float:
        return self._fps

    @property
    def frame_count(self) -> int:
        return self._frame_count

    @property
    def current_frame_index(self) -> int:
        return self._current_index

    @property
    def current_timestamp_s(self) -> float:
        if self._fps <= 0.0:
            return 0.0
        return self._current_index / self._fps

    @property
    def is_opened(self) -> bool:
        return self._is_opened

    def open(self, source: str | int | Path) -> None:
        """
        Open a local video file.

        Raises:
            VideoSourceNotFoundError: If the file path does not exist.
            VideoSourceError: If OpenCV fails to open the file.
        """
        self.release()

        path = Path(source) if isinstance(source, (str, Path)) else None
        if path is not None and not path.exists():
            raise VideoSourceNotFoundError(f"Video file does not exist: {path}")

        try:
            import cv2

            self._cap = cv2.VideoCapture(str(source))
            if not self._cap.isOpened():
                raise VideoSourceError(f"OpenCV could not open video source: {source}")

            raw_fps = float(self._cap.get(cv2.CAP_PROP_FPS))
            self._fps = raw_fps if raw_fps > 0.0 else 30.0
            self._frame_count = int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self._source_path = path
            self._current_index = 0
            self._is_opened = True
        except ImportError:
            raise VideoSourceError("OpenCV (cv2) is required to read video files.")
        except VideoSourceError:
            raise
        except Exception as e:
            raise VideoSourceError(f"Unexpected error opening video source '{source}': {e}") from e

    def read(self) -> tuple[bool, np.ndarray]:
        """
        Read the next sequential frame.

        Returns:
            (success, frame) where frame is (H, W, 3) BGR uint8 or empty array on EOF.
        """
        if not self._is_opened or self._cap is None:
            return False, np.zeros((0, 0, 3), dtype=np.uint8)

        ret, frame = self._cap.read()
        if not ret or frame is None:
            return False, np.zeros((0, 0, 3), dtype=np.uint8)

        self._current_index += 1
        return True, frame

    def release(self) -> None:
        """Release video capture resources."""
        if self._cap is not None:
            try:
                self._cap.release()
            except Exception:
                pass
            self._cap = None
        self._is_opened = False
        self._current_index = 0

    def frames(self) -> Iterator[np.ndarray]:
        """Iterate over all frames in the video until exhausted."""
        while self._is_opened:
            ok, frame = self.read()
            if not ok:
                break
            yield frame
