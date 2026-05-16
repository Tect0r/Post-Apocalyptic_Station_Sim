from typing import Any

from metro_sim.player.actions.player_action import PlayerAction
from metro_sim.player.models.player_asset import PlayerAsset
from metro_sim.player.models.player_state import PlayerState
from metro_sim.player.actions.player_action_status import PlayerActionStatus
from metro_sim.world.models.world_state import WorldState
from metro_sim.contracts.models.contract_status import ContractStatus
from metro_sim.world.services.pressure_service import add_station_pressure
from metro_sim.player.services.crew_assignment_service import release_crew_members_from_action
from metro_sim.player.actions.player_action_type import PlayerActionType
from metro_sim.player.models.crew_member_status import CrewMemberStatus
from metro_sim.player.services.player_asset_service import add_player_asset_to_player


def resolve_completed_player_actions(
    world: WorldState,
    players: dict[str, PlayerState],
) -> list[PlayerAction]:
    completed_actions: list[PlayerAction] = []

    for player in players.values():
        still_active_actions: list[PlayerAction] = []

        for action in player.active_actions:
            if action.status != PlayerActionStatus.ACTIVE:
                still_active_actions.append(action)
                continue

            if world.current_tick < action.completes_at_tick:
                still_active_actions.append(action)
                continue

            apply_action_effects(world, player, action)
            apply_movement_completion(player, action)
            update_linked_contract_on_completion(world, action)

            action.status = PlayerActionStatus.COMPLETED
            completed_actions.append(action)
            player.completed_actions.append(action)
            release_crew_members_from_action(player, action.id)

        player.active_actions = still_active_actions

    return completed_actions


def apply_action_effects(
    world: WorldState,
    player: PlayerState,
    action: PlayerAction,
) -> None:
    definition = action.payload.get("definition", {})
    effects = definition.get("effects", {})
    reward = definition.get("reward", {})

    apply_crew_effects(player, effects.get("crew", {}))
    apply_player_reputation_effects(player, action, effects.get("player_reputation", {}))
    apply_station_pressure_effects(world, action, effects.get("station_pressure", {}))
    apply_route_pressure_effects(world, action, effects.get("route_pressure", {}))
    apply_inventory_effects(player, effects.get("inventory", {}))
    apply_inventory_effects(player, reward)
    apply_player_asset_effects(world, player, action, effects.get("player_asset", {}))


def apply_crew_effects(player: PlayerState, crew_effects: dict[str, int]) -> None:
    for key, delta in crew_effects.items():
        if hasattr(player.crew, key):
            current_value = getattr(player.crew, key)
            setattr(player.crew, key, current_value + delta)


def apply_player_reputation_effects(
    player: PlayerState,
    action: PlayerAction,
    reputation_effects: dict[str, int],
) -> None:
    for target, delta in reputation_effects.items():
        reputation_key = action.target_id if target == "station" else target
        current_value = player.reputation.values.get(reputation_key, 0)
        player.reputation.values[reputation_key] = current_value + delta


def apply_station_pressure_effects(
    world: WorldState,
    action: PlayerAction,
    pressure_effects: dict[str, int],
) -> None:
    if action.target_type != "station":
        return

    if action.target_id not in world.stations:
        return

    station = world.stations[action.target_id]

    for pressure_key, delta in pressure_effects.items():
        add_station_pressure(station, pressure_key, delta)


def apply_route_pressure_effects(
    world: WorldState,
    action: PlayerAction,
    route_pressure_effects: dict[str, int],
) -> None:
    if action.target_type != "route":
        return

    if not action.target_id:
        return

    route = world.routes.get(action.target_id)

    if route is None:
        return

    pressure = get_or_create_route_pressure(route)

    for pressure_key, delta in route_pressure_effects.items():
        if not isinstance(pressure_key, str) or not pressure_key:
            continue

        if not isinstance(delta, int | float):
            continue

        current_value = pressure.get(pressure_key, 0)

        if not isinstance(current_value, int | float):
            current_value = 0

        pressure[pressure_key] = clamp_pressure_value(current_value + delta)


def get_or_create_route_pressure(route: Any) -> dict[str, int]:
    if isinstance(route, dict):
        pressure = route.get("pressure")

        if not isinstance(pressure, dict):
            pressure = {}
            route["pressure"] = pressure

        return pressure

    pressure = getattr(route, "pressure", None)

    if not isinstance(pressure, dict):
        pressure = {}
        setattr(route, "pressure", pressure)

    return pressure


def clamp_pressure_value(value: int | float) -> int:
    return int(max(0, min(100, value)))


def apply_inventory_effects(player: PlayerState, inventory_effects: dict[str, int]) -> None:
    for item_id, delta in inventory_effects.items():
        current_value = player.inventory.items.get(item_id, 0)
        player.inventory.items[item_id] = current_value + delta


def apply_player_asset_effects(
    world: WorldState,
    player: PlayerState,
    action: PlayerAction,
    asset_effects: dict,
) -> None:
    if not asset_effects:
        return

    asset_type = asset_effects["asset_type"]

    station_id = action.target_id if action.target_type == "station" else None
    route_id = action.target_id if action.target_type == "route" else None

    add_player_asset_to_player(
        world=world,
        player=player,
        asset_type=asset_type,
        station_id=station_id,
        route_id=route_id,
        metadata={
            "created_by_action": action.action_type.value,
        },
    )

def update_linked_contract_on_completion(world: WorldState, action: PlayerAction) -> None:
    contract_id = action.payload.get("contract_id")

    if contract_id is None:
        return

    if contract_id not in world.contracts:
        return

    contract = world.contracts[contract_id]
    contract.status = ContractStatus.COMPLETED
    contract.completed_tick = world.current_tick

def apply_movement_completion(player: PlayerState, action: PlayerAction) -> None:
    if action.action_type != PlayerActionType.MOVE_CREW:
        return

    movement = action.payload.get("movement", {})
    destination_id = movement.get("to_station_id")

    if destination_id is None:
        return

    player.crew.current_location_id = destination_id
    player.crew.destination_location_id = None
    player.crew.is_traveling = False

    for member in player.crew.crew_members:
        if member.id in action.assigned_crew_member_ids:
            member.current_location_id = destination_id
            member.status = CrewMemberStatus.AVAILABLE
            member.assigned_action_id = None

def apply_player_asset_effects(
    world: WorldState,
    player: PlayerState,
    action: PlayerAction,
    asset_effects: dict,
) -> None:
    if not asset_effects:
        return

    asset_type = asset_effects["asset_type"]

    station_id = action.target_id if action.target_type == "station" else None
    route_id = action.target_id if action.target_type == "route" else None

    add_player_asset_to_player(
        world=world,
        player=player,
        asset_type=asset_type,
        station_id=station_id,
        route_id=route_id,
        metadata={
            "created_by_action": action.action_type.value,
        },
    )