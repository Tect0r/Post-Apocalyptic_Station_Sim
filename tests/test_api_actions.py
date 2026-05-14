from fastapi.testclient import TestClient

from metro_sim.interfaces.api.app import app
from tests.api_test_helpers import authenticated_test_user

client = TestClient(app)


def test_start_player_action_via_api():
    with authenticated_test_user(client) as auth:
        response = client.post(
            "/player/me/actions",
            headers=auth["headers"],
            json={
                "action_type": "support_militia",
                "target_id": "paveletskaya",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["success"] is True
        assert data["message"] == "player_action_started"
        assert data["data"]["action_type"] == "support_militia"


def test_start_player_action_rejects_unknown_action_type():
    with authenticated_test_user(client) as auth:
        response = client.post(
            "/player/me/actions",
            headers=auth["headers"],
            json={
                "action_type": "unknown_action",
                "target_id": "paveletskaya",
            },
        )



    assert response.status_code == 400
    assert response.json()["detail"] == "unknown_action_type"


def test_start_player_action_rejects_missing_station():
    with authenticated_test_user(client) as auth:
        response = client.post(
            "/player/me/actions",
            headers=auth["headers"],
            json={
                "action_type": "support_militia",
                "target_id": "missing_station",
            },
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "target_station_not_found"

def test_start_player_action_requires_authentication():
    response = client.post(
        "/player/me/actions",
        json={
            "action_type": "support_militia",
            "target_id": "paveletskaya",
        },
    )

    assert response.status_code in (401, 403)
    