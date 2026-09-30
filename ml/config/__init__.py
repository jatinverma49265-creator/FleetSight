"""
FleetSight ML Configuration Package.

Exposes structured Pydantic configurations for training, evaluation,
inference, and comparative benchmarking.
"""

from __future__ import annotations

from ml.config.benchmark import BenchmarkConfig
from ml.config.evaluation import EvaluationConfig
from ml.config.inference import InferenceConfig
from ml.config.training import TrainingConfig

__all__ = [
    "BenchmarkConfig",
    "EvaluationConfig",
    "InferenceConfig",
    "TrainingConfig",
]
