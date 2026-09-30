"""
Training Pipeline Configuration Schema.

Encapsulates all hyperparameters and environmental settings required for reproducible
fine-tuning of YOLO models on RDD2022 and Jaipur custom road damage datasets.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class TrainingConfig(BaseModel):
    """Specification for model training and fine-tuning."""

    model_family: str = Field(
        default="yolo11", description="Model architecture under training (yolo11, yolo12, yolo26)"
    )
    base_weights: str = Field(
        default="yolo11n.pt", description="Base checkpoint / pretrained weights"
    )
    dataset_yaml: str = Field(
        default="data/rdd2022/dataset.yaml", description="Path to YOLO dataset YAML"
    )
    epochs: int = Field(default=100, ge=1, description="Total training epochs")
    batch_size: int = Field(default=16, ge=1, description="Batch size per GPU / device")
    imgsz: int = Field(default=640, ge=32, description="Square input image resolution")
    device: str = Field(
        default="0", description="Compute device for training ('0', 'cpu', 'cuda:0')"
    )
    workers: int = Field(default=4, ge=0, description="Dataloader worker threads")
    lr0: float = Field(default=0.01, gt=0.0, description="Initial learning rate")
    lrf: float = Field(default=0.01, gt=0.0, description="Final learning rate factor")
    optimizer: str = Field(default="auto", description="Optimizer choice ('SGD', 'AdamW', 'auto')")
    freeze_layers: int = Field(default=0, ge=0, description="Number of backbone layers to freeze")
    patience: int = Field(default=20, ge=1, description="Early stopping patience in epochs")
    save_period: int = Field(default=10, ge=1, description="Checkpoint save frequency")
    project: str = Field(default="runs/train", description="Directory to store training runs")
    name: str = Field(default="baseline_run", description="Experiment run name")
    seed: int = Field(default=42, description="Random seed for reproducibility")

    model_config = ConfigDict(extra="ignore")
