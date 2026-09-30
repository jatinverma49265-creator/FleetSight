"""
YOLO11 Concrete Detector Adapter.

Represents the primary edge-optimized baseline candidate under evaluation.
Final production suitability is determined strictly by empirical benchmarking.
"""

from __future__ import annotations

from ml.models.base import BaseYOLOAdapter
from ml.registry import register_detector


class YOLO11Detector(BaseYOLOAdapter):
    """YOLO11 edge detection backend candidate."""

    def __init__(self) -> None:
        super().__init__(model_name="yolo11", model_version="yolo11-v0.1.0")


# Register with model registry
register_detector("yolo11", YOLO11Detector)
register_detector("yolo11-n", YOLO11Detector)
register_detector("yolo11-s", YOLO11Detector)
