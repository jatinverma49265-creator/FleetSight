"""Shared test fixtures."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from backend.app import create_app


@pytest.fixture()
def client() -> TestClient:
    """Synchronous test client for the FastAPI app."""
    app = create_app()
    return TestClient(app)
