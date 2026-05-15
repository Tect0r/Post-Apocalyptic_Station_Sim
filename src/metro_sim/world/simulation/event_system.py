from metro_sim.world.models.world_effect import WorldEffect
from metro_sim.world.models.world_event import WorldEvent, create_world_event
from metro_sim.world.models.world_log_entry import WorldLogEntry, create_world_log_entry
from metro_sim.world.models.world_state import WorldState


def process_world_events(world: WorldState) -> tuple[list[WorldEvent], list[WorldEffect], list[WorldLogEntry]]:
    events: list[WorldEvent] = []
    effects: list[WorldEffect] = []
    logs: list[WorldLogEntry] = []

    for station in world.stations.values():
        station_events, station_effects, station_logs = process_station_event_triggers(
            world=world,
            station_id=station.id,
        )

        events.extend(station_events)
        effects.extend(station_effects)
        logs.extend(station_logs)

    if events:
        world.events.extend(events)

    return events, effects, logs


def process_station_event_triggers(
    *,
    world: WorldState,
    station_id: str,
) -> tuple[list[WorldEvent], list[WorldEffect], list[WorldLogEntry]]:
    station = world.stations[station_id]

    events: list[WorldEvent] = []
    effects: list[WorldEffect] = []
    logs: list[WorldLogEntry] = []

    militia_support = station.pressure.get("militia_support", 0)

    if militia_support >= 20:
        event = create_world_event(
            event_type="militia_gains_control",
            target_type="station",
            target_id=station.id,
            started_at_tick=world.current_tick,
            severity=1,
            causes=["high_militia_support"],
            data={
                "militia_support": militia_support,
            },
        )

        events.append(event)

        effects.append(
            WorldEffect(
                target_type="station",
                target_id=station.id,
                field_path=["stats", "order"],
                operation="add",
                value=3,
                reason="militia_gains_control",
                source="event_system",
                importance="normal",
            )
        )

        effects.append(
            WorldEffect(
                target_type="station",
                target_id=station.id,
                field_path=["pressure", "militia_support"],
                operation="set",
                value=0,
                reason="militia_gains_control_resolved",
                source="event_system",
                importance="debug",
            )
        )

        logs.append(
            create_world_log_entry(
                tick=world.current_tick,
                category="world_event",
                message=f"Militia gained control in {station.id}.",
                target_type="station",
                target_id=station.id,
                importance="normal",
                data={
                    "event_type": event.event_type,
                    "event_id": event.id,
                    "causes": event.causes,
                },
            )
        )

    return events, effects, logs