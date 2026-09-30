"""Tests for RDD2022, COCO, and Jaipur class taxonomy mappings."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from backend.schemas import DetectionClass
from ml.datasets.coco import map_coco_id_to_class, map_coco_name_to_class
from ml.datasets.jaipur import (
    JAIPUR_CLASSES,
    JAIPUR_SUBDIRECTORIES,
    JaipurDatasetLayout,
    JaipurFrameMetadata,
)
from ml.datasets.rdd2022 import (
    map_rdd2022_code_to_class,
    map_rdd2022_id_to_class,
)


class TestClassMappings:
    def test_rdd2022_code_mapping(self) -> None:
        assert map_rdd2022_code_to_class("D00") == DetectionClass.LONGITUDINAL_CRACK
        assert map_rdd2022_code_to_class("D10") == DetectionClass.TRANSVERSE_CRACK
        assert map_rdd2022_code_to_class("D20") == DetectionClass.ALLIGATOR_CRACK
        assert map_rdd2022_code_to_class("D40") == DetectionClass.POTHOLE

        with pytest.raises(KeyError, match="Unknown RDD2022 class code"):
            map_rdd2022_code_to_class("D99")

    def test_rdd2022_id_mapping(self) -> None:
        assert map_rdd2022_id_to_class(0) == DetectionClass.LONGITUDINAL_CRACK
        assert map_rdd2022_id_to_class(1) == DetectionClass.TRANSVERSE_CRACK
        assert map_rdd2022_id_to_class(2) == DetectionClass.ALLIGATOR_CRACK
        assert map_rdd2022_id_to_class(3) == DetectionClass.POTHOLE

        with pytest.raises(ValueError, match="Invalid RDD2022 YOLO class ID"):
            map_rdd2022_id_to_class(4)

    def test_coco_id_and_name_mapping(self) -> None:
        # Check standard automotive and pedestrian categories
        assert map_coco_id_to_class(0) == DetectionClass.PEDESTRIAN
        assert map_coco_id_to_class(1) == DetectionClass.TWO_WHEELER
        assert map_coco_id_to_class(2) == DetectionClass.CAR
        assert map_coco_id_to_class(3) == DetectionClass.TWO_WHEELER
        assert map_coco_id_to_class(5) == DetectionClass.BUS
        assert map_coco_id_to_class(7) == DetectionClass.TRUCK

        # Name mapping
        assert map_coco_name_to_class("pedestrian") == DetectionClass.PEDESTRIAN
        assert map_coco_name_to_class("car") == DetectionClass.CAR
        assert map_coco_name_to_class("bus") == DetectionClass.BUS

        # Unmonitored indoor/animal classes return None
        assert map_coco_id_to_class(999) is None
        assert map_coco_name_to_class("cat") is None

    def test_jaipur_classes_and_structure(self, tmp_path: pytest.TempPathFactory) -> None:
        assert DetectionClass.POTHOLE in JAIPUR_CLASSES
        assert DetectionClass.WATERLOGGING in JAIPUR_CLASSES
        assert DetectionClass.DAMAGED_SIGN in JAIPUR_CLASSES
        assert len(JAIPUR_CLASSES) == 9

        # Test JaipurDatasetLayout
        layout = JaipurDatasetLayout(root_path=Path(str(tmp_path)))
        assert not layout.is_structure_valid()
        layout.initialize_structure()
        assert layout.is_structure_valid()
        for subdir in JAIPUR_SUBDIRECTORIES:
            assert (Path(str(tmp_path)) / subdir).is_dir()

    def test_jaipur_frame_metadata_schema(self) -> None:
        meta = JaipurFrameMetadata(
            frame_id="jpr_r9a_20260929_0001",
            route_id="Route-9A",
            bus_id="RJ14-PA-1234",
            timestamp=datetime.now(UTC),
            capture_day="2026-09-29",
            latitude=26.9124,
            longitude=75.7873,
            speed_kmh=35.0,
            weather="clear",
            lighting="daylight",
            privacy_face_blurred=True,
            privacy_plate_blurred=True,
            consent_verified=True,
        )
        assert meta.frame_id == "jpr_r9a_20260929_0001"
        assert meta.privacy_face_blurred is True
