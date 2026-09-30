"""
YOLO12 Concrete Detector Adapter.

Represents an experimental attention-centric candidate under benchmark evaluation.
Subject to hardware acceleration and thermal tests before any production adoption.
"""

from __future__ import annotations

from ml.models.base import BaseYOLOAdapter
from ml.registry import register_detector


class YOLO12Detector(BaseYOLOAdapter):
    """YOLO12 experimental detection backend candidate."""

    def __init__(self) -> None:
        super().__init__(model_name="yolo12", model_version="yolo12-v0.1.0-exp")


# Register with model registry
register_detector("yolo12", YOLO12Detector)
register_detector("yolo12-n", YOLO12Detector)
register_detector("yolo12-s", YOLO12Detector)
