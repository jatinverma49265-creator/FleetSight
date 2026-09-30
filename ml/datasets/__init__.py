"""
FleetSight ML Datasets Package.

Exports dataset manifests, RDD2022/COCO/Jaipur definitions,
route/day splitters, and annotation validation utilities.
"""

from __future__ import annotations

from ml.datasets.coco import map_coco_id_to_class, map_coco_name_to_class
from ml.datasets.exceptions import (
    AnnotationValidationError,
    DatasetError,
    DatasetNotFoundError,
    DatasetNotReadyError,
    LicenseVerificationError,
    ModelWeightsMissingError,
)
from ml.datasets.jaipur import (
    JAIPUR_CLASSES,
    JaipurDatasetLayout,
    JaipurFrameMetadata,
)
from ml.datasets.manifest import (
    DatasetManifest,
    DatasetManifestEntry,
    DatasetStatus,
    DatasetType,
    load_default_manifest,
)
from ml.datasets.rdd2022 import (
    RDD2022_CODE_TO_CANONICAL,
    map_rdd2022_code_to_class,
    map_rdd2022_id_to_class,
)
from ml.datasets.split import RouteDaySplitter, SplitRatio, SplitResult
from ml.datasets.validator import (
    ValidationIssue,
    ValidationSummary,
    YOLOAnnotation,
    validate_annotation_file,
    validate_dataset_directory,
)

__all__ = [
    "AnnotationValidationError",
    "DatasetError",
    "DatasetManifest",
    "DatasetManifestEntry",
    "DatasetNotFoundError",
    "DatasetNotReadyError",
    "DatasetStatus",
    "DatasetType",
    "JAIPUR_CLASSES",
    "JaipurDatasetLayout",
    "JaipurFrameMetadata",
    "LicenseVerificationError",
    "ModelWeightsMissingError",
    "RDD2022_CODE_TO_CANONICAL",
    "RouteDaySplitter",
    "SplitRatio",
    "SplitResult",
    "ValidationIssue",
    "ValidationSummary",
    "YOLOAnnotation",
    "load_default_manifest",
    "map_coco_id_to_class",
    "map_coco_name_to_class",
    "map_rdd2022_code_to_class",
    "map_rdd2022_id_to_class",
    "validate_annotation_file",
    "validate_dataset_directory",
]
