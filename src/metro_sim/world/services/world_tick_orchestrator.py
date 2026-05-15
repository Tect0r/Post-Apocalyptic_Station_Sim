from dataclasses import dataclass, field

from metro_sim.core.game_session import GameSession
from metro_sim.world.services.world_tick_service import advance_world_tick
from metro_sim.world.services.action_resolution_service import resolve_completed_player_actions


@dataclass
class TickProcessingResult:
    start_tick: int
    end_tick: int
    processed_ticks: int
    reports: list = field(default_factory=list)


def process_single_tick(session: GameSession) -> None:
    if session.paused or not session.running:
        return

    session.last_report = advance_world_tick(session.world)

    # Später optional machen oder in eigenes System auslagern.
    completed_actions = resolve_completed_player_actions(
        world=session.world,
        players=session.players,
    )

    if completed_actions:
        session.last_report.events.extend(
            {
                "type": "player_action_completed",
                "player_id": action.player_id,
                "action_id": action.id,
                "action_type": action.action_type.value,
                "target_type": action.target_type,
                "target_id": action.target_id,
            }
            for action in completed_actions
        )


def process_ticks(session: GameSession, amount: int) -> TickProcessingResult:
    start_tick = session.world.current_tick

    for _ in range(amount):
        process_single_tick(session)

    return TickProcessingResult(
        start_tick=start_tick,
        end_tick=session.world.current_tick,
        processed_ticks=session.world.current_tick - start_tick,
    )