from metro_sim.world.models.route_state import RouteState


def create_route_state(
    route_id: str,
    route_data: dict,
) -> RouteState:
    return RouteState(
        id=route_id,
        from_station_id=route_data["from_station_id"],
        to_station_id=route_data["to_station_id"],
        distance=route_data["distance"],
        danger=route_data["danger"],
        status=route_data.get("status", "open"),
        travel_time_ticks=route_data["travel_time_ticks"],
        control=route_data.get("control", {}),
        modifiers=route_data.get("modifiers", {}),
    )