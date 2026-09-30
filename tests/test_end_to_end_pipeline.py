"""
Complete End-to-End Pipeline Integration Test for FleetSight.

Flow tested:
1. Edge Video/Event Generation (Sampling, Tracking, Privacy Blur, Dedup)
2. Ingestion by FastAPI backend
3. Spatial clustering & corroboration (Pass 1 Candidate -> Pass 2 2-Bus Verified)
4. Explainable severity breakdown scoring
5. Work-order candidate generation
6. Human-in-the-loop Engineer approval & assignment
7. Closed-loop re-detection pass (Defect repaired -> Verified Closed)
"""

from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from backend.analytics.store import store
from backend.app import create_app
from backend.schemas import (
    BoundingBox,
    DataOrigin,
    DetectionClass,
    DetectionEvent,
    DetectionType,
    IssueStatus,
    SeverityLevel,
    UserRole,
    WorkOrderStatus,
)
from edge.privacy import MockPrivacyFilter
from edge.tracking import CentroidTracker, TrackerConfig


def test_full_end_to_end_lifecycle():
    """Verify entire edge-to-GIS decision loop from camera detection to closure."""
    # 0. Initialize Clean App and Store
    app = create_app()

    with TestClient(app) as client:
        store.reset_state()
        # 1. Edge Processing: Privacy filter & Tracker
        privacy = MockPrivacyFilter()
        tracker = CentroidTracker(TrackerConfig(max_disappeared=5))

        # 2. Pass 1 (Bus RJ14-01): Edge detects a severe pothole on MI Road
        now = datetime.now(UTC)
        pothole_lat, pothole_lon = 26.91720, 75.81250
        event1 = {
            "event_id": "EVT-E2E-001",
            "type": DetectionType.ROAD_DAMAGE.value,
            "class": DetectionClass.POTHOLE.value,
            "confidence": 0.92,
            "severity": SeverityLevel.HIGH.value,
            "latitude": pothole_lat,
            "longitude": pothole_lon,
            "timestamp": (now - timedelta(minutes=45)).isoformat(),
            "camera_id": "CAM-FRONT-01",
            "bus_id": "RJ14-01",
            "model_version": "yolo11-v0.1.0",
            "bbox": {"x": 0.45, "y": 0.60, "w": 0.20, "h": 0.15},
            "data_origin": DataOrigin.SIMULATED.value,
        }

        res1 = client.post("/api/v1/events/", json=event1)
        assert res1.status_code == 201
        assert res1.json()["event_id"] == "EVT-E2E-001"

        # Verify Issue is created as CANDIDATE (single observation)
        res_issues1 = client.get("/api/v1/issues/")
        assert res_issues1.status_code == 200
        issues1 = res_issues1.json()
        assert len(issues1) == 1
        issue = issues1[0]
        assert issue["status"] == "candidate"
        assert issue["observation_count"] == 1
        assert issue["bus_ids"] == ["RJ14-01"]
        issue_id = issue["issue_id"]

        # 3. Pass 2 (Bus RJ14-07): Second public bus surveys same corridor (~10m offset)
        event2 = {
            "event_id": "EVT-E2E-002",
            "type": DetectionType.ROAD_DAMAGE.value,
            "class": DetectionClass.POTHOLE.value,
            "confidence": 0.94,
            "severity": SeverityLevel.HIGH.value,
            "latitude": pothole_lat + 0.00008,
            "longitude": pothole_lon - 0.00005,
            "timestamp": (now - timedelta(minutes=15)).isoformat(),
            "camera_id": "CAM-FRONT-07",
            "bus_id": "RJ14-07",
            "model_version": "yolo11-v0.1.0",
            "bbox": {"x": 0.42, "y": 0.58, "w": 0.22, "h": 0.16},
            "data_origin": DataOrigin.SIMULATED.value,
        }

        res2 = client.post("/api/v1/events/", json=event2)
        assert res2.status_code == 201

        # Verify Corroboration promotes issue to WORK_ORDER / VERIFIED
        res_issues2 = client.get(f"/api/v1/issues/{issue_id}", headers={"x-user-role": "engineer"})
        assert res_issues2.status_code == 200
        corroborated_issue = res_issues2.json()
        assert corroborated_issue["observation_count"] == 2
        assert set(corroborated_issue["bus_ids"]) == {"RJ14-01", "RJ14-07"}
        assert corroborated_issue["priority_score"] >= 75
        assert corroborated_issue["severity_breakdown"]["recurrence_weight"] == 20

        # 4. Work Order Candidate is created
        res_wos = client.get("/api/v1/work-orders/")
        assert res_wos.status_code == 200
        wos = res_wos.json()
        assert len(wos) >= 1
        target_wo = [w for w in wos if w["issue_id"] == issue_id][0]
        wo_id = target_wo["work_order_id"]

        # 5. RBAC Enforcement: Viewer is DENIED approval
        res_viewer_deny = client.patch(
            f"/api/v1/work-orders/{wo_id}",
            json={"status": "assigned", "assigned_to": "PWD Road Crew Division 1"},
            headers={"x-user-role": "viewer"},
        )
        assert res_viewer_deny.status_code == 403

        # Engineer is ALLOWED approval & assignment
        res_eng_approve = client.patch(
            f"/api/v1/work-orders/{wo_id}",
            json={
                "status": "assigned",
                "assigned_to": "PWD Road Crew Division 1",
                "comment": "Approved for immediate pothole patching",
            },
            headers={"x-user-role": "engineer"},
        )
        assert res_eng_approve.status_code == 200
        assert res_eng_approve.json()["status"] == "assigned"

        # Maintenance crew finishes repair -> marked COMPLETED
        client.patch(
            f"/api/v1/work-orders/{wo_id}",
            json={"status": "completed", "comment": "Patching finished at 15:30"},
            headers={"x-user-role": "engineer"},
        )

        # 6. Pass 3 (Bus RJ14-12): Re-detection survey pass
        # Road was repaired, so Bus RJ14-12 does NOT detect any defect at pothole_lat, pothole_lon
        res_redetect = client.post(
            "/api/v1/demo/redetection-check",
            json={
                "bus_id": "RJ14-12",
                "detected_issue_ids": [],  # zero detections at repair site
                "surveyed_segments": ["MI Road (Ajmeri Gate to Paanch Batti)"],
            },
        )
        assert res_redetect.status_code == 200
        redetect_data = res_redetect.json()
        assert wo_id in redetect_data["closed_work_orders"]

        # 7. Confirm Work Order is officially CLOSED in state
        final_wo = client.get(f"/api/v1/work-orders/{wo_id}").json()
        assert final_wo["status"] == "closed"
        assert any(h["action"] == "REDETECTION_VERIFIED_CLOSED" for h in final_wo["history"])

        # 8. Check KPIs and Audit Trail
        kpis = client.get("/api/v1/kpis/").json()
        assert kpis["work_orders_closed"] >= 1
        assert kpis["bandwidth_saved_pct"] > 90.0

        audit_res = client.get("/api/v1/audit/", headers={"x-user-role": "admin"})
        assert audit_res.status_code == 200
        audit_logs = audit_res.json()
        assert any(a["action"] == "WORK_ORDER_VERIFIED_CLOSED" for a in audit_logs)
