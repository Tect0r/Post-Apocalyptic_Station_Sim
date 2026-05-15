from metro_sim.world.models.tick_result import WorldTickResult
from metro_sim.world.models.world_state import WorldState
from metro_sim.world.simulation.tick_orchestrator import process_world_tick


def advance_world_tick(world: WorldState) -> WorldTickResult:
    return process_world_tick(world)