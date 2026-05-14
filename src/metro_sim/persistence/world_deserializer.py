from metro_sim.world.models.faction_state import FactionState
from metro_sim.world.models.route_state import RouteState
from metro_sim.world.models.world_event import WorldEvent
from metro_sim.world.models.station_state import StationState
from metro_sim.world.models.world_state import WorldState


def deserialize_world_state(data: dict) -> WorldState:
    stations = {
        station_id: StationState(**station_data)
        for station_id, station_data in data["stations"].items()
    }

    routes = {
        route_id: RouteState(**route_data)
        for route_id, route_data in data["routes"].items()
    }

    factions = {
        faction_id: FactionState(**faction_data)
        for faction_id, faction_data in data["factions"].items()
    }

    events = [
        WorldEvent(**event_data)
        for event_data in data.get("events", [])
    ]

    return WorldState(
        current_tick=data["current_tick"],
        stations=stations,
        factions=factions,
        routes=routes,
        events=events,
    )