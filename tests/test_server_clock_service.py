from datetime import datetime, timedelta, timezone

from metro_sim.core.game_session import create_game_session
from metro_sim.core.server_clock_service import (
    calculate_elapsed_ticks,
    initialize_server_clock,
    process_elapsed_ticks,
)
from metro_sim.core.tick_config import SECONDS_PER_TICK, MAX_CATCHUP_TICKS_PER_REQUEST


def test_initialize_server_clock_sets_last_processed_at():
    session = create_game_session()

    initialize_server_clock(session)

    assert session.last_processed_at is not None


def test_calculate_elapsed_ticks_returns_zero_without_timestamp():
    session = create_game_session()

    assert calculate_elapsed_ticks(session) == 0


def test_calculate_elapsed_ticks_returns_elapsed_game_ticks():
    session = create_game_session()
    session.last_processed_at = (
        datetime.now(timezone.utc) - timedelta(seconds=SECONDS_PER_TICK * 3)
    ).isoformat()

    assert calculate_elapsed_ticks(session) == 3


def test_process_elapsed_ticks_advances_world_tick():
    session = create_game_session()
    session.last_processed_at = (
        datetime.now(timezone.utc) - timedelta(seconds=SECONDS_PER_TICK * 2)
    ).isoformat()

    tick_before = session.world.current_tick

    processed_ticks = process_elapsed_ticks(session)

    assert processed_ticks == 2
    assert session.world.current_tick == tick_before + 2

def test_process_elapsed_ticks_respects_catchup_limit():
    session = create_game_session()
    session.last_processed_at = (
        datetime.now(timezone.utc)
        - timedelta(seconds=SECONDS_PER_TICK * (MAX_CATCHUP_TICKS_PER_REQUEST + 100))
    ).isoformat()

    processed_ticks = process_elapsed_ticks(session)

    assert processed_ticks == MAX_CATCHUP_TICKS_PER_REQUEST
