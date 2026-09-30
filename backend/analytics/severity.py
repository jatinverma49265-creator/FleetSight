"""
FleetSight severity & explainable priority scoring engine.

Calculates a deterministic 0-100 priority score with a full factor breakdown:
- Base defect severity weight (0-40)
- Multi-bus recurrence & observation weight (0-30)
- Road hierarchy context weight (0-20)
- Detector confidence weight (0-10)
"""

from __future__ import annotations

from backend.schemas import DetectionClass, DetectionType, SeverityBreakdown, SeverityLevel


def compute_severity_level(
    detection_class: DetectionClass,
    detection_type: DetectionType,
    bbox_area_ratio: float | None = None,
) -> SeverityLevel:
    """Derive base severity level from detection class and bounding box size."""
    if detection_class in {DetectionClass.POTHOLE, DetectionClass.ALLIGATOR_CRACK}:
        if bbox_area_ratio and bbox_area_ratio > 0.08:
            return SeverityLevel.CRITICAL
        return SeverityLevel.HIGH
    if detection_class in {
        DetectionClass.WATERLOGGING,
        DetectionClass.DAMAGED_BARRIER,
        DetectionClass.MISSING_SIGN,
    }:
        return SeverityLevel.HIGH
    if detection_class in {
        DetectionClass.TRANSVERSE_CRACK,
        DetectionClass.LONGITUDINAL_CRACK,
        DetectionClass.DAMAGED_SIGN,
    }:
        return SeverityLevel.MEDIUM
    return SeverityLevel.LOW


def calculate_severity_breakdown(
    severity_level: SeverityLevel,
    observation_count: int,
    confidence: float,
    road_classification: str = "Arterial",
) -> SeverityBreakdown:
    """
    Compute explainable priority score breakdown (0-100).

    Formula:
    Priority = Severity_Weight (max 40)
             + Recurrence_Weight (max 30)
             + Context_Weight (max 20)
             + Confidence_Weight (max 10)
    """
    # 1. Base Severity Weight (0-40)
    severity_weights = {
        SeverityLevel.CRITICAL: 40,
        SeverityLevel.HIGH: 32,
        SeverityLevel.MEDIUM: 20,
        SeverityLevel.LOW: 10,
    }
    s_weight = severity_weights.get(severity_level, 10)

    # 2. Recurrence / Multi-Pass Weight (0-30)
    # 1 pass = 10, 2 passes = 20, 3+ passes = 30
    r_weight = min(30, max(10, observation_count * 10))

    # 3. Road Hierarchy Context Weight (0-20)
    road_weights = {
        "Arterial": 20,
        "Collector": 12,
        "Local": 5,
    }
    c_weight = road_weights.get(road_classification, 15)

    # 4. Detector Confidence Weight (0-10)
    conf_weight = int(round(min(1.0, max(0.0, confidence)) * 10))

    total_score = min(100, max(0, s_weight + r_weight + c_weight + conf_weight))

    explanation = (
        f"Score {total_score}/100 based on {severity_level.value.upper()} severity (+{s_weight}), "
        f"{observation_count} corroborating observation(s) (+{r_weight}), "
        f"{road_classification} corridor context (+{c_weight}), and "
        f"{int(confidence * 100)}% detection confidence (+{conf_weight})."
    )

    return SeverityBreakdown(
        score=total_score,
        severity_level=severity_level,
        severity_weight=s_weight,
        recurrence_weight=r_weight,
        context_weight=c_weight,
        confidence_weight=conf_weight,
        road_classification=road_classification,
        explanation=explanation,
    )
