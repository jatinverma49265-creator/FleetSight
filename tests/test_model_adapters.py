"""Tests for concrete model adapters (YOLO11, YOLO12, YOLO26) and Detector protocol conformance."""

from __future__ import annotations

import numpy as np
import pytest

from ml.datasets.exceptions import ModelWeightsMissingError
from ml.detector import Detector, FrameResult
from ml.models import BaseYOLOAdapter, YOLO11Detector, YOLO12Detector, YOLO26Detector
from ml.registry import available_detectors, create_detector


class TestModelAdapters:
    def test_registered_model_names(self) -> None:
        avail = available_detectors()
        assert "yolo11" in avail
        assert "yolo12" in avail
        assert "yolo26" in avail

    @pytest.mark.parametrize(
        ("model_key", "expected_cls"),
        [
            ("yolo11", YOLO11Detector),
            ("yolo12", YOLO12Detector),
            ("yolo26", YOLO26Detector),
        ],
    )
    def test_detector_protocol_conformance(self, model_key: str, expected_cls: type) -> None:
        detector = create_detector(model_key)
        assert isinstance(detector, expected_cls)
        assert isinstance(detector, Detector)
        assert detector.model_name == model_key
        assert detector.model_version

    def test_missing_weights_raises_descriptive_error(self) -> None:
        with pytest.raises(ModelWeightsMissingError, match="Weights not found"):
            create_detector("yolo11", weights="weights/missing_yolo11.pt")

    def test_predict_without_load_raises_runtime_error(self) -> None:
        detector = create_detector("yolo11")
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        with pytest.raises(RuntimeError, match="has not been loaded"):
            detector.predict(frame)

    @pytest.mark.parametrize("model_key", ["yolo11", "yolo12", "yolo26"])
    def test_mock_mode_inference_and_warmup(self, model_key: str) -> None:
        detector = create_detector(model_key)
        assert isinstance(detector, BaseYOLOAdapter)
        detector.enable_mock_mode()


        # Warmup should not raise
        detector.warmup(imgsz=(320, 320))

        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        res = detector.predict(frame, confidence_threshold=0.25)
        assert isinstance(res, FrameResult)
        assert res.inference_time_ms >= 0.0
