from dataclasses import dataclass

from metro_sim.player.factories.player_factory import create_initial_player
from metro_sim.player.models.player_state import PlayerState
from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.models.tick_result import WorldTickResult
from metro_sim.world.models.world_state import WorldState

@dataclass
class GameSession:
    world: WorldState
    players: dict[str, PlayerState]
    last_report: WorldTickResult | None = None
    last_processed_at: str | None = None
    running: bool = True
    paused: bool = False


def create_game_session() -> GameSession:
    player = create_initial_player()

    return GameSession(
        world=create_world(),
        players={player.id: player},
    )


def advance_tick(session: GameSession) -> None:
    from metro_sim.core.simulation_tick_service import process_simulation_tick

    process_simulation_tick(session)