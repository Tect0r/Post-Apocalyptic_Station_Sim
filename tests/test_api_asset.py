from fastapi.testclient import TestClient

from metro_sim.interfaces.api.app import app
from tests.api_test_helpers import authenticated_test_user

client = TestClient(app)


def test_get_player_assets_returns_assets_list():
    with authenticated_test_user(client) as auth:
        response = client.get(
            "/player/me/assets",
            headers=auth["headers"],
        )

        assert response.status_code == 200
        assert "assets" in response.json()


def test_add_asset_via_debug_api():
    with authenticated_test_user(client) as auth:
        response = client.post(
            "/player/me/assets",
            headers=auth["headers"],
            json={
                "asset_type": "storage_room",
                "station_id": "paveletskaya_ring",
            },
        )

        assert response.status_code == 200
        assert response.json()["success"] is True

        assets_response = client.get(
            "/player/me/assets",
            headers=auth["headers"],
        )

        assets = assets_response.json()["assets"]

        assert len(assets) == 1
        assert assets[0]["asset_type"] == "storage_room"


def test_upgrade_asset_via_api():
    with authenticated_test_user(client) as auth:
        add_response = client.post(
            "/player/me/assets",
            headers=auth["headers"],
            json={
                "asset_type": "storage_room",
                "station_id": "paveletskaya_ring",
            },
        )

        asset_id = add_response.json()["data"]["asset_id"]

        upgrade_response = client.post(
            f"/player/me/assets/{asset_id}/upgrade",
            headers=auth["headers"],
        )

        assert upgrade_response.status_code == 200
        assert upgrade_response.json()["success"] is True