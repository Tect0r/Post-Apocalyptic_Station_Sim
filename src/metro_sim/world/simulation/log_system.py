from metro_sim.world.models.world_log_entry import WorldLogEntry
from metro_sim.world.models.world_state import WorldState


MAX_STORED_WORLD_LOGS = 1000


def append_world_logs(
    *,
    world: WorldState,
    logs: list[WorldLogEntry],
) -> None:
    if not logs:
        return

    world.logs.extend(logs)

    if len(world.logs) > MAX_STORED_WORLD_LOGS:
        world.logs = world.logs[-MAX_STORED_WORLD_LOGS:]