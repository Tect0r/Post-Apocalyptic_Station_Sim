from fastapi.testclient import TestClient

from metro_sim.interfaces.api.app import app

client = TestClient(app)


def test_get_player_me_returns_test_player():
    response = client.get("/player/me")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "player_001"
    assert "crew" in data
    assert "inventory" in data
    assert "reputation" in data
    assert "active_actions" in data


def test_get_player_crew_returns_crew():
    response = client.get("/player/me/crew")

    assert response.status_code == 200

    data = response.json()

    assert "members" in data
    assert "health" in data
    assert "morale" in data
    assert "fatigue" in data


def test_get_player_actions_returns_active_actions():
    response = client.get("/player/me/actions")

    assert response.status_code == 200
    assert "active_actions" in response.json()