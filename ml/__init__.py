"""
FleetSight ML Package.

Model abstraction, registry, dataset manifests, split logic,
annotation validation, training/inference configs, and metrics.
"""

from __future__ import annotations

from ml import models as models  # Ensures backends are registered in ml.registry
from ml.detector import Detection, Detector, FrameResult
from ml.metrics import (
    AccuracyMetrics,
    BenchmarkReport,
    HardwareContext,
    MetricStatus,
    ModelBenchmarkResult,
    PerformanceMetrics,
)
from ml.registry import available_detectors, create_detector, register_detector

__all__ = [
    "AccuracyMetrics",
    "BenchmarkReport",
    "Detection",
    "Detector",
    "FrameResult",
    "HardwareContext",
    "MetricStatus",
    "ModelBenchmarkResult",
    "PerformanceMetrics",
    "available_detectors",
    "create_detector",
    "register_detector",
]
