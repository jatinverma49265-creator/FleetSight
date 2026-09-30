"""
Tests for Work Orders API and RBAC state transitions.
"""

from fastapi.testclient import TestClient

from backend.analytics.store import store
from backend.app import create_app
from backend.schemas import WorkOrderStatus


def test_work_orders_listing_and_rbac_flow():
    app = create_app()
    with TestClient(app) as client:
        # 1. Fetch work orders
        res = client.get("/api/v1/work-orders/")
        assert res.status_code == 200
        wos = res.json()
        assert len(wos) >= 1
        target_wo = wos[0]
        wo_id = target_wo["work_order_id"]

        # 2. Viewer attempt to update work order -> 403 Forbidden
        viewer_headers = {"x-user-role": "viewer"}
        res_viewer = client.patch(
            f"/api/v1/work-orders/{wo_id}",
            json={"status": "assigned", "assigned_to": "PWD Road Crew A"},
            headers=viewer_headers,
        )
        assert res_viewer.status_code == 403
        assert "Access denied" in res_viewer.json()["detail"]

        # 3. Police attempt to update work order -> 403 Forbidden
        police_headers = {"x-user-role": "police"}
        res_police = client.patch(
            f"/api/v1/work-orders/{wo_id}",
            json={"status": "assigned", "assigned_to": "PWD Road Crew A"},
            headers=police_headers,
        )
        assert res_police.status_code == 403

        # 4. Engineer approves/assigns work order -> 200 OK
        eng_headers = {"x-user-role": "engineer"}
        res_eng = client.patch(
            f"/api/v1/work-orders/{wo_id}",
            json={"status": "assigned", "assigned_to": "PWD Road Crew A", "comment": "Approved for emergency pothole patching"},
            headers=eng_headers,
        )
        assert res_eng.status_code == 200
        updated = res_eng.json()
        assert updated["status"] == "assigned"
        assert updated["assigned_to"] == "PWD Road Crew A"
        assert len(updated["history"]) >= 1
