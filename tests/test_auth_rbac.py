"""
Tests for Auth & RBAC roles.
"""

from fastapi.testclient import TestClient

from backend.app import create_app


def test_auth_login_and_roles():
    app = create_app()
    with TestClient(app) as client:
        # Admin login
        res = client.post("/api/v1/auth/login", json={"username": "admin", "password": "any"})
        assert res.status_code == 200
        data = res.json()
        assert data["user"]["role"] == "admin"

        # Engineer login
        res = client.post("/api/v1/auth/login", json={"username": "engineer", "password": "any"})
        assert res.status_code == 200
        data = res.json()
        assert data["user"]["role"] == "engineer"

        # Check me endpoint with Bearer token
        res_me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {data['access_token']}"})
        assert res_me.status_code == 200
        assert res_me.json()["role"] == "engineer"


def test_audit_log_rbac_restriction():
    app = create_app()
    with TestClient(app) as client:
        # Viewer denied access to audit logs
        res_v = client.get("/api/v1/audit/", headers={"x-user-role": "viewer"})
        assert res_v.status_code == 403

        # Engineer denied access to audit logs
        res_e = client.get("/api/v1/audit/", headers={"x-user-role": "engineer"})
        assert res_e.status_code == 403

        # Admin allowed
        res_a = client.get("/api/v1/audit/", headers={"x-user-role": "admin"})
        assert res_a.status_code == 200
        assert isinstance(res_a.json(), list)

        # Police allowed
        res_p = client.get("/api/v1/audit/", headers={"x-user-role": "police"})
        assert res_p.status_code == 200
