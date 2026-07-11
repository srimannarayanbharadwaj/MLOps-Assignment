"""Tests for API monitoring endpoints."""

from fastapi.testclient import TestClient

from src.api import app


client = TestClient(app)


def test_health_endpoint_returns_ok_status() -> None:
    """The health endpoint should report a healthy service."""
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["model_loaded"] is True


def test_metrics_endpoint_returns_prometheus_text() -> None:
    """The metrics endpoint should expose Prometheus-formatted metrics."""
    client.get("/health")
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "http_requests_total" in response.text
