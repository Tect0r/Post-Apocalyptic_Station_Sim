from metro_sim.world.models.faction_state import FactionState
from metro_sim.world.models.route_state import RouteState
from metro_sim.world.models.world_event import WorldEvent
from metro_sim.world.models.station_state import StationState
from metro_sim.world.models.world_state import WorldState
from metro_sim.contracts.models.contract_state import ContractState
from metro_sim.contracts.models.contract_status import ContractStatus
from metro_sim.pvp.models.pvp_impact import PvPImpact
from metro_sim.pvp.models.pvp_action_type import PvPActionType


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

    contracts = {
        contract_id: deserialize_contract_state(contract_data)
        for contract_id, contract_data in data.get("contracts", {}).items()
    }

    pvp_impacts = [
        deserialize_pvp_impact(impact_data)
        for impact_data in data.get("pvp_impacts", [])
    ]

    return WorldState(
        current_tick=data["current_tick"],
        stations=stations,
        factions=factions,
        routes=routes,
        events=events,
        contracts=contracts,
        pvp_impacts=pvp_impacts
    )

def deserialize_pvp_impact(data: dict) -> PvPImpact:
    return PvPImpact(
        id=data["id"],
        source_player_id=data["source_player_id"],
        target_player_id=data.get("target_player_id"),
        action_type=PvPActionType(data["action_type"]),
        target_type=data["target_type"],
        target_id=data["target_id"],
        created_tick=data["created_tick"],
        effects=data.get("effects", {}),
        detected=data.get("detected", False),
        reputation_cost=data.get("reputation_cost", {}),
    )

def deserialize_contract_state(contract_data: dict) -> ContractState:
    return ContractState(
        id=contract_data["id"],
        title=contract_data["title"],
        description_key=contract_data["description_key"],
        issuer_type=contract_data["issuer_type"],
        issuer_id=contract_data["issuer_id"],
        target_type=contract_data["target_type"],
        target_id=contract_data["target_id"],
        action_type=contract_data["action_type"],
        duration_ticks=contract_data["duration_ticks"],
        cost=contract_data.get("cost", {}),
        reward=contract_data.get("reward", {}),
        effects=contract_data.get("effects", {}),
        status=ContractStatus(contract_data.get("status", "available")),
        accepted_by_player_id=contract_data.get("accepted_by_player_id"),
        linked_action_id=contract_data.get("linked_action_id"),
        created_tick=contract_data.get("created_tick", 0),
        accepted_tick=contract_data.get("accepted_tick"),
        completed_tick=contract_data.get("completed_tick"),
    )