from metro_sim.world.models.world_effect import WorldEffect
from metro_sim.world.models.world_log_entry import WorldLogEntry, create_world_log_entry
from metro_sim.world.models.world_state import WorldState


PRODUCTION_INTERVAL_TICKS = 10


PRODUCTION_BY_STATION_TYPE: dict[str, dict[str, int]] = {
    "hansa_station": {
        "food": 12,
        "water": 12,
        "trade_goods": 12,
        "parts": 4,
    },
    "independent_frontier_station": {
        "food": 5,
        "water": 5,
        "ammo": 3,
    },
    "transit_station_complex": {
        "food": 4,
        "water": 4,
        "trade_goods": 5,
    },
    "small_outpost": {
        "food": 3,
        "water": 3,
        "trade_goods": 2,
    },
    "frontier_stronghold": {
        "ammo": 10,
        "food": 4,
        "parts": 4,
        "water": 3,
    },
}


def process_production_tick(world: WorldState) -> tuple[list[WorldEffect], list[WorldLogEntry]]:
    if world.current_tick <= 0:
        return [], []

    if world.current_tick % PRODUCTION_INTERVAL_TICKS != 0:
        return [], []

    effects: list[WorldEffect] = []
    logs: list[WorldLogEntry] = []

    for station_id, station in world.stations.items():
        if not station.inhabited:
            continue

        production = PRODUCTION_BY_STATION_TYPE.get(station.station_type, {})

        if not production:
            continue

        for resource_id, amount in production.items():
            effects.append(
                WorldEffect(
                    target_type="station",
                    target_id=station_id,
                    field_path=["resources", resource_id],
                    operation="add",
                    value=amount,
                    reason="station_production",
                    source="production_system",
                    importance="debug",
                )
            )

        logs.append(
            create_world_log_entry(
                tick=world.current_tick,
                category="station_production",
                message=f"Station production processed for {station_id}.",
                target_type="station",
                target_id=station_id,
                importance="debug",
                data={
                    "station_type": station.station_type,
                    "production": production,
                },
            )
        )

    return effects, logs