from datetime import datetime, timedelta, timezone

from metro_sim.core.game_session import GameSession
from metro_sim.core.simulation_tick_service import process_simulation_tick
from metro_sim.core.tick_config import (
    MAX_CATCHUP_TICKS_PER_REQUEST,
    SECONDS_PER_TICK,
)


def initialize_server_clock(session: GameSession) -> None:
    if session.last_processed_at is None:
        session.last_processed_at = datetime.now(timezone.utc).isoformat()


def calculate_elapsed_ticks(session: GameSession) -> int:
    if session.last_processed_at is None:
        return 0

    now = datetime.now(timezone.utc)
    last_processed_at = datetime.fromisoformat(session.last_processed_at)

    elapsed_seconds = (now - last_processed_at).total_seconds()

    if elapsed_seconds < SECONDS_PER_TICK:
        return 0

    return int(elapsed_seconds // SECONDS_PER_TICK)


def process_elapsed_ticks(session: GameSession) -> int:
    initialize_server_clock(session)

    ticks_to_process = calculate_elapsed_ticks(session)

    if ticks_to_process <= 0:
        return 0

    ticks_to_process = min(
        ticks_to_process,
        MAX_CATCHUP_TICKS_PER_REQUEST,
    )

    last_processed_at = datetime.fromisoformat(session.last_processed_at)

    processed_ticks = 0

    for _ in range(ticks_to_process):
        if session.paused or not session.running:
            break

        process_simulation_tick(session)
        processed_ticks += 1

    session.last_processed_at = (
        last_processed_at + timedelta(seconds=processed_ticks * SECONDS_PER_TICK)
    ).isoformat()

    return processed_ticks