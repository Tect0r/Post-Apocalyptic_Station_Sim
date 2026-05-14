from fastapi.testclient import TestClient

from metro_sim.interfaces.api.app import app
from tests.api_test_helpers import authenticated_test_user

client = TestClient(app)


def test_get_player_me_returns_authenticated_player():
    with authenticated_test_user(client) as auth:
        response = client.get(
            "/player/me",
            headers=auth["headers"],
        )

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == auth["username"]
        assert "crew" in data
        assert "inventory" in data
        assert "reputation" in data
        assert "active_actions" in data


def test_get_player_crew_returns_authenticated_crew():
    with authenticated_test_user(client) as auth:
        response = client.get(
            "/player/me/crew",
            headers=auth["headers"],
        )

        assert response.status_code == 200

        data = response.json()

        assert "members" in data
        assert "health" in data
        assert "morale" in data
        assert "fatigue" in data


def test_get_player_actions_returns_authenticated_active_actions():
    with authenticated_test_user(client) as auth:
        response = client.get(
            "/player/me/actions",
            headers=auth["headers"],
        )

        assert response.status_code == 200
        assert "active_actions" in response.json()

def test_player_me_requires_authentication():
    response = client.get("/player/me")

    assert response.status_code in (401, 403)
    