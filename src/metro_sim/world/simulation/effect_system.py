from typing import Any

from metro_sim.world.models.world_effect import WorldEffect
from metro_sim.world.models.world_log_entry import WorldLogEntry, create_world_log_entry
from metro_sim.world.models.world_state import WorldState


NUMERIC_LIMITS: dict[tuple[str, ...], tuple[int, int]] = {
    ("stats", "morale"): (0, 100),
    ("stats", "order"): (0, 100),
    ("stats", "security"): (0, 100),
    ("stats", "health"): (0, 100),
    ("stats", "comfort"): (0, 100),
    
    ("pressure", "sabotage"): (0, 100),
    ("pressure", "militia_support"): (0, 100),
    ("pressure", "medical_support"): (0, 100),
    ("pressure", "smuggling"): (0, 100),
    ("pressure", "danger"): (0, 100),
    ("pressure", "supply_disruption"): (0, 100),
    ("pressure", "security_risk"): (0, 100),

    ("pressure", "unrest"): (0, 100),
    ("pressure", "faction_tension"): (0, 100),
}


SUPPORTED_TARGET_TYPES = {
    "station",
}


SUPPORTED_OPERATIONS = {
    "add",
    "subtract",
    "set",
}


def apply_world_effects(
    *,
    world: WorldState,
    effects: list[WorldEffect],
) -> list[WorldLogEntry]:
    logs: list[WorldLogEntry] = []

    for effect in effects:
        if effect.operation not in SUPPORTED_OPERATIONS:
            logs.append(create_failed_effect_log(
                world=world,
                effect=effect,
                reason=f"Unsupported effect operation: {effect.operation}",
            ))
            continue

        if effect.target_type not in SUPPORTED_TARGET_TYPES:
            logs.append(create_failed_effect_log(
                world=world,
                effect=effect,
                reason=f"Unsupported effect target type: {effect.target_type}",
            ))
            continue

        target = resolve_effect_target(
            world=world,
            effect=effect,
        )

        if target is None:
            logs.append(create_failed_effect_log(
                world=world,
                effect=effect,
                reason=f"Effect target not found: {effect.target_id}",
            ))
            continue

        try:
            old_value = get_nested_value(target, effect.field_path)
            new_value = calculate_new_value(
                old_value=old_value,
                operation=effect.operation,
                value=effect.value,
            )
            new_value = clamp_value(effect.field_path, new_value)

            set_nested_value(target, effect.field_path, new_value)

            logs.append(create_applied_effect_log(
                world=world,
                effect=effect,
                old_value=old_value,
                new_value=new_value,
            ))

        except (AttributeError, KeyError, TypeError, ValueError) as error:
            logs.append(create_failed_effect_log(
                world=world,
                effect=effect,
                reason=str(error),
            ))

    return logs


def resolve_effect_target(
    *,
    world: WorldState,
    effect: WorldEffect,
) -> Any | None:
    if effect.target_type == "station":
        return world.stations.get(effect.target_id)

    return None


def get_nested_value(target: Any, field_path: list[str]) -> Any:
    current: Any = target

    for part in field_path:
        if isinstance(current, dict):
            if part not in current:
                raise KeyError(f"Field path not found: {'.'.join(field_path)}")
            current = current[part]
        else:
            if not hasattr(current, part):
                raise AttributeError(f"Field path not found: {'.'.join(field_path)}")
            current = getattr(current, part)

    return current


def set_nested_value(target: Any, field_path: list[str], value: Any) -> None:
    current: Any = target

    for part in field_path[:-1]:
        if isinstance(current, dict):
            if part not in current:
                raise KeyError(f"Field path not found: {'.'.join(field_path)}")
            current = current[part]
        else:
            if not hasattr(current, part):
                raise AttributeError(f"Field path not found: {'.'.join(field_path)}")
            current = getattr(current, part)

    final_key = field_path[-1]

    if isinstance(current, dict):
        if final_key not in current:
            raise KeyError(f"Field path not found: {'.'.join(field_path)}")
        current[final_key] = value
    else:
        if not hasattr(current, final_key):
            raise AttributeError(f"Field path not found: {'.'.join(field_path)}")
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


def create_applied_effect_log(
    *,
    world: WorldState,
    effect: WorldEffect,
    old_value: Any,
    new_value: Any,
) -> WorldLogEntry:
    return create_world_log_entry(
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
            "effect_id": effect.id,
            "field_path": effect.field_path,
            "operation": effect.operation,
            "value": effect.value,
            "old_value": old_value,
            "new_value": new_value,
            "reason": effect.reason,
            "source": effect.source,
        },
    )


def create_failed_effect_log(
    *,
    world: WorldState,
    effect: WorldEffect,
    reason: str,
) -> WorldLogEntry:
    return create_world_log_entry(
        tick=world.current_tick,
        category="effect_failed",
        message=f"Effect failed: {reason}",
        target_type=effect.target_type,
        target_id=effect.target_id,
        importance="warning",
        data={
            "effect_id": effect.id,
            "field_path": effect.field_path,
            "operation": effect.operation,
            "value": effect.value,
            "reason": effect.reason,
            "source": effect.source,
            "failure_reason": reason,
        },
    )