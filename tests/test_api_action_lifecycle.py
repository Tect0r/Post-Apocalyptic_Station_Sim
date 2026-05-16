from fastapi.testclient import TestClient

from metro_sim.interfaces.api.app import app
from tests.api_test_helpers import authenticated_test_user

client = TestClient(app)


def test_cancel_action_via_api():
    with authenticated_test_user(client) as auth:
        start_response = client.post(
            "/player/me/actions",
            headers=auth["headers"],
            json={
                "action_type": "support_militia",
                "target_id": "paveletskaya_radial",
            },
        )

        assert start_response.status_code == 200

        action_id = start_response.json()["data"]["action_id"]

        cancel_response = client.post(
            f"/player/me/actions/{action_id}/cancel",
            headers=auth["headers"],
        )

        assert cancel_response.status_code == 200
        assert cancel_response.json()["success"] is True
        assert cancel_response.json()["message"] == "player_action_cancelled"

        player_response = client.get(
            "/player/me",
            headers=auth["headers"],
        )

        player = player_response.json()

        assert len(player["active_actions"]) == 0
        assert len(player["completed_actions"]) == 1
        assert player["completed_actions"][0]["status"] == "cancelled"