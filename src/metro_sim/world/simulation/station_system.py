from metro_sim.world.models.station_state import StationState
from metro_sim.world.models.tick_result import StationTickResult
from metro_sim.world.models.world_effect import WorldEffect
from metro_sim.world.models.world_log_entry import create_world_log_entry

NON_DECAYING_PRESSURES = {
    "danger",
    "supply_disruption",
    "security_risk",
}

def process_station_tick(
    *,
    station: StationState,
    current_tick: int,
) -> StationTickResult:
    effects: list[WorldEffect] = []
    logs = []

    effects.extend(create_pressure_decay_effects(station))
    effects.extend(create_basic_station_drift_effects(station))

    logs.append(
        create_world_log_entry(
            tick=current_tick,
            category="station_processed",
            message=f"Station processed: {station.id}",
            target_type="station",
            target_id=station.id,
            importance="debug",
            data={
                "stats": station.stats,
                "pressure": station.pressure,
            },
        )
    )

    return StationTickResult(
        station_id=station.id,
        report={
            "station_id": station.id,
            "pressure": station.pressure,
            "stats": station.stats,
            "faction_influence": station.faction_influence,
        },
        effects=effects,
        logs=logs,
    )


def create_pressure_decay_effects(station: StationState) -> list[WorldEffect]:
    effects: list[WorldEffect] = []

    non_decaying_pressures = {
        "danger",
        "supply_disruption",
        "security_risk",
    }

    for pressure_name, pressure_value in station.pressure.items():
        if pressure_name in non_decaying_pressures:
            continue

        if pressure_value <= 0:
            continue

        effects.append(
            WorldEffect(
                target_type="station",
                target_id=station.id,
                field_path=["pressure", pressure_name],
                operation="add",
                value=-1,
                reason="pressure_decay",
                source="station_system",
                importance="debug",
            )
        )

    return effects


def create_basic_station_drift_effects(station: StationState) -> list[WorldEffect]:
    effects: list[WorldEffect] = []

    if station.pressure.get("sabotage", 0) >= 20:
        effects.append(
            WorldEffect(
                target_type="station",
                target_id=station.id,
                field_path=["stats", "security"],
                operation="add",
                value=-1,
                reason="sabotage_pressure",
                source="station_system",
            )
        )

    if station.pressure.get("medical_support", 0) >= 10:
        effects.append(
            WorldEffect(
                target_type="station",
                target_id=station.id,
                field_path=["stats", "health"],
                operation="add",
                value=1,
                reason="medical_support_pressure",
                source="station_system",
            )
        )

    if station.pressure.get("militia_support", 0) >= 10:
        effects.append(
            WorldEffect(
                target_type="station",
                target_id=station.id,
                field_path=["stats", "order"],
                operation="add",
                value=1,
                reason="militia_support_pressure",
                source="station_system",
            )
        )

    if station.pressure.get("smuggling", 0) >= 15:
        effects.append(
            WorldEffect(
                target_type="station",
                target_id=station.id,
                field_path=["stats", "order"],
                operation="add",
                value=-1,
                reason="smuggling_pressure",
                source="station_system",
            )
        )

    return effects