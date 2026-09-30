"""
Benchmark Pipeline Configuration Schema.

Governs standardized comparative evaluation across candidate models (YOLO11, YOLO12, YOLO26)
on consistent hardware and test splits.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class BenchmarkConfig(BaseModel):
    """Specification for running evidence-based comparative model benchmarks."""

    models: list[str] = Field(
        default_factory=lambda: ["yolo11", "yolo12", "yolo26"],
        description="Candidate models to benchmark",
    )
    dataset_name: str = Field(
        default="jaipur_custom",
        description="Primary test dataset for comparison",
    )
    test_split_path: str = Field(
        default="data/local/jaipur/splits/test.txt",
        description="Route/day isolated test split file",
    )
    warmup_frames: int = Field(default=50, ge=0, description="Frames discarded to prime GPU caches")
    benchmark_frames: int = Field(default=1000, ge=10, description="Sequential frames evaluated")
    device: str = Field(default="cpu", description="Hardware device ('cpu', 'cuda:0', 'jetson')")

    # Threshold criteria (targets for edge viability, not claimed measurements)
    target_min_fps: float = Field(
        default=15.0, description="Minimum acceptable FPS on edge hardware"
    )
    target_max_latency_ms: float = Field(
        default=66.7, description="Maximum acceptable p95 latency in ms"
    )
    target_max_memory_mb: float = Field(default=2048.0, description="Maximum peak memory in MB")

    report_output_dir: str = Field(
        default="reports/benchmarks",
        description="Directory for JSON and markdown benchmark reports",
    )

    model_config = ConfigDict(extra="ignore")
