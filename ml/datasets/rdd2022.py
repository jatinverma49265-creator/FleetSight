"""
RDD2022 (Road Damage Detection Challenge) Dataset Definition & Taxonomy Mapping.

Maps CRDDC 2022 international road damage classes (D00, D10, D20, D40)
to FleetSight canonical DetectionClass instances.
"""

from __future__ import annotations

from typing import Final

from backend.schemas import DetectionClass

# Official CRDDC 2022 class code definitions
RDD2022_CODE_TO_CANONICAL: Final[dict[str, DetectionClass]] = {
    "D00": DetectionClass.LONGITUDINAL_CRACK,
    "D10": DetectionClass.TRANSVERSE_CRACK,
    "D20": DetectionClass.ALLIGATOR_CRACK,
    "D40": DetectionClass.POTHOLE,
}

CANONICAL_TO_RDD2022_CODE: Final[dict[DetectionClass, str]] = {
    v: k for k, v in RDD2022_CODE_TO_CANONICAL.items()
}

# RDD2022 integer class index mapping for standard YOLO format
RDD2022_YOLO_CLASS_NAMES: Final[list[str]] = ["D00", "D10", "D20", "D40"]
RDD2022_YOLO_ID_TO_CODE: Final[dict[int, str]] = {
    idx: name for idx, name in enumerate(RDD2022_YOLO_CLASS_NAMES)
}
RDD2022_YOLO_CODE_TO_ID: Final[dict[str, int]] = {
    name: idx for idx, name in enumerate(RDD2022_YOLO_CLASS_NAMES)
}


def map_rdd2022_code_to_class(code: str) -> DetectionClass:
    """
    Map an RDD2022 code string (e.g. 'D40') to FleetSight canonical DetectionClass.

    Raises:
        KeyError: If code is not a known RDD2022 class.
    """
    clean_code = code.strip().upper()
    if clean_code not in RDD2022_CODE_TO_CANONICAL:
        valid_codes = list(RDD2022_CODE_TO_CANONICAL.keys())
        raise KeyError(f"Unknown RDD2022 class code '{code}'. Expected one of {valid_codes}")
    return RDD2022_CODE_TO_CANONICAL[clean_code]




def map_rdd2022_id_to_class(class_id: int) -> DetectionClass:
    """
    Map a zero-indexed YOLO class ID from an RDD2022 model to FleetSight DetectionClass.

    Raises:
        ValueError: If class_id is out of range.
    """
    if class_id not in RDD2022_YOLO_ID_TO_CODE:
        max_id = len(RDD2022_YOLO_CLASS_NAMES) - 1
        raise ValueError(f"Invalid RDD2022 YOLO class ID {class_id}. Expected 0..{max_id}")

    return RDD2022_CODE_TO_CANONICAL[RDD2022_YOLO_ID_TO_CODE[class_id]]
