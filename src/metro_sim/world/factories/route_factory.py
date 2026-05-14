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
        danger_level=route_data["danger_level"],
        status=route_data.get("status", "open"),
        modifiers=route_data.get("modifiers", {}),
    )