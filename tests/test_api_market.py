from fastapi.testclient import TestClient

from metro_sim.interfaces.api.app import app
from tests.api_test_helpers import authenticated_test_user
from metro_sim.interfaces.api.api_state import get_game_session

client = TestClient(app)


def test_get_current_market():
    with authenticated_test_user(client) as auth:
        response = client.get(
            "/market",
            headers=auth["headers"],
        )

        assert response.status_code == 200
        assert response.json()["station_id"] == "paveletskaya_radial"
        assert "prices" in response.json()


def test_buy_market_item_via_api():
    with authenticated_test_user(client) as auth:
        session = get_game_session()
        player = session.players["player_001"]
        station = session.world.stations[player.crew.current_location_id]

        station.market.setdefault("stock", {})
        station.market["stock"]["food"] = 10

        station.market.setdefault("item_prices", {})
        station.market["item_prices"]["food"] = 1

        player.inventory.items["currency"] = 100

        response = client.post(
            "/market/buy",
            headers=auth["headers"],
            json={
                "item_id": "food",
                "amount": 1,
            },
        )

        assert response.status_code == 200
        assert response.json()["success"] is True

def test_sell_market_item_via_api():
    with authenticated_test_user(client) as auth:
        session = get_game_session()
        player = session.players["player_001"]
        station = session.world.stations[player.crew.current_location_id]

        station.market.setdefault("stock", {})
        station.market["stock"]["food"] = 10

        station.market.setdefault("item_prices", {})
        station.market["item_prices"]["food"] = 1

        player.inventory.items["currency"] = 100

        buy_response = client.post(
            "/market/buy",
            headers=auth["headers"],
            json={
                "item_id": "food",
                "amount": 1,
            },
        )

        assert buy_response.status_code == 200
        assert buy_response.json()["success"] is True

        sell_response = client.post(
            "/market/sell",
            headers=auth["headers"],
            json={
                "item_id": "food",
                "amount": 1,
            },
        )

        assert sell_response.status_code == 200
        assert sell_response.json()["success"] is True