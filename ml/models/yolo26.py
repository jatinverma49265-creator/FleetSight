"""
YOLO26 Concrete Detector Adapter.

Represents a future/speculative edge candidate targeting NMS-free, ultra-low-power
inference on next-generation automotive compute platforms.
"""

from __future__ import annotations

from ml.models.base import BaseYOLOAdapter
from ml.registry import register_detector


class YOLO26Detector(BaseYOLOAdapter):
    """YOLO26 speculative low-power edge detection candidate."""

    def __init__(self) -> None:
        super().__init__(model_name="yolo26", model_version="yolo26-v0.1.0-speculative")


# Register with model registry
register_detector("yolo26", YOLO26Detector)
register_detector("yolo26-n", YOLO26Detector)
register_detector("yolo26-s", YOLO26Detector)
