"""
FleetSight ML Metrics & Benchmark Reporting.

Defines typed, auditable representations for detection accuracy and edge efficiency metrics.
Strictly differentiates measured values, target requirements, and unmeasured/unavailable states
to ensure absolute benchmark claim integrity.
"""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class MetricStatus(StrEnum):
    """
    Provenance status for an ML metric value.

    Guarantees that target design criteria or simulated estimates are never
    presented or reported as empirically measured benchmarks.
    """

    MEASURED = "measured"  # Empirically measured during a validated benchmark run
    TARGET = "target"  # Design requirement / engineering acceptance target
    UNAVAILABLE = "unavailable"  # Not yet measured or checkpoint not present locally


class AccuracyMetrics(BaseModel):
    """Computer vision detection accuracy metrics."""

    status: MetricStatus = Field(
        default=MetricStatus.UNAVAILABLE,
        description="Whether values are measured or target specifications",
    )
    map_50: float | None = Field(default=None, ge=0.0, le=1.0, description="mAP at IoU=0.50")
    map_50_95: float | None = Field(
        default=None, ge=0.0, le=1.0, description="mAP across IoU 0.50:0.95"
    )
    precision: float | None = Field(default=None, ge=0.0, le=1.0)
    recall: float | None = Field(default=None, ge=0.0, le=1.0)
    f1: float | None = Field(default=None, ge=0.0, le=1.0)
    per_class_recall: dict[str, float] = Field(
        default_factory=dict,
        description="Per-hazard recall (e.g. pothole, alligator_crack)",
    )

    model_config = ConfigDict(extra="ignore")

    @classmethod
    def calculate_f1(cls, precision: float, recall: float) -> float:
        """Calculate harmonic mean F1 from precision and recall."""
        if precision + recall <= 0.0:
            return 0.0
        return round(2.0 * (precision * recall) / (precision + recall), 4)


class PerformanceMetrics(BaseModel):
    """Hardware resource utilization and latency efficiency metrics."""

    status: MetricStatus = Field(
        default=MetricStatus.UNAVAILABLE,
        description="Whether values are measured or target specifications",
    )
    latency_ms_p50: float | None = Field(
        default=None, ge=0.0, description="Median latency per frame in ms"
    )
    latency_ms_p95: float | None = Field(
        default=None, ge=0.0, description="95th percentile latency in ms"
    )
    latency_ms_p99: float | None = Field(
        default=None, ge=0.0, description="99th percentile latency in ms"
    )
    fps: float | None = Field(default=None, ge=0.0, description="Frames processed per second")
    model_size_mb: float | None = Field(
        default=None, ge=0.0, description="Disk / binary footprint in MB"
    )
    peak_memory_mb: float | None = Field(
        default=None, ge=0.0, description="Peak RAM / VRAM consumption in MB"
    )

    model_config = ConfigDict(extra="ignore")


class HardwareContext(BaseModel):
    """Hardware and environment telemetry under which a benchmark was conducted."""

    device_name: str = Field(default="cpu")
    cpu_model: str = Field(default="")
    gpu_model: str = Field(default="")
    ram_total_gb: float = Field(default=0.0, ge=0.0)
    vram_total_gb: float = Field(default=0.0, ge=0.0)
    os_platform: str = Field(default="")

    model_config = ConfigDict(extra="ignore")


class ModelBenchmarkResult(BaseModel):
    """Consolidated benchmark evaluation result for a single candidate model."""

    model_name: str = Field(
        ..., min_length=1, description="Model key (e.g. yolo11, yolo12, yolo26)"
    )
    model_version: str = Field(..., min_length=1)
    dataset_name: str = Field(..., min_length=1)
    dataset_version: str = Field(..., min_length=1)
    accuracy: AccuracyMetrics = Field(default_factory=AccuracyMetrics)
    performance: PerformanceMetrics = Field(default_factory=PerformanceMetrics)
    hardware: HardwareContext = Field(default_factory=HardwareContext)
    inference_config: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    notes: str = Field(
        default="", description="Experimental conditions, thermal state, or observations"
    )

    model_config = ConfigDict(extra="ignore")


class BenchmarkReport(BaseModel):
    """Standardized report comparing candidate models under uniform benchmark conditions."""

    report_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    methodology: str = Field(
        default=(
            "Measured on route/day-isolated split with thermal stability protocol. "
            "No fabricated claims."
        ),
    )
    results: list[ModelBenchmarkResult] = Field(default_factory=list)

    model_config = ConfigDict(extra="ignore")

    def add_result(self, result: ModelBenchmarkResult) -> None:
        """Append a model benchmark result."""
        self.results.append(result)

    def to_markdown(self) -> str:
        """Render a comparative markdown table clearly delineating status."""
        header_cols = [
            "Model", "Dataset", "Acc Status", "mAP@0.5", "Precision",
            "Recall", "F1", "Perf Status", "Latency p95", "FPS", "Model Size", "Peak Memory",
        ]
        table_header = "| " + " | ".join(header_cols) + " |"
        table_separator = "| " + " | ".join(["---"] * len(header_cols)) + " |"

        lines: list[str] = [
            f"# FleetSight Model Benchmark Report (`{self.report_id}`)",
            f"**Generated**: {self.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"**Methodology**: {self.methodology}",
            "",
            table_header,
            table_separator,
        ]

        def _fmt(val: float | None, unit: str = "") -> str:
            if val is None:
                return "N/A"
            return f"{val:.2f}{unit}"

        for r in self.results:
            acc = r.accuracy
            perf = r.performance
            row = (
                f"| {r.model_name} ({r.model_version}) | {r.dataset_name}:{r.dataset_version} "
                f"| {acc.status.value.upper()} "
                f"| {_fmt(acc.map_50)} "
                f"| {_fmt(acc.precision)} "
                f"| {_fmt(acc.recall)} "
                f"| {_fmt(acc.f1)} "
                f"| {perf.status.value.upper()} "
                f"| {_fmt(perf.latency_ms_p95, ' ms')} "
                f"| {_fmt(perf.fps)} "
                f"| {_fmt(perf.model_size_mb, ' MB')} "
                f"| {_fmt(perf.peak_memory_mb, ' MB')} |"
            )
            lines.append(row)

        lines.append("")
        lines.append("> [!NOTE]")
        lines.append(
            "> Status tags: `MEASURED` = empirical hardware test; "
            "`TARGET` = engineering goal; `UNAVAILABLE` = pending benchmark."
        )
        return "\n".join(lines)


    def save_to_json(self, path: Path | str) -> None:
        """Persist report to a JSON file."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", encoding="utf-8") as f:
            f.write(self.model_dump_json(indent=2))

    @classmethod
    def load_from_json(cls, path: Path | str) -> BenchmarkReport:
        """Load report from a JSON file."""
        p = Path(path)
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)
