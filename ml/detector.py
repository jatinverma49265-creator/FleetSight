"""
FleetSight model abstraction layer.

Defines the ``Detector`` protocol that every model backend must implement,
plus shared data types for inference results.  This abstraction ensures the
CV pipeline can benchmark and switch between YOLO11, YOLO12, YOLO26 (or any
future detector) without scattering model-specific code throughout the system.

**No model weights are downloaded or loaded in this module.**
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol, runtime_checkable

import numpy as np

# ---------------------------------------------------------------------------
# Inference result types
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Detection:
    """A single object detection from one frame."""

    class_id: int
    class_name: str
    confidence: float
    # Bounding box in pixel coordinates (x1, y1, x2, y2).
    x1: float
    y1: float
    x2: float
    y2: float


@dataclass(frozen=True, slots=True)
class FrameResult:
    """All detections from a single frame."""

    detections: Sequence[Detection] = field(default_factory=list)
    inference_time_ms: float = 0.0


# ---------------------------------------------------------------------------
# Detector protocol (interface)
# ---------------------------------------------------------------------------


@runtime_checkable
class Detector(Protocol):
    """
    Abstract detector interface.

    Every concrete model backend (YOLO11Detector, YOLO12Detector, …) must
    satisfy this protocol so the edge pipeline and benchmarking harness can
    treat them interchangeably.
    """

    @property
    def model_name(self) -> str:
        """Human-readable model identifier, e.g. ``'yolo11-n'``."""
        ...

    @property
    def model_version(self) -> str:
        """Versioned string used in event metadata, e.g. ``'yolo11-v0.1.0'``."""
        ...

    def load(self, weights_path: Path, device: str = "cpu") -> None:
        """
        Load model weights from *weights_path* onto *device*.

        Must be called before ``predict``.
        """
        ...

    def predict(
        self,
        frame: np.ndarray,
        confidence_threshold: float = 0.25,
    ) -> FrameResult:
        """
        Run inference on a single BGR frame (H×W×3 uint8 numpy array).

        Returns a ``FrameResult`` containing zero or more ``Detection``
        objects whose confidence ≥ *confidence_threshold*.
        """
        ...

    def warmup(self, imgsz: tuple[int, int] = (640, 640)) -> None:
        """
        Optional warm-up pass to prime GPU / TensorRT / ONNX runtime.

        Implementations may no-op if warm-up is not applicable.
        """
        ...
