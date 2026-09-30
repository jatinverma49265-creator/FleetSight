"""
Model registry — maps configuration strings to detector implementations.

Usage (future — once concrete detectors exist)::

    from ml.registry import create_detector
    detector = create_detector("yolo11", weights="weights/yolo11n.pt", device="cuda:0")
    result   = detector.predict(frame)

The registry is intentionally thin: it resolves a string identifier to a
class, instantiates it and calls ``load()``.  The actual model code lives
in dedicated modules (e.g. ``ml.models.yolo11``).

**No weights are downloaded in this module.**
"""

from __future__ import annotations

from pathlib import Path

from ml.detector import Detector

# ---------------------------------------------------------------------------
# Registry map — populated as concrete backends are implemented.
# ---------------------------------------------------------------------------

_REGISTRY: dict[str, type[Detector]] = {}


def register_detector(name: str, cls: type[Detector]) -> None:
    """Register a detector class under a short name."""
    _REGISTRY[name.lower()] = cls


def available_detectors() -> list[str]:
    """Return the names of all registered detector backends."""
    return sorted(_REGISTRY.keys())


def create_detector(
    name: str,
    *,
    weights: str | Path = "",
    device: str = "cpu",
) -> Detector:
    """
    Instantiate and load a detector by its registered name.

    Parameters
    ----------
    name:
        One of the keys returned by ``available_detectors()``.
    weights:
        Path to the model weights file.
    device:
        PyTorch-style device string (``"cpu"``, ``"cuda:0"``, …).

    Raises
    ------
    KeyError
        If *name* is not a registered detector.
    FileNotFoundError
        If *weights* is given but does not exist.
    """
    key = name.lower()
    if key not in _REGISTRY:
        raise KeyError(f"Unknown detector '{name}'. Available: {available_detectors()}")

    weights_path = Path(weights) if weights else Path()
    if weights and not weights_path.exists():
        from ml.datasets.exceptions import ModelWeightsMissingError

        raise ModelWeightsMissingError(name, str(weights_path))

    detector = _REGISTRY[key]()
    if weights:
        detector.load(weights_path, device=device)
    return detector
