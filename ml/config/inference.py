"""
Inference Configuration Schema.

Defines runtime options for edge forward-pass detection without hardcoding constants.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class InferenceConfig(BaseModel):
    """Configuration contract for model inference execution."""

    model_name: str = Field(default="yolo11", description="Registered model key")
    weights_path: str = Field(default="weights/yolo11n.pt", description="Path to checkpoint file")
    device: str = Field(
        default="cpu", description="Hardware execution device ('cpu', 'cuda:0', 'mps')"
    )
    imgsz: tuple[int, int] = Field(
        default=(640, 640), description="Input frame resolution (width, height)"
    )
    conf_threshold: float = Field(
        default=0.25, ge=0.0, le=1.0, description="Confidence filtering cutoff"
    )
    iou_threshold: float = Field(default=0.45, ge=0.0, le=1.0, description="NMS IoU threshold")
    half_precision: bool = Field(
        default=False, description="Use FP16 half precision when supported"
    )
    max_detections: int = Field(default=300, ge=1, description="Maximum detection count per frame")
    warmup_iterations: int = Field(
        default=5, ge=0, description="Number of pre-inference priming passes"
    )
    enable_tracking: bool = Field(
        default=True, description="Attach edge object tracker across frames"
    )

    model_config = ConfigDict(extra="ignore")
