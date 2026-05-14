from metro_sim.utils.file_loader import load_world_data
from metro_sim.world.factories.faction_factory import create_faction_state
from metro_sim.world.factories.route_factory import create_route_state
from metro_sim.world.factories.station_factory import create_station_state
from metro_sim.world.models.world_state import WorldState
from metro_sim.contracts.factories.contract_factory import create_contract_state
from metro_sim.utils.file_loader import load_contracts_data


def create_world() -> WorldState:
    world_data = load_world_data()
    contracts_data = load_contracts_data()

    stations = {
        station_id: create_station_state(station_id, station_data)
        for station_id, station_data in world_data["stations"].items()
    }

    routes = {
        route_id: create_route_state(route_id, route_data)
        for route_id, route_data in world_data["routes"].items()
    }

    factions = {
        faction_id: create_faction_state(faction_id, faction_data)
        for faction_id, faction_data in world_data["factions"].items()
    }

    contracts = {
        contract_id: create_contract_state(
            contract_id=contract_id,
            contract_data=contract_data,
            created_tick=0,
        )
        for contract_id, contract_data in contracts_data.items()
    }

    return WorldState(
        current_tick=0,
        stations=stations,
        factions=factions,
        routes=routes,
        events=[],
        contracts=contracts
    )
