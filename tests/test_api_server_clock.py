from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from metro_sim.core.tick_config import SECONDS_PER_TICK
from metro_sim.interfaces.api.api_state import get_game_session, reset_game_session
from metro_sim.interfaces.api.app import app
from tests.api_test_helpers import authenticated_test_user

client = TestClient(app)


def test_world_request_processes_elapsed_ticks():
    reset_game_session()

    with authenticated_test_user(client, reset_session=False) as auth:
        session = get_game_session()
        session.last_processed_at = (
            datetime.now(timezone.utc) - timedelta(seconds=SECONDS_PER_TICK * 2)
        ).isoformat()

        tick_before = session.world.current_tick

        response = client.get(
            "/world",
            headers=auth["headers"],
        )

        assert response.status_code == 200
        assert response.json()["tick"] == tick_before + 2

def test_only_world_request_processes_elapsed_ticks():
    reset_game_session()

    with authenticated_test_user(client, reset_session=False) as auth:
        session = get_game_session()
        session.last_processed_at = (
            datetime.now(timezone.utc)
            - timedelta(seconds=SECONDS_PER_TICK * 2)
        ).isoformat()

        tick_before = session.world.current_tick

        world_response = client.get(
            "/world",
            headers=auth["headers"],
        )

        assert world_response.status_code == 200
        assert world_response.json()["tick"] == tick_before + 2

        tick_after_world = get_game_session().world.current_tick

        player_response = client.get(
            "/player/me",
            headers=auth["headers"],
        )

        assert player_response.status_code == 200
        assert get_game_session().world.current_tick == tick_after_world