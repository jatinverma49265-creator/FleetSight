"""
Edge Privacy Filter Hooks.

Provides interface and reference implementations for de-identifying sensitive imagery
(human faces, vehicle registration plates) at the edge before evidence frames
are persisted to the offline cache or transmitted to central storage.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from edge.interfaces import PrivacyFilter


class NoOpPrivacyFilter(PrivacyFilter):
    """
    Pass-through privacy filter for baseline execution and testing.

    Explicitly does not perform face or license plate redaction.
    Actual automated face/plate detection models will be integrated in future edge loops.
    """

    def filter(
        self,
        frame: np.ndarray,
        regions: Sequence[tuple[float, float, float, float]] | None = None,
    ) -> np.ndarray:
        """Return an unmodified copy of the frame."""
        return frame.copy()


class MockPrivacyFilter(PrivacyFilter):
    """
    Deterministic privacy filter for unit testing.

    Applies a solid pixel block mask or box blur to designated sensitive regions
    to verify pipeline ordering before evidence persistence.
    """

    def __init__(self, mask_color: tuple[int, int, int] = (0, 0, 0)) -> None:
        self.mask_color = mask_color
        self.invocations_count: int = 0

    def filter(
        self,
        frame: np.ndarray,
        regions: Sequence[tuple[float, float, float, float]] | None = None,
    ) -> np.ndarray:
        """
        Apply deterministic masking to specified pixel regions.

        Regions are (x1, y1, x2, y2) in pixel coordinates.
        """
        self.invocations_count += 1
        anonymized = frame.copy()
        if not regions:
            return anonymized

        h, w = anonymized.shape[:2]
        for x1, y1, x2, y2 in regions:
            ix1 = max(0, min(int(round(x1)), w))
            iy1 = max(0, min(int(round(y1)), h))
            ix2 = max(0, min(int(round(x2)), w))
            iy2 = max(0, min(int(round(y2)), h))
            if ix2 > ix1 and iy2 > iy1:
                anonymized[iy1:iy2, ix1:ix2] = self.mask_color

        return anonymized
