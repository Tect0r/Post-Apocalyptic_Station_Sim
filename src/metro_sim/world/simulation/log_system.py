from metro_sim.world.models.world_log_entry import WorldLogEntry
from metro_sim.world.models.world_state import WorldState


MAX_STORED_WORLD_LOGS = 1000

VISIBLE_IMPORTANCE_LEVELS = {
    "normal",
    "important",
    "critical",
}


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


def get_visible_world_logs(
    *,
    world: WorldState,
    limit: int = 50,
) -> list[WorldLogEntry]:
    visible_logs = [
        log for log in world.logs
        if log.importance in VISIBLE_IMPORTANCE_LEVELS
    ]

    return visible_logs[-limit:]


def get_debug_world_logs(
    *,
    world: WorldState,
    limit: int = 100,
) -> list[WorldLogEntry]:
    return world.logs[-limit:]


def get_logs_by_category(
    *,
    world: WorldState,
    category: str,
    limit: int = 50,
) -> list[WorldLogEntry]:
    matching_logs = [
        log for log in world.logs
        if log.category == category
    ]

    return matching_logs[-limit:]


def get_logs_for_target(
    *,
    world: WorldState,
    target_type: str,
    target_id: str,
    limit: int = 50,
) -> list[WorldLogEntry]:
    matching_logs = [
        log for log in world.logs
        if log.target_type == target_type and log.target_id == target_id
    ]

    return matching_logs[-limit:]