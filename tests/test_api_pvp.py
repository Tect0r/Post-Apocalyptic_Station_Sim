from fastapi.testclient import TestClient

from metro_sim.interfaces.api.app import app
from tests.api_test_helpers import authenticated_test_user

client = TestClient(app)


def test_pvp_station_pressure_via_api():
    with authenticated_test_user(client) as auth:
        response = client.post(
            "/pvp/station-pressure",
            headers=auth["headers"],
            json={
                "station_id": "paveletskaya",
                "pressure_key": "sabotage",
                "amount": 5,
            },
        )

        assert response.status_code == 200
        assert response.json()["success"] is True


def test_get_pvp_impacts_via_api():
    with authenticated_test_user(client) as auth:
        client.post(
            "/pvp/station-pressure",
            headers=auth["headers"],
            json={
                "station_id": "paveletskaya",
                "pressure_key": "sabotage",
                "amount": 5,
            },
        )

        response = client.get(
            "/pvp/impacts",
            headers=auth["headers"],
        )

        assert response.status_code == 200
        assert "impacts" in response.json()
        assert len(response.json()["impacts"]) >= 1