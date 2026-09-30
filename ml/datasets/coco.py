"""
COCO Pretrained Dataset Mapping.

Maps standard 80-class COCO object categories (vehicles, vulnerable road users,
and traffic infrastructure) to FleetSight canonical DetectionClass instances.
"""

from __future__ import annotations

from typing import Final

from backend.schemas import DetectionClass

# COCO category integer ID -> FleetSight DetectionClass for relevant road scene classes
COCO_ID_TO_CANONICAL: Final[dict[int, DetectionClass]] = {
    0: DetectionClass.PEDESTRIAN,  # person
    1: DetectionClass.TWO_WHEELER,  # bicycle
    2: DetectionClass.CAR,  # car
    3: DetectionClass.TWO_WHEELER,  # motorcycle
    5: DetectionClass.BUS,  # bus
    7: DetectionClass.TRUCK,  # truck
    9: DetectionClass.SIGNBOARD,  # traffic light (mapped to infrastructure)
    11: DetectionClass.SIGNBOARD,  # stop sign
}

# COCO category name -> FleetSight DetectionClass
COCO_NAME_TO_CANONICAL: Final[dict[str, DetectionClass]] = {
    "person": DetectionClass.PEDESTRIAN,
    "pedestrian": DetectionClass.PEDESTRIAN,
    "bicycle": DetectionClass.TWO_WHEELER,
    "car": DetectionClass.CAR,
    "motorcycle": DetectionClass.TWO_WHEELER,
    "bus": DetectionClass.BUS,
    "truck": DetectionClass.TRUCK,
    "traffic light": DetectionClass.SIGNBOARD,
    "stop sign": DetectionClass.SIGNBOARD,
}


def map_coco_id_to_class(coco_id: int) -> DetectionClass | None:
    """
    Map a COCO 80-class integer index to FleetSight canonical DetectionClass.

    Returns None if the class is not relevant to urban intelligence monitoring
    (e.g., animals, indoor objects).
    """
    return COCO_ID_TO_CANONICAL.get(coco_id)


def map_coco_name_to_class(name: str) -> DetectionClass | None:
    """
    Map a COCO class name to FleetSight canonical DetectionClass.

    Returns None if class is not monitored by FleetSight.
    """
    return COCO_NAME_TO_CANONICAL.get(name.lower().strip())
