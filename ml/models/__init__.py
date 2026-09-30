"""
FleetSight Model Backends Package.

Exposes concrete detector adapters for YOLO11, YOLO12, and YOLO26,
registering them with ml.registry on import.
"""

from __future__ import annotations

from ml.models.base import BaseYOLOAdapter
from ml.models.yolo11 import YOLO11Detector
from ml.models.yolo12 import YOLO12Detector
from ml.models.yolo26 import YOLO26Detector

__all__ = [
    "BaseYOLOAdapter",
    "YOLO11Detector",
    "YOLO12Detector",
    "YOLO26Detector",
]
