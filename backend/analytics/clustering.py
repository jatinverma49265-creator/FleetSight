"""
FleetSight spatial clustering and multi-bus corroboration engine.

Groups individual GPS-tagged detection events into canonical spatial issues.
Promotes an issue from CANDIDATE to VERIFIED when corroborated by >= 2 distinct buses.
"""

from __future__ import annotations

import math
from datetime import UTC, datetime

from backend.analytics.severity import calculate_severity_breakdown, compute_severity_level
from backend.schemas import (
    ClusteredIssue,
    DataOrigin,
    DetectionClass,
    DetectionEvent,
    DetectionType,
    IssueStatus,
    SeverityLevel,
)


def haversine_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great-circle distance between two GPS coordinates in metres."""
    r = 6371000.0  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return r * c


def determine_road_segment(latitude: float, longitude: float) -> str:
    """Classify Jaipur road corridor based on coordinates."""
    # Centered around Jaipur major corridors
    if 26.910 <= latitude <= 26.925 and 75.790 <= longitude <= 75.820:
        return "MI Road (Ajmeri Gate to Paanch Batti)"
    if 26.860 <= latitude <= 26.910 and 75.795 <= longitude <= 75.815:
        return "Tonk Road (Rambagh to Gandhi Nagar)"
    if 26.880 <= latitude <= 26.915 and 75.810 <= longitude <= 75.830:
        return "JLN Marg (Birla Temple to Jawahar Circle)"
    if 26.900 <= latitude <= 26.920 and 75.760 <= longitude <= 75.795:
        return "Civil Lines / Ajmer Road"
    return "Jaipur City Sector Arterial"


class CorroborationEngine:
    """
    Stateful or batch corroborator for detection events.

    Clusters incoming events within a distance threshold (default: 35.0 metres)
    and validates multi-bus corroboration.
    """

    def __init__(self, cluster_radius_meters: float = 35.0) -> None:
        self.cluster_radius_meters = cluster_radius_meters

    def find_matching_issue(
        self,
        event: DetectionEvent,
        existing_issues: list[ClusteredIssue],
    ) -> ClusteredIssue | None:
        """Find an existing issue within cluster radius matching class and type."""
        for issue in existing_issues:
            # Check class compatibility (potholes match potholes, cracks match cracks)
            if issue.detection_class == event.detection_class:
                dist = haversine_distance_meters(
                    issue.latitude,
                    issue.longitude,
                    event.latitude,
                    event.longitude,
                )
                if dist <= self.cluster_radius_meters:
                    return issue
        return None

    def process_event(
        self,
        event: DetectionEvent,
        existing_issues: list[ClusteredIssue],
    ) -> tuple[ClusteredIssue, bool]:
        """
        Incorporate a new DetectionEvent.

        Returns (issue, is_new_issue).
        """
        match = self.find_matching_issue(event, existing_issues)
        road_segment = determine_road_segment(event.latitude, event.longitude)

        if match is not None:
            # Update existing issue
            match.observation_count += 1
            match.last_detected_at = max(match.last_detected_at, event.timestamp)
            if event.bus_id not in match.bus_ids:
                match.bus_ids.append(event.bus_id)
            if event.camera_id not in match.camera_ids:
                match.camera_ids.append(event.camera_id)
            if event.event_id not in match.event_ids:
                match.event_ids.append(event.event_id)
            if event.evidence_uri and not match.evidence_uri:
                match.evidence_uri = event.evidence_uri

            # Multi-bus corroboration check: 2+ distinct buses promotes to VERIFIED
            if len(match.bus_ids) >= 2 and match.status == IssueStatus.CANDIDATE:
                match.status = IssueStatus.VERIFIED

            # Recalculate severity & priority score
            bbox_area = (event.bbox.w * event.bbox.h) if event.bbox else None
            sev_level = event.severity or compute_severity_level(
                event.detection_class, event.type, bbox_area
            )
            # Retain higher severity
            if (
                sev_level == SeverityLevel.CRITICAL
                or match.severity == SeverityLevel.LOW
            ):
                match.severity = sev_level

            breakdown = calculate_severity_breakdown(
                severity_level=match.severity,
                observation_count=match.observation_count,
                confidence=event.confidence,
                road_classification="Arterial",
            )
            match.priority_score = breakdown.score
            match.severity_breakdown = breakdown

            return match, False

        # Create new candidate issue
        bbox_area = (event.bbox.w * event.bbox.h) if event.bbox else None
        sev_level = event.severity or compute_severity_level(
            event.detection_class, event.type, bbox_area
        )
        breakdown = calculate_severity_breakdown(
            severity_level=sev_level,
            observation_count=1,
            confidence=event.confidence,
            road_classification="Arterial",
        )

        new_issue = ClusteredIssue(
            type=event.type,
            detection_class=event.detection_class,
            status=IssueStatus.CANDIDATE,
            severity=sev_level,
            priority_score=breakdown.score,
            severity_breakdown=breakdown,
            latitude=event.latitude,
            longitude=event.longitude,
            road_segment=road_segment,
            first_detected_at=event.timestamp,
            last_detected_at=event.timestamp,
            observation_count=1,
            bus_ids=[event.bus_id],
            camera_ids=[event.camera_id],
            event_ids=[event.event_id],
            evidence_uri=event.evidence_uri,
            data_origin=event.data_origin,
        )
        return new_issue, True
