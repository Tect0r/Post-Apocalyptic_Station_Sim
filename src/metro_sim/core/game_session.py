from dataclasses import dataclass

from metro_sim.world.factories.world_factory import create_initial_world
from metro_sim.world.models.tick_result import WorldTickResult
from metro_sim.world.models.world_state import WorldState
from metro_sim.world.services.world_tick_service import advance_world_tick


@dataclass
class GameSession:
    world: WorldState
    last_report: WorldTickResult | None = None
    running: bool = True
    paused: bool = False


def create_game_session() -> GameSession:
    return GameSession(
        world=create_initial_world(),
    )


def advance_tick(session: GameSession) -> None:
    session.last_report = advance_world_tick(session.world)