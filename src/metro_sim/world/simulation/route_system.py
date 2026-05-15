from metro_sim.world.models.world_effect import WorldEffect
from metro_sim.world.models.world_log_entry import WorldLogEntry, create_world_log_entry
from metro_sim.world.models.world_state import WorldState


def process_routes_tick(world: WorldState) -> tuple[list[WorldEffect], list[WorldLogEntry]]:
    effects: list[WorldEffect] = []
    logs: list[WorldLogEntry] = []

    for route_id, route in world.routes.items():
        route.id = route_id

        route_effects, route_logs = process_single_route_tick(
            world=world,
            route_id=route_id,
        )

        effects.extend(route_effects)
        logs.extend(route_logs)

    return effects, logs


def process_single_route_tick(
    *,
    world: WorldState,
    route_id: str,
) -> tuple[list[WorldEffect], list[WorldLogEntry]]:
    route = world.routes[route_id]

    effects: list[WorldEffect] = []
    logs: list[WorldLogEntry] = []

    danger = getattr(route, "danger", 0)
    condition = getattr(route, "condition", 100)
    traffic = getattr(route, "traffic", 0)
    travel_time_ticks = getattr(route, "travel_time_ticks", 60)

    connected_station_ids = [
        getattr(route, "from_station_id", None),
        getattr(route, "to_station_id", None),
    ]

    connected_station_ids = [
        station_id for station_id in connected_station_ids
        if station_id in world.stations
    ]

    if danger >= 70:
        for station_id in connected_station_ids:
            effects.append(
                WorldEffect(
                    target_type="station",
                    target_id=station_id,
                    field_path=["pressure", "danger"],
                    operation="add",
                    value=1,
                    reason="dangerous_route_nearby",
                    source="route_system",
                    importance="debug",
                )
            )

    if condition <= 30:
        for station_id in connected_station_ids:
            effects.append(
                WorldEffect(
                    target_type="station",
                    target_id=station_id,
                    field_path=["pressure", "supply_disruption"],
                    operation="add",
                    value=1,
                    reason="damaged_route_nearby",
                    source="route_system",
                    importance="debug",
                )
            )

    if traffic >= 50 and danger >= 50:
        for station_id in connected_station_ids:
            effects.append(
                WorldEffect(
                    target_type="station",
                    target_id=station_id,
                    field_path=["pressure", "security_risk"],
                    operation="add",
                    value=1,
                    reason="unsafe_high_traffic_route",
                    source="route_system",
                    importance="debug",
                )
            )

    logs.append(
        create_world_log_entry(
            tick=world.current_tick,
            category="route_processed",
            message=f"Route processed: {route_id}",
            target_type="route",
            target_id=route_id,
            importance="debug",
            data={
                "danger": danger,
                "condition": condition,
                "traffic": traffic,
                "travel_time_ticks": travel_time_ticks,
                "connected_stations": connected_station_ids,
            },
        )
    )

    return effects, logs