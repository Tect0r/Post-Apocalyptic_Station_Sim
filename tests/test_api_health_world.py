from fastapi.testclient import TestClient

from metro_sim.interfaces.api.app import app

client = TestClient(app)


def test_health_endpoint_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_world_endpoint_returns_world_state():
    response = client.get("/world")

    assert response.status_code == 200

    data = response.json()

    assert "tick" in data
    assert "stations" in data
    assert "routes" in data
    assert "factions" in data
    assert "events" in data