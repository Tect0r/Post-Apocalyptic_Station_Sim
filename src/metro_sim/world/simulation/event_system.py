from metro_sim.world.models.world_effect import WorldEffect
from metro_sim.world.models.world_event import WorldEvent, create_world_event
from metro_sim.world.models.world_log_entry import WorldLogEntry, create_world_log_entry
from metro_sim.world.models.world_state import WorldState


def process_world_events(
    world: WorldState,
) -> tuple[list[WorldEvent], list[WorldEffect], list[WorldLogEntry]]:
    events: list[WorldEvent] = []
    effects: list[WorldEffect] = []
    logs: list[WorldLogEntry] = []

    for station_id, station in world.stations.items():
        station.id = station_id

        station_events, station_effects, station_logs = process_station_event_triggers(
            world=world,
            station_id=station_id,
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

    trigger_builders = [
        build_militia_gains_control_event,
        build_sabotage_incident_event,
        build_medical_campaign_success_event,
        build_black_market_expands_event,
        build_mutant_attack_event,
        build_mutant_sighting_event,
        build_supply_shortage_event,
        build_checkpoint_incident_event,
    ]

    for build_event in trigger_builders:
        event, event_effects, event_logs = build_event(
            world=world,
            station_id=station_id,
        )

        if event is None:
            continue

        events.append(event)
        effects.extend(event_effects)
        logs.extend(event_logs)

    return events, effects, logs


def build_militia_gains_control_event(
    *,
    world: WorldState,
    station_id: str,
) -> tuple[WorldEvent | None, list[WorldEffect], list[WorldLogEntry]]:
    station = world.stations[station_id]
    militia_support = station.pressure.get("militia_support", 0)

    if militia_support < 20:
        return None, [], []

    event = create_world_event(
        event_type="militia_gains_control",
        target_type="station",
        target_id=station_id,
        started_at_tick=world.current_tick,
        severity=1,
        causes=["high_militia_support"],
        data={"militia_support": militia_support},
    )

    effects = [
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["stats", "order"],
            operation="add",
            value=3,
            reason="militia_gains_control",
            source="event_system",
            importance="normal",
        ),
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["pressure", "militia_support"],
            operation="set",
            value=0,
            reason="militia_gains_control_resolved",
            source="event_system",
            importance="debug",
        ),
    ]

    logs = [
        create_event_log(
            world=world,
            event=event,
            message=f"Militia forces gained control in {station_id}.",
        )
    ]

    return event, effects, logs


def build_sabotage_incident_event(
    *,
    world: WorldState,
    station_id: str,
) -> tuple[WorldEvent | None, list[WorldEffect], list[WorldLogEntry]]:
    station = world.stations[station_id]
    sabotage = station.pressure.get("sabotage", 0)

    if sabotage < 20:
        return None, [], []

    event = create_world_event(
        event_type="sabotage_incident",
        target_type="station",
        target_id=station_id,
        started_at_tick=world.current_tick,
        severity=1,
        causes=["high_sabotage_pressure"],
        data={"sabotage": sabotage},
    )

    effects = [
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["stats", "security"],
            operation="add",
            value=-5,
            reason="sabotage_incident",
            source="event_system",
            importance="normal",
        ),
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["stats", "morale"],
            operation="add",
            value=-2,
            reason="sabotage_incident",
            source="event_system",
            importance="normal",
        ),
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["pressure", "sabotage"],
            operation="set",
            value=0,
            reason="sabotage_incident_resolved",
            source="event_system",
            importance="debug",
        ),
    ]

    logs = [
        create_event_log(
            world=world,
            event=event,
            message=f"A sabotage incident damaged security in {station_id}.",
        )
    ]

    return event, effects, logs


def build_medical_campaign_success_event(
    *,
    world: WorldState,
    station_id: str,
) -> tuple[WorldEvent | None, list[WorldEffect], list[WorldLogEntry]]:
    station = world.stations[station_id]
    medical_support = station.pressure.get("medical_support", 0)

    if medical_support < 20:
        return None, [], []

    event = create_world_event(
        event_type="medical_campaign_success",
        target_type="station",
        target_id=station_id,
        started_at_tick=world.current_tick,
        severity=1,
        causes=["high_medical_support"],
        data={"medical_support": medical_support},
    )

    effects = [
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["stats", "health"],
            operation="add",
            value=4,
            reason="medical_campaign_success",
            source="event_system",
            importance="normal",
        ),
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["stats", "morale"],
            operation="add",
            value=1,
            reason="medical_campaign_success",
            source="event_system",
            importance="normal",
        ),
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["pressure", "medical_support"],
            operation="set",
            value=0,
            reason="medical_campaign_success_resolved",
            source="event_system",
            importance="debug",
        ),
    ]

    logs = [
        create_event_log(
            world=world,
            event=event,
            message=f"Medical support improved health conditions in {station_id}.",
        )
    ]

    return event, effects, logs


def build_black_market_expands_event(
    *,
    world: WorldState,
    station_id: str,
) -> tuple[WorldEvent | None, list[WorldEffect], list[WorldLogEntry]]:
    station = world.stations[station_id]
    smuggling = station.pressure.get("smuggling", 0)

    if smuggling < 20:
        return None, [], []

    event = create_world_event(
        event_type="black_market_expands",
        target_type="station",
        target_id=station_id,
        started_at_tick=world.current_tick,
        severity=1,
        causes=["high_smuggling_pressure"],
        data={"smuggling": smuggling},
    )

    effects = [
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["stats", "order"],
            operation="add",
            value=-3,
            reason="black_market_expands",
            source="event_system",
            importance="normal",
        ),
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["stats", "morale"],
            operation="add",
            value=1,
            reason="black_market_expands",
            source="event_system",
            importance="normal",
        ),
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["pressure", "smuggling"],
            operation="set",
            value=0,
            reason="black_market_expands_resolved",
            source="event_system",
            importance="debug",
        ),
    ]

    logs = [
        create_event_log(
            world=world,
            event=event,
            message=f"Black market activity expanded in {station_id}.",
        )
    ]

    return event, effects, logs


def create_event_log(
    *,
    world: WorldState,
    event: WorldEvent,
    message: str,
) -> WorldLogEntry:
    return create_world_log_entry(
        tick=world.current_tick,
        category="world_event",
        message=message,
        target_type=event.target_type,
        target_id=event.target_id,
        importance="normal",
        data={
            "event_id": event.id,
            "event_type": event.event_type,
            "causes": event.causes,
            "severity": event.severity,
        },
    )

def build_mutant_sighting_event(
    *,
    world: WorldState,
    station_id: str,
) -> tuple[WorldEvent | None, list[WorldEffect], list[WorldLogEntry]]:
    station = world.stations[station_id]
    danger = station.pressure.get("danger", 0)

    danger = station.pressure.get("danger", 0)

    if danger < 20 or danger >= 50:
        return None, [], []

    event = create_world_event(
        event_type="mutant_sighting",
        target_type="station",
        target_id=station_id,
        started_at_tick=world.current_tick,
        severity=1,
        causes=["high_route_danger_pressure"],
        data={"danger": danger},
    )

    effects = [
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["stats", "morale"],
            operation="add",
            value=-2,
            reason="mutant_sighting",
            source="event_system",
            importance="normal",
        ),
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["stats", "security"],
            operation="add",
            value=-1,
            reason="mutant_sighting",
            source="event_system",
            importance="normal",
        ),
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["pressure", "danger"],
            operation="set",
            value=0,
            reason="mutant_sighting_resolved",
            source="event_system",
            importance="debug",
        ),
    ]

    logs = [
        create_event_log(
            world=world,
            event=event,
            message=f"Mutant activity was sighted near {station_id}.",
        )
    ]

    return event, effects, logs


def build_supply_shortage_event(
    *,
    world: WorldState,
    station_id: str,
) -> tuple[WorldEvent | None, list[WorldEffect], list[WorldLogEntry]]:
    station = world.stations[station_id]
    supply_disruption = station.pressure.get("supply_disruption", 0)

    if supply_disruption < 20:
        return None, [], []

    event = create_world_event(
        event_type="supply_shortage",
        target_type="station",
        target_id=station_id,
        started_at_tick=world.current_tick,
        severity=1,
        causes=["high_supply_disruption_pressure"],
        data={"supply_disruption": supply_disruption},
    )

    effects = [
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["stats", "morale"],
            operation="add",
            value=-3,
            reason="supply_shortage",
            source="event_system",
            importance="normal",
        ),
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["stats", "order"],
            operation="add",
            value=-2,
            reason="supply_shortage",
            source="event_system",
            importance="normal",
        ),
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["pressure", "supply_disruption"],
            operation="set",
            value=0,
            reason="supply_shortage_resolved",
            source="event_system",
            importance="debug",
        ),
    ]

    logs = [
        create_event_log(
            world=world,
            event=event,
            message=f"Supply disruption caused shortages in {station_id}.",
        )
    ]

    return event, effects, logs


def build_checkpoint_incident_event(
    *,
    world: WorldState,
    station_id: str,
) -> tuple[WorldEvent | None, list[WorldEffect], list[WorldLogEntry]]:
    station = world.stations[station_id]
    security_risk = station.pressure.get("security_risk", 0)

    if security_risk < 20:
        return None, [], []

    event = create_world_event(
        event_type="checkpoint_incident",
        target_type="station",
        target_id=station_id,
        started_at_tick=world.current_tick,
        severity=1,
        causes=["high_security_risk_pressure"],
        data={"security_risk": security_risk},
    )

    effects = [
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["stats", "order"],
            operation="add",
            value=-2,
            reason="checkpoint_incident",
            source="event_system",
            importance="normal",
        ),
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["stats", "security"],
            operation="add",
            value=-2,
            reason="checkpoint_incident",
            source="event_system",
            importance="normal",
        ),
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["pressure", "security_risk"],
            operation="set",
            value=0,
            reason="checkpoint_incident_resolved",
            source="event_system",
            importance="debug",
        ),
    ]

    logs = [
        create_event_log(
            world=world,
            event=event,
            message=f"A checkpoint incident increased tension in {station_id}.",
        )
    ]

    return event, effects, logs

def build_mutant_attack_event(
    *,
    world: WorldState,
    station_id: str,
) -> tuple[WorldEvent | None, list[WorldEffect], list[WorldLogEntry]]:
    station = world.stations[station_id]
    danger = station.pressure.get("danger", 0)

    if danger < 50:
        return None, [], []

    event = create_world_event(
        event_type="mutant_attack",
        target_type="station",
        target_id=station_id,
        started_at_tick=world.current_tick,
        status="running",
        duration_ticks=30,
        current_phase="approaching",
        severity=2,
        causes=["critical_route_danger_pressure"],
        data={"danger": danger},
    )

    effects = [
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["pressure", "danger"],
            operation="set",
            value=0,
            reason="mutant_attack_started",
            source="event_system",
            importance="debug",
        )
    ]

    logs = [
        create_event_log(
            world=world,
            event=event,
            message=f"A mutant attack started at {station_id}.",
        )
    ]

    return event, effects, logs