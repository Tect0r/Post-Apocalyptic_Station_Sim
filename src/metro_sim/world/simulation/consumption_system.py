from metro_sim.world.models.world_effect import WorldEffect
from metro_sim.world.models.world_log_entry import WorldLogEntry, create_world_log_entry
from metro_sim.world.models.world_state import WorldState


CONSUMPTION_INTERVAL_TICKS = 30


def process_consumption_tick(world: WorldState) -> tuple[list[WorldEffect], list[WorldLogEntry]]:
    if world.current_tick <= 0:
        return [], []

    if world.current_tick % CONSUMPTION_INTERVAL_TICKS != 0:
        return [], []

    effects: list[WorldEffect] = []
    logs: list[WorldLogEntry] = []

    for station_id, station in world.stations.items():
        if not station.inhabited:
            continue

        consumption = calculate_station_consumption(station)

        for resource_id, amount in consumption.items():
            if amount <= 0:
                continue

            current_amount = int(station.resources.get(resource_id, 0))
            actual_amount = min(current_amount, amount)

            if actual_amount <= 0:
                continue

            effects.append(
                WorldEffect(
                    target_type="station",
                    target_id=station_id,
                    field_path=["resources", resource_id],
                    operation="subtract",
                    value=actual_amount,
                    reason="station_consumption",
                    source="consumption_system",
                    importance="debug",
                )
            )

        logs.append(
            create_world_log_entry(
                tick=world.current_tick,
                category="station_consumption",
                message=f"Station consumption processed for {station_id}.",
                target_type="station",
                target_id=station_id,
                importance="debug",
                data={
                    "population": station.population,
                    "requested_consumption": consumption,
                },
            )
        )

    return effects, logs


def calculate_station_consumption(station) -> dict[str, int]:
    population = max(0, int(station.population))

    # intentionally coarse v1:
    # per 100 people per consumption interval
    population_units = population / 100

    food = round(population_units * 0.5)
    water = round(population_units * 0.5)
    medicine = round(population_units * 0.05)

    ammo = 0
    if station.station_type in {
        "independent_frontier_station",
        "frontier_stronghold",
        "small_outpost",
    }:
        ammo = round(population_units * 0.5)

    return {
        "food": max(0, food),
        "water": max(0, water),
        "medicine": max(0, medicine),
        "ammo": max(0, ammo),
    }