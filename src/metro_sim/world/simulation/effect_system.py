from typing import Any

from metro_sim.world.models.world_effect import WorldEffect
from metro_sim.world.models.world_log_entry import WorldLogEntry, create_world_log_entry
from metro_sim.world.models.world_state import WorldState


NUMERIC_LIMITS: dict[tuple[str, ...], tuple[int, int]] = {
    ("stats", "morale"): (0, 100),
    ("stats", "order"): (0, 100),
    ("stats", "security"): (0, 100),
    ("stats", "health"): (0, 100),
}


def apply_world_effects(
    *,
    world: WorldState,
    effects: list[WorldEffect],
) -> list[WorldLogEntry]:
    logs: list[WorldLogEntry] = []

    for effect in effects:
        if effect.target_type != "station":
            logs.append(
                create_world_log_entry(
                    tick=world.current_tick,
                    category="effect_skipped",
                    message=f"Unsupported effect target type: {effect.target_type}",
                    target_type=effect.target_type,
                    target_id=effect.target_id,
                    importance="debug",
                    data={"effect": effect.__dict__},
                )
            )
            continue

        station = world.stations.get(effect.target_id)

        if station is None:
            logs.append(
                create_world_log_entry(
                    tick=world.current_tick,
                    category="effect_failed",
                    message=f"Effect target not found: {effect.target_id}",
                    target_type=effect.target_type,
                    target_id=effect.target_id,
                    importance="warning",
                    data={"effect": effect.__dict__},
                )
            )
            continue

        old_value = get_nested_value(station, effect.field_path)
        new_value = calculate_new_value(
            old_value=old_value,
            operation=effect.operation,
            value=effect.value,
        )
        new_value = clamp_value(effect.field_path, new_value)

        set_nested_value(station, effect.field_path, new_value)

        logs.append(
            create_world_log_entry(
                tick=world.current_tick,
                category="effect_applied",
                message=(
                    f"{effect.target_id}: "
                    f"{'.'.join(effect.field_path)} changed "
                    f"from {old_value} to {new_value}"
                ),
                target_type=effect.target_type,
                target_id=effect.target_id,
                importance=effect.importance,
                data={
                    "field_path": effect.field_path,
                    "operation": effect.operation,
                    "value": effect.value,
                    "old_value": old_value,
                    "new_value": new_value,
                    "reason": effect.reason,
                    "source": effect.source,
                },
            )
        )

    return logs


def get_nested_value(target: Any, field_path: list[str]) -> Any:
    current: Any = target

    for part in field_path:
        if isinstance(current, dict):
            current = current.get(part, 0)
        else:
            current = getattr(current, part)

    return current


def set_nested_value(target: Any, field_path: list[str], value: Any) -> None:
    current: Any = target

    for part in field_path[:-1]:
        if isinstance(current, dict):
            current = current.setdefault(part, {})
        else:
            current = getattr(current, part)

    final_key = field_path[-1]

    if isinstance(current, dict):
        current[final_key] = value
    else:
        setattr(current, final_key, value)


def calculate_new_value(*, old_value: Any, operation: str, value: Any) -> Any:
    if operation == "add":
        return old_value + value

    if operation == "subtract":
        return old_value - value

    if operation == "set":
        return value

    raise ValueError(f"Unsupported effect operation: {operation}")


def clamp_value(field_path: list[str], value: Any) -> Any:
    limits = NUMERIC_LIMITS.get(tuple(field_path))

    if limits is None:
        return value

    minimum, maximum = limits
    return max(minimum, min(maximum, value))