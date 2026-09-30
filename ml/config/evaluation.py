"""
Evaluation Pipeline Configuration Schema.

Defines validation and test set evaluation parameters across detection models.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class EvaluationConfig(BaseModel):
    """Specification for model validation and offline evaluation."""

    model_name: str = Field(default="yolo11", description="Registered model backend identifier")
    weights_path: str = Field(
        default="weights/yolo11n.pt", description="Path to checkpoint under test"
    )
    dataset_yaml: str = Field(
        default="data/rdd2022/dataset.yaml", description="Target dataset configuration"
    )
    split: str = Field(default="val", description="Dataset split to evaluate ('val', 'test')")
    conf_threshold: float = Field(
        default=0.001, ge=0.0, le=1.0, description="Confidence threshold for PR curves"
    )
    iou_threshold: float = Field(
        default=0.60, ge=0.0, le=1.0, description="IoU threshold for mAP calculation"
    )
    imgsz: int = Field(default=640, ge=32, description="Inference frame resolution")
    batch_size: int = Field(default=16, ge=1, description="Batch size for parallel evaluation")
    device: str = Field(default="cpu", description="Compute device ('cpu', 'cuda:0')")
    half_precision: bool = Field(default=False, description="FP16 evaluation mode")
    save_json: bool = Field(
        default=True, description="Save predictions to JSON for COCO evaluation"
    )
    output_dir: str = Field(
        default="reports/eval", description="Directory to store evaluation artifacts"
    )

    model_config = ConfigDict(extra="ignore")
