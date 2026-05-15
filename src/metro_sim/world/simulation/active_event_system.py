from metro_sim.world.models.world_effect import WorldEffect
from metro_sim.world.models.world_event import WorldEvent
from metro_sim.world.models.world_log_entry import WorldLogEntry, create_world_log_entry
from metro_sim.world.models.world_state import WorldState


def process_active_events(
    world: WorldState,
) -> tuple[list[WorldEffect], list[WorldLogEntry]]:
    effects: list[WorldEffect] = []
    logs: list[WorldLogEntry] = []

    for event in world.events:
        if event.status != "running":
            continue

        event_effects, event_logs = process_single_active_event(
            world=world,
            event=event,
        )

        effects.extend(event_effects)
        logs.extend(event_logs)

    return effects, logs


def process_single_active_event(
    *,
    world: WorldState,
    event: WorldEvent,
) -> tuple[list[WorldEffect], list[WorldLogEntry]]:
    if event.event_type == "mutant_attack":
        return process_mutant_attack_event(
            world=world,
            event=event,
        )

    return [], []


def process_mutant_attack_event(
    *,
    world: WorldState,
    event: WorldEvent,
) -> tuple[list[WorldEffect], list[WorldLogEntry]]:
    effects: list[WorldEffect] = []
    logs: list[WorldLogEntry] = []

    if event.ends_at_tick is None:
        return [], []

    ticks_elapsed = world.current_tick - event.started_at_tick

    new_phase = determine_mutant_attack_phase(
        ticks_elapsed=ticks_elapsed,
        duration_ticks=event.duration_ticks,
    )

    if new_phase != event.current_phase:
        event.current_phase = new_phase

        logs.append(
            create_world_log_entry(
                tick=world.current_tick,
                category="event_phase_changed",
                message=f"Mutant attack at {event.target_id} entered phase: {new_phase}",
                target_type=event.target_type,
                target_id=event.target_id,
                importance="normal",
                data={
                    "event_id": event.id,
                    "event_type": event.event_type,
                    "phase": new_phase,
                },
            )
        )

    if world.current_tick >= event.ends_at_tick:
        event.status = "completed"

        effects.extend([
            WorldEffect(
                target_type=event.target_type,
                target_id=event.target_id,
                field_path=["stats", "morale"],
                operation="add",
                value=-5,
                reason="mutant_attack_resolved",
                source="active_event_system",
                importance="important",
            ),
            WorldEffect(
                target_type=event.target_type,
                target_id=event.target_id,
                field_path=["stats", "security"],
                operation="add",
                value=-3,
                reason="mutant_attack_resolved",
                source="active_event_system",
                importance="important",
            ),
        ])

        logs.append(
            create_world_log_entry(
                tick=world.current_tick,
                category="event_completed",
                message=f"Mutant attack at {event.target_id} ended.",
                target_type=event.target_type,
                target_id=event.target_id,
                importance="important",
                data={
                    "event_id": event.id,
                    "event_type": event.event_type,
                    "duration_ticks": event.duration_ticks,
                },
            )
        )

    return effects, logs


def determine_mutant_attack_phase(
    *,
    ticks_elapsed: int,
    duration_ticks: int,
) -> str:
    if duration_ticks <= 0:
        return "unknown"

    progress = ticks_elapsed / duration_ticks

    if progress < 0.25:
        return "approaching"

    if progress < 0.50:
        return "first_contact"

    if progress < 0.75:
        return "breach_attempt"

    return "aftermath"