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

    if station.inhabited:
        effects.extend(create_inhabited_station_need_effects(station))
        effects.extend(create_basic_station_drift_effects(station))
    else:
        effects.extend(create_abandoned_station_effects(station))

    logs.append(
        create_world_log_entry(
            tick=current_tick,
            category="station_processed",
            message=f"Station processed: {station.id}",
            target_type="station",
            target_id=station.id,
            importance="debug",
            data={
                "inhabited": station.inhabited,
                "station_type": station.station_type,
                "resources": station.resources,
                "stats": station.stats,
                "pressure": station.pressure,
            },
        )
    )

    return StationTickResult(
        station_id=station.id,
        report={
            "station_id": station.id,
            "inhabited": station.inhabited,
            "station_type": station.station_type,
            "resources": station.resources,
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
        "unrest",
        "faction_tension",
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

def create_inhabited_station_need_effects(station: StationState) -> list[WorldEffect]:
    effects: list[WorldEffect] = []

    population = max(0, int(station.population))

    if population <= 0:
        return effects

    food = int(station.resources.get("food", 0))
    water = int(station.resources.get("water", 0))
    medicine = int(station.resources.get("medicine", 0))
    ammo = int(station.resources.get("ammo", 0))

    food_per_100_people = food / max(1, population / 100)
    water_per_100_people = water / max(1, population / 100)
    medicine_per_100_people = medicine / max(1, population / 100)
    ammo_per_100_people = ammo / max(1, population / 100)

    if food_per_100_people < 30:
        effects.extend([
            WorldEffect(
                target_type="station",
                target_id=station.id,
                field_path=["stats", "morale"],
                operation="add",
                value=-1,
                reason="food_shortage",
                source="station_needs",
                importance="normal",
            ),
            WorldEffect(
                target_type="station",
                target_id=station.id,
                field_path=["pressure", "unrest"],
                operation="add",
                value=1,
                reason="food_shortage",
                source="station_needs",
                importance="normal",
            ),
            WorldEffect(
                target_type="station",
                target_id=station.id,
                field_path=["pressure", "supply_disruption"],
                operation="add",
                value=1,
                reason="food_shortage",
                source="station_needs",
                importance="debug",
            ),
        ])

    if water_per_100_people < 25:
        effects.extend([
            WorldEffect(
                target_type="station",
                target_id=station.id,
                field_path=["stats", "health"],
                operation="add",
                value=-1,
                reason="water_shortage",
                source="station_needs",
                importance="normal",
            ),
            WorldEffect(
                target_type="station",
                target_id=station.id,
                field_path=["pressure", "unrest"],
                operation="add",
                value=1,
                reason="water_shortage",
                source="station_needs",
                importance="normal",
            ),
            WorldEffect(
                target_type="station",
                target_id=station.id,
                field_path=["pressure", "supply_disruption"],
                operation="add",
                value=1,
                reason="water_shortage",
                source="station_needs",
                importance="debug",
            ),
        ])

    if medicine_per_100_people < 3:
        effects.extend([
            WorldEffect(
                target_type="station",
                target_id=station.id,
                field_path=["stats", "health"],
                operation="add",
                value=-1,
                reason="medicine_shortage",
                source="station_needs",
                importance="normal",
            ),
            WorldEffect(
                target_type="station",
                target_id=station.id,
                field_path=["pressure", "medical_support"],
                operation="add",
                value=1,
                reason="medicine_shortage",
                source="station_needs",
                importance="debug",
            ),
        ])

    if ammo_per_100_people < 8:
        effects.extend([
            WorldEffect(
                target_type="station",
                target_id=station.id,
                field_path=["stats", "security"],
                operation="add",
                value=-1,
                reason="ammo_shortage",
                source="station_needs",
                importance="normal",
            ),
            WorldEffect(
                target_type="station",
                target_id=station.id,
                field_path=["pressure", "security_risk"],
                operation="add",
                value=1,
                reason="ammo_shortage",
                source="station_needs",
                importance="debug",
            ),
        ])

    return effects

def create_abandoned_station_effects(station: StationState) -> list[WorldEffect]:
    effects: list[WorldEffect] = []

    if "mutant_activity" in station.tags:
        effects.append(
            WorldEffect(
                target_type="station",
                target_id=station.id,
                field_path=["pressure", "danger"],
                operation="add",
                value=1,
                reason="abandoned_mutant_activity",
                source="station_system",
                importance="debug",
            )
        )

    if "bandit_activity" in station.tags:
        effects.append(
            WorldEffect(
                target_type="station",
                target_id=station.id,
                field_path=["pressure", "security_risk"],
                operation="add",
                value=1,
                reason="abandoned_bandit_activity",
                source="station_system",
                importance="debug",
            )
        )

    return effects