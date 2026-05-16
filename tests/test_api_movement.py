from fastapi.testclient import TestClient

from metro_sim.interfaces.api.app import app
from tests.api_test_helpers import authenticated_test_user

client = TestClient(app)


def test_start_crew_movement_via_api():
    with authenticated_test_user(client) as auth:
        response = client.post(
            "/player/me/movement/start",
            headers=auth["headers"],
            json={
                "route_id": "route_paveletskaya_ring_radial",
            },
        )

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["message"] == "crew_movement_started"

        player_response = client.get(
            "/player/me",
            headers=auth["headers"],
        )

        player = player_response.json()

        assert player["crew"]["is_traveling"] is True
        assert player["crew"]["destination_location_id"] == "paveletskaya_ring"