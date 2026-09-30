"""
Tests for KPIs and Traffic API endpoints.
"""

from fastapi.testclient import TestClient

from backend.app import create_app


def test_kpis_and_traffic_endpoints():
    app = create_app()
    with TestClient(app) as client:
        # KPIs endpoint
        res_kpi = client.get("/api/v1/kpis/")
        assert res_kpi.status_code == 200
        kpi = res_kpi.json()
        assert kpi["buses_active"] >= 1
        assert kpi["defects_detected"] >= 1
        assert kpi["bandwidth_saved_pct"] > 90.0
        assert kpi["data_origin"] == "simulated"

        # Traffic endpoint
        res_traffic = client.get("/api/v1/traffic/")
        assert res_traffic.status_code == 200
        traffic = res_traffic.json()
        assert "MI Road" in traffic["corridor_name"]
        assert len(traffic["segments"]) >= 1
        assert len(traffic["time_series"]) >= 1
