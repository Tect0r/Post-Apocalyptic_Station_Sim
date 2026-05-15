from metro_sim.core.game_session import GameSession
from metro_sim.world.services.action_resolution_service import resolve_completed_player_actions
from metro_sim.world.simulation.tick_orchestrator import process_world_tick


def process_simulation_tick(session: GameSession) -> None:
    """
    Processes one full simulation tick.

    This is the orchestration layer above the pure world tick.

    World tick:
    - stations
    - routes later
    - markets later
    - factions later
    - events later
    - effects/logs

    Actor tick:
    - player actions
    - contract completion
    - asset rewards
    - later NPC/faction/AI actors
    """
    if session.paused or not session.running:
        return

    session.last_report = process_world_tick(session.world)

    completed_actions = resolve_completed_player_actions(
        world=session.world,
        players=session.players,
    )

    if not completed_actions:
        return

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