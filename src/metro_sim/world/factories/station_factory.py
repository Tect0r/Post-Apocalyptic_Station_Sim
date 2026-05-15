from metro_sim.world.models.station_state import StationState


def create_station_state(
    station_id: str,
    station_data: dict,
) -> StationState:
    return StationState(
        id=station_id,
        name=station_data["name"],
        station_type=station_data["type"],
        description_key=station_data["description_key"],
        resources=station_data.get("resources", {}),
        population=station_data.get("population", {}),
        stats=station_data.get("stats", {}),
        pressure=station_data.get("pressure", {}),
        faction_influence=station_data.get("faction_influence", {}),
        buildings=station_data.get("buildings", {}),
        market=station_data.get("market", {}),
    )