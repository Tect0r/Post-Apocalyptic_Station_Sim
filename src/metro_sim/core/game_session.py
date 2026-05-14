from dataclasses import dataclass

from metro_sim.player.factories.player_factory import create_initial_player
from metro_sim.player.models.player_state import PlayerState
from metro_sim.world.factories.world_factory import create_initial_world
from metro_sim.world.models.tick_result import WorldTickResult
from metro_sim.world.models.world_state import WorldState
from metro_sim.world.services.world_tick_service import advance_world_tick
from metro_sim.world.services.action_resolution_service import resolve_completed_player_actions
from metro_sim.world.factories.world_factory import create_world


@dataclass
class GameSession:
    world: WorldState
    players: dict[str, PlayerState]
    last_report: WorldTickResult | None = None
    running: bool = True
    paused: bool = False

def create_game_session() -> GameSession:
    player = create_initial_player()

    return GameSession(
        world=create_initial_world(),
        players={
            player.id: player,
        },
    )

def advance_tick(session: GameSession) -> None:
    session.last_report = advance_world_tick(session.world)

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

def create_game_session() -> GameSession:
    player = create_initial_player()

    return GameSession(
        world=create_world(),
        players={player.id: player},
    )