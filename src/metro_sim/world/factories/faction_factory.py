from metro_sim.world.models.faction_state import FactionState


def create_faction_state(
    faction_id: str,
    faction_data: dict,
) -> FactionState:
    return FactionState(
        id=faction_id,
        name=faction_data["name"],
        resources=faction_data.get("resources", {}),
        relations=faction_data.get("relations", {}),
        controlled_stations=faction_data.get("controlled_stations", []),
    )