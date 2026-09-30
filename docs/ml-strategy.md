# FleetSight — Machine Learning Strategy & Benchmarking

> **Document Status**: ML ARCHITECTURAL SPECIFICATION & BENCHMARK HARNESS (LOOP 2 IMPLEMENTATION)  
> **Claim Status**: TARGET SPECIFICATIONS & MEASUREMENT PROTOCOL (NO FABRICATED BENCHMARKS)

---

## 1. Multi-Model Architecture & Abstraction

FleetSight does not hardcode edge computer vision to any single YOLO version or proprietary model architecture. Instead, an explicit runtime abstraction (`ml.detector.Detector` protocol) decouples application detection logic from the model provider.

### Model Candidates Under Evaluation:
1. **YOLO11** (`ml.models.YOLO11Detector`):
   - Baseline candidate for edge compute due to mature export tooling (ONNX, TensorRT, CoreML) and established operational efficiency.
2. **YOLO12** (`ml.models.YOLO12Detector`):
   - Evaluated as an **experimental candidate**. Features attention-centric architectural modifications. Must be benchmarked empirically on target edge hardware rather than presumed superior.
3. **YOLO26** (`ml.models.YOLO26Detector`):
   - Advanced research candidate for end-to-end NMS-free and low-power architectures as open specifications solidify.

All candidate models implement the `Detector` protocol:
- Properties: `model_name`, `model_version`, `is_loaded`
- Methods: `load(weights_path, device)`, `predict(frame, confidence_threshold)`, `warmup(imgsz)`

---

## 2. Evidence-Based Selection Methodology

No model will be designated as the "production winner" based on marketing claims or generic public benchmarks. Selection will be determined entirely by an empirical benchmarking harness run on our designated edge compute target.

### Standardized Metric Definitions (`ml.metrics`):
Every benchmark records the following 8 standardized metrics, strictly delineated by provenance status:

| Metric | Type | Unit | Description |
|---|---|---|---|
| **mAP@0.5** | Accuracy | `[0.0, 1.0]` | Mean average precision at IoU=0.50 threshold |
| **Precision** | Accuracy | `[0.0, 1.0]` | True positives / total positive detections |
| **Recall** | Accuracy | `[0.0, 1.0]` | True positives / total ground-truth instances |
| **F1** | Accuracy | `[0.0, 1.0]` | Harmonic mean of precision and recall: `2*(P*R)/(P+R)` |
| **Latency** | Efficiency | `ms` | Per-frame latency distribution (p50, p95, p99) under sustained load |
| **FPS** | Efficiency | `frames/sec` | Continuous sustained throughput on edge device |
| **Model Size** | Efficiency | `MB` | On-disk checkpoint / runtime memory footprint |
| **Memory** | Efficiency | `MB` | Peak VRAM / RAM allocation during continuous inference |

### Metric Status Governance:
To prevent inflated or fabricated performance claims, every metric reported in FleetSight is tagged with a `MetricStatus`:
- `MEASURED`: Empirically validated on hardware using ground-truth test data.
- `TARGET`: Design requirement / engineering acceptance threshold.
- `UNAVAILABLE`: Not yet measured or checkpoint not locally present.

---

## 3. Standardized Comparative Benchmark Report

The `BenchmarkReport` container (`ml.metrics.BenchmarkReport`) aggregates candidate evaluation results and serializes to JSON and comparative Markdown tables:

```python
from ml.metrics import BenchmarkReport, ModelBenchmarkResult, AccuracyMetrics, PerformanceMetrics, MetricStatus

report = BenchmarkReport()
report.add_result(ModelBenchmarkResult(
    model_name="yolo11",
    model_version="yolo11-v0.1.0",
    dataset_name="rdd2022",
    dataset_version="2022.1",
    accuracy=AccuracyMetrics(status=MetricStatus.TARGET, map_50=0.70),
    performance=PerformanceMetrics(status=MetricStatus.TARGET, fps=30.0),
))
```

---

## 4. Configuration Schema (`ml.config`)

Hyperparameters and environmental configurations are centralized in typed Pydantic models:
- `InferenceConfig`: Runtime resolution, confidence threshold (default 0.25), IoU cutoff (default 0.45), FP16 half precision, tracking enablement.
- `TrainingConfig`: Model family, epochs (default 100), batch size, image size (640), learning rate, patience (20), checkpoint intervals.
- `EvaluationConfig`: Test split selection, IoU thresholds, batch size, evaluation output directory.
- `BenchmarkConfig`: Candidate model list, test dataset path, target FPS (15.0), max latency (66.7 ms), warmup iterations (50).

---

## 5. Running ML and Dataset Tests

Execute the complete ML pipeline test suite via pytest:

```bash
# Run all ML and dataset tests
pytest tests/test_dataset_manifest.py tests/test_class_mappings.py tests/test_dataset_split.py tests/test_annotation_validator.py tests/test_model_adapters.py tests/test_ml_configs_and_metrics.py -v

# Run with coverage report
pytest --cov=ml --cov=backend tests/
```
