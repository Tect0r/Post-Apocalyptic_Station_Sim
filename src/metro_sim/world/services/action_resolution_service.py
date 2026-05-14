from uuid import uuid4

from metro_sim.player.actions.player_action import PlayerAction
from metro_sim.player.models.player_asset import PlayerAsset
from metro_sim.player.models.player_state import PlayerState
from metro_sim.player.actions.player_action_status import PlayerActionStatus
from metro_sim.world.models.world_state import WorldState
from metro_sim.contracts.models.contract_status import ContractStatus
from metro_sim.world.services.pressure_service import add_station_pressure


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
            action.status = PlayerActionStatus.COMPLETED
            completed_actions.append(action)
            player.completed_actions.append(action)

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
    apply_player_asset_effects(player, action, effects.get("player_asset", {}))
    apply_inventory_effects(player, reward)


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

    if action.target_id not in world.routes:
        return

    route = world.routes[action.target_id]
    pressure = route.modifiers.setdefault("pressure", {})

    for pressure_key, delta in route_pressure_effects.items():
        current_value = pressure.get(pressure_key, 0)
        pressure[pressure_key] = max(0, min(100, current_value + delta))


def apply_inventory_effects(player: PlayerState, inventory_effects: dict[str, int]) -> None:
    for item_id, delta in inventory_effects.items():
        current_value = player.inventory.items.get(item_id, 0)
        player.inventory.items[item_id] = current_value + delta


def apply_player_asset_effects(
    player: PlayerState,
    action: PlayerAction,
    asset_effects: dict,
) -> None:
    if not asset_effects:
        return

    asset = PlayerAsset(
        id=str(uuid4()),
        name=asset_effects.get("name", asset_effects["asset_type"]),
        asset_type=asset_effects["asset_type"],
        location_id=action.target_id,
        condition=asset_effects.get("condition", 100),
        metadata={
            "created_by_action": action.action_type.value,
        },
    )

    player.assets.append(asset)