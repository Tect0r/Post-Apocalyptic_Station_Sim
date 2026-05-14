from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone

from metro_sim.interfaces.api.api_state import reset_game_session
from metro_sim.interfaces.api.app import app
from tests.api_test_helpers import authenticated_test_user
from metro_sim.core.tick_config import SECONDS_PER_TICK
from metro_sim.interfaces.api.api_state import get_game_session


client = TestClient(app)


def test_two_users_exist_in_same_world():
    reset_game_session()

    with authenticated_test_user(client, reset_session=False) as user_a:
        with authenticated_test_user(client, reset_session=False) as user_b:
            world_a = client.get("/world", headers=user_a["headers"]).json()
            world_b = client.get("/world", headers=user_b["headers"]).json()

            assert world_a["tick"] == world_b["tick"]
            assert world_a["stations"].keys() == world_b["stations"].keys()

            players_response = client.get("/player", headers=user_a["headers"])

            assert players_response.status_code == 200

            players = players_response.json()["players"]
            player_ids = {player["id"] for player in players}

            assert user_a["player_id"] in player_ids
            assert user_b["player_id"] in player_ids

def test_two_players_influence_same_station_pressure():
    reset_game_session()

    with authenticated_test_user(client, reset_session=False) as user_a:
        with authenticated_test_user(client, reset_session=False) as user_b:
            action_a = client.post(
                "/player/me/actions",
                headers=user_a["headers"],
                json={
                    "action_type": "support_militia",
                    "target_id": "paveletskaya",
                },
            )

            action_b = client.post(
                "/player/me/actions",
                headers=user_b["headers"],
                json={
                    "action_type": "hide_contraband",
                    "target_id": "paveletskaya",
                },
            )

            assert action_a.status_code == 200
            assert action_b.status_code == 200

            duration_a = action_a.json()["data"]["duration_ticks"]
            duration_b = action_b.json()["data"]["duration_ticks"]
            ticks_to_advance = max(duration_a, duration_b)

            session = get_game_session()

            session.last_processed_at = (
                datetime.now(timezone.utc)
                - timedelta(seconds=SECONDS_PER_TICK * ticks_to_advance)
            ).isoformat()

            world_response = client.get(
                "/world",
                headers=user_a["headers"],
            )

            assert world_response.status_code == 200

            station_response = client.get(
                "/stations/paveletskaya",
                headers=user_a["headers"],
            )

            assert station_response.status_code == 200

            station = station_response.json()

            assert station["pressure"]["militia_support"] > 0
            assert station["pressure"]["smuggling"] > 0