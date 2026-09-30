"""Tests for the /health endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient) -> None:
    """GET /health should return 200 with status='ok'."""
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "version" in body
    assert "environment" in body


def test_health_contains_version(client: TestClient) -> None:
    """Health response must include a semver-style version string."""
    body = client.get("/health").json()
    parts = body["version"].split(".")
    assert len(parts) == 3, f"Expected semver, got {body['version']}"
