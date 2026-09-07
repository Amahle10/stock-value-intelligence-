from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200


def test_pairs_endpoint():
    response = client.get("/api/market/pairs")
    assert response.status_code == 200
    assert "pairs" in response.json()


def test_summary_endpoint():
    response = client.get("/api/analytics/summary/EUR/USD")
    assert response.status_code == 200
