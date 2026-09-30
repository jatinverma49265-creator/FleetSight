"""Tests for ML configurations, metrics structures, and benchmark report serialization."""

from __future__ import annotations

from pathlib import Path

from ml.config import (
    BenchmarkConfig,
    EvaluationConfig,
    InferenceConfig,
    TrainingConfig,
)
from ml.metrics import (
    AccuracyMetrics,
    BenchmarkReport,
    HardwareContext,
    MetricStatus,
    ModelBenchmarkResult,
    PerformanceMetrics,
)


class TestMLConfigsAndMetrics:
    def test_configurations_defaults_and_validation(self) -> None:
        inf_cfg = InferenceConfig(model_name="yolo11", conf_threshold=0.30)
        assert inf_cfg.model_name == "yolo11"
        assert inf_cfg.conf_threshold == 0.30
        assert inf_cfg.device == "cpu"

        train_cfg = TrainingConfig(model_family="yolo11", epochs=50)
        assert train_cfg.epochs == 50
        assert train_cfg.batch_size == 16

        eval_cfg = EvaluationConfig(model_name="yolo12", split="test")
        assert eval_cfg.split == "test"
        assert eval_cfg.conf_threshold == 0.001

        bench_cfg = BenchmarkConfig()
        assert "yolo11" in bench_cfg.models
        assert "yolo12" in bench_cfg.models
        assert "yolo26" in bench_cfg.models
        assert bench_cfg.target_min_fps == 15.0

    def test_f1_calculation(self) -> None:
        # Standard harmonic mean
        f1 = AccuracyMetrics.calculate_f1(precision=0.8, recall=0.8)
        assert f1 == 0.8

        f1_diff = AccuracyMetrics.calculate_f1(precision=0.6, recall=0.8)
        assert round(f1_diff, 4) == 0.6857

        # Zero edge case
        assert AccuracyMetrics.calculate_f1(0.0, 0.0) == 0.0
        assert AccuracyMetrics.calculate_f1(0.5, 0.0) == 0.0

    def test_metrics_status_differentiation(self) -> None:
        # Default state is UNAVAILABLE
        acc = AccuracyMetrics()
        assert acc.status == MetricStatus.UNAVAILABLE
        assert acc.map_50 is None

        # Target specification
        target_acc = AccuracyMetrics(
            status=MetricStatus.TARGET, map_50=0.75, precision=0.80, recall=0.70
        )
        assert target_acc.status == MetricStatus.TARGET
        assert target_acc.map_50 == 0.75

        # Measured result
        measured_perf = PerformanceMetrics(
            status=MetricStatus.MEASURED,
            latency_ms_p95=28.4,
            fps=35.2,
            model_size_mb=6.2,
            peak_memory_mb=420.0,
        )
        assert measured_perf.status == MetricStatus.MEASURED
        assert measured_perf.fps == 35.2

    def test_benchmark_report_markdown_and_json_roundtrip(self, tmp_path: Path) -> None:
        report = BenchmarkReport(report_id="test_run_001")

        # Add YOLO11 result
        r_yolo11 = ModelBenchmarkResult(
            model_name="yolo11",
            model_version="yolo11-v0.1.0",
            dataset_name="rdd2022",
            dataset_version="2022.1",
            accuracy=AccuracyMetrics(status=MetricStatus.TARGET, map_50=0.70),
            performance=PerformanceMetrics(
                status=MetricStatus.TARGET, fps=30.0, latency_ms_p95=33.3
            ),
            hardware=HardwareContext(device_name="Jetson Orin Nano"),
            notes="Target acceptance specification",
        )
        report.add_result(r_yolo11)

        # Add YOLO12 result
        r_yolo12 = ModelBenchmarkResult(
            model_name="yolo12",
            model_version="yolo12-v0.1.0-exp",
            dataset_name="rdd2022",
            dataset_version="2022.1",
            accuracy=AccuracyMetrics(status=MetricStatus.UNAVAILABLE),
            performance=PerformanceMetrics(status=MetricStatus.UNAVAILABLE),
            hardware=HardwareContext(device_name="Jetson Orin Nano"),
            notes="Experimental candidate pending hardware benchmark",
        )
        report.add_result(r_yolo12)

        # Check markdown generation
        md = report.to_markdown()
        assert "# FleetSight Model Benchmark Report" in md
        assert "yolo11" in md
        assert "yolo12" in md
        assert "TARGET" in md
        assert "UNAVAILABLE" in md
        assert "No fabricated claims" in md

        # Check JSON roundtrip
        json_file = tmp_path / "benchmark_report.json"
        report.save_to_json(json_file)
        assert json_file.exists()

        reloaded = BenchmarkReport.load_from_json(json_file)
        assert reloaded.report_id == "test_run_001"
        assert len(reloaded.results) == 2
        assert reloaded.results[0].model_name == "yolo11"
        assert reloaded.results[0].accuracy.status == MetricStatus.TARGET
