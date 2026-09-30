"""
Simulated Bus Dashcam Video Source.

Generates deterministic, synthetic road scene frames for testing and demonstration
without requiring physical bus cameras or pre-recorded road footage.
Strictly tagged as simulation to ensure zero confusion with real road data.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import numpy as np

from edge.interfaces import VideoSource


class SimulatedVideoSource(VideoSource):
    """Synthetic frame generator simulating a forward-facing municipal bus dashcam."""

    def __init__(
        self,
        bus_id: str = "SIM-BUS-01",
        camera_id: str = "CAM-FRONT-01",
        fps: float = 30.0,
        width: int = 640,
        height: int = 480,
        total_frames: int = 100,
        defect_interval: int = 20,
    ) -> None:
        self.bus_id = bus_id
        self.camera_id = camera_id
        self._fps = float(fps) if fps > 0 else 30.0
        self.width = width
        self.height = height
        self.total_frames = total_frames
        self.defect_interval = defect_interval

        self._current_index = 0
        self._is_opened = True

    @property
    def fps(self) -> float:
        return self._fps

    @property
    def frame_count(self) -> int:
        return self.total_frames

    @property
    def current_frame_index(self) -> int:
        return self._current_index

    @property
    def current_timestamp_s(self) -> float:
        return self._current_index / self._fps

    @property
    def is_opened(self) -> bool:
        return self._is_opened

    def open(self, source: str | int | Path) -> None:
        """Reset generator state for a simulated run."""
        self._current_index = 0
        self._is_opened = True

    def read(self) -> tuple[bool, np.ndarray]:
        """
        Generate next deterministic simulated road frame.

        Returns:
            (success, frame) where frame is (H, W, 3) BGR uint8 with road-like canvas.
        """
        if not self._is_opened or self._current_index >= self.total_frames:
            return False, np.zeros((0, 0, 3), dtype=np.uint8)

        # Base dark gray asphalt road canvas (BGR = 60, 60, 60)
        frame = np.full((self.height, self.width, 3), 60, dtype=np.uint8)

        # Draw simulated road horizon & perspective lines
        # Upper horizon (sky = light gray/blue: 180, 160, 140)
        horizon_y = int(self.height * 0.4)
        frame[:horizon_y, :] = [180, 160, 140]

        # Center lane dashed marking (yellow: 0, 215, 255)
        lane_w = 6
        center_x = self.width // 2
        # Dashed pattern cycling with frame index
        dash_offset = (self._current_index * 8) % 40
        for y in range(horizon_y, self.height, 40):
            y_start = min(y + dash_offset, self.height)
            y_end = min(y_start + 20, self.height)
            if y_start < self.height:
                half = lane_w // 2
                frame[y_start:y_end, center_x - half : center_x + half] = [0, 215, 255]

        # Periodically insert a simulated dark defect patch (e.g. pothole) for detector testing
        if self.defect_interval > 0 and (self._current_index % self.defect_interval) < 5:
            # Defect patch visible for 5 consecutive frames to test tracking
            px = int(self.width * 0.45)
            py = int(self.height * 0.70)
            frame[py : py + 30, px : px + 50] = [20, 20, 20]

        self._current_index += 1
        return True, frame

    def release(self) -> None:
        """Close simulated source."""
        self._is_opened = False
        self._current_index = 0

    def frames(self) -> Iterator[np.ndarray]:
        """Iterate over all simulated frames until count is reached."""
        while self._is_opened and self._current_index < self.total_frames:
            ok, frame = self.read()
            if not ok:
                break
            yield frame
