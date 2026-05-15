from metro_sim.core.action_result import ActionResult
from metro_sim.player.factories.player_asset_factory import create_player_asset
from metro_sim.player.models.player_asset_status import PlayerAssetStatus
from metro_sim.player.services.inventory_service import can_afford, pay_cost
from metro_sim.utils.file_loader import load_player_assets_data

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from metro_sim.core.game_session import GameSession

def get_player_asset_by_id(session: "GameSession", player_id: str, asset_id: str):
    if player_id not in session.players:
        return None

    player = session.players[player_id]

    for asset in player.assets:
        if asset.id == asset_id:
            return asset

    return None


def add_player_asset(
    session: "GameSession",
    player_id: str,
    asset_type: str,
    station_id: str | None = None,
    route_id: str | None = None,
    metadata: dict | None = None,
) -> ActionResult:
    if player_id not in session.players:
        return ActionResult(False, "player_not_found", {"player_id": player_id})

    player = session.players[player_id]

    return add_player_asset_to_player(
        world=session.world,
        player=player,
        asset_type=asset_type,
        station_id=station_id,
        route_id=route_id,
        metadata=metadata,
    )


def upgrade_player_asset(
    session: "GameSession",
    player_id: str,
    asset_id: str,
) -> ActionResult:
    if player_id not in session.players:
        return ActionResult(False, "player_not_found", {"player_id": player_id})

    player = session.players[player_id]
    asset = get_player_asset_by_id(session, player_id, asset_id)

    if asset is None:
        return ActionResult(False, "asset_not_found", {"asset_id": asset_id})

    if asset.status == PlayerAssetStatus.LOST:
        return ActionResult(False, "asset_lost", {"asset_id": asset_id})

    asset_definitions = load_player_assets_data()
    asset_definition = asset_definitions[asset.asset_type]

    max_level = asset_definition["max_level"]
    next_level = asset.level + 1

    if next_level > max_level:
        return ActionResult(False, "asset_max_level_reached", {"asset_id": asset_id})

    upgrade_cost = asset_definition.get("upgrade_cost_by_level", {}).get(str(next_level), {})

    if not can_afford(player.inventory, upgrade_cost):
        return ActionResult(False, "not_enough_resources", {"cost": upgrade_cost})

    pay_cost(player.inventory, upgrade_cost)

    asset.level = next_level
    asset.effects = asset_definition.get("effects_by_level", {}).get(str(next_level), asset.effects)

    return ActionResult(
        True,
        "player_asset_upgraded",
        {
            "asset_id": asset.id,
            "level": asset.level,
            "effects": asset.effects,
        },
    )


def damage_player_asset(
    session: "GameSession",
    player_id: str,
    asset_id: str,
    amount: int,
) -> ActionResult:
    asset = get_player_asset_by_id(session, player_id, asset_id)

    if asset is None:
        return ActionResult(False, "asset_not_found", {"asset_id": asset_id})

    asset.condition = max(0, asset.condition - amount)

    if asset.condition == 0:
        asset.status = PlayerAssetStatus.DISABLED
    elif asset.condition < 50:
        asset.status = PlayerAssetStatus.DAMAGED

    return ActionResult(
        True,
        "player_asset_damaged",
        {
            "asset_id": asset.id,
            "condition": asset.condition,
            "status": asset.status.value,
        },
    )


def repair_player_asset(
    session: "GameSession",
    player_id: str,
    asset_id: str,
) -> ActionResult:
    if player_id not in session.players:
        return ActionResult(False, "player_not_found", {"player_id": player_id})

    player = session.players[player_id]
    asset = get_player_asset_by_id(session, player_id, asset_id)

    if asset is None:
        return ActionResult(False, "asset_not_found", {"asset_id": asset_id})

    if asset.condition >= 100:
        return ActionResult(False, "asset_condition_full", {"asset_id": asset_id})

    asset_definitions = load_player_assets_data()
    asset_definition = asset_definitions[asset.asset_type]
    repair_cost = asset_definition.get("repair_cost_per_10_condition", {})

    if not can_afford(player.inventory, repair_cost):
        return ActionResult(False, "not_enough_resources", {"cost": repair_cost})

    pay_cost(player.inventory, repair_cost)

    asset.condition = min(100, asset.condition + 10)

    if asset.condition >= 50:
        asset.status = PlayerAssetStatus.ACTIVE
    elif asset.condition > 0:
        asset.status = PlayerAssetStatus.DAMAGED

    return ActionResult(
        True,
        "player_asset_repaired",
        {
            "asset_id": asset.id,
            "condition": asset.condition,
            "status": asset.status.value,
        },
    )

def add_player_asset_to_player(
    world,
    player,
    asset_type: str,
    station_id: str | None = None,
    route_id: str | None = None,
    metadata: dict | None = None,
) -> ActionResult:
    asset_definitions = load_player_assets_data()

    if asset_type not in asset_definitions:
        return ActionResult(False, "unknown_asset_type", {"asset_type": asset_type})

    asset_definition = asset_definitions[asset_type]
    target_type = asset_definition["target_type"]

    if target_type == "station":
        if station_id is None or station_id not in world.stations:
            return ActionResult(False, "target_station_not_found", {"station_id": station_id})

    if target_type == "route":
        if route_id is None or route_id not in world.routes:
            return ActionResult(False, "target_route_not_found", {"route_id": route_id})

    asset = create_player_asset(
        owner_player_id=player.id,
        asset_type=asset_type,
        asset_definition=asset_definition,
        station_id=station_id,
        route_id=route_id,
        metadata=metadata,
    )

    player.assets.append(asset)

    return ActionResult(
        True,
        "player_asset_added",
        {
            "asset_id": asset.id,
            "asset_type": asset.asset_type,
            "station_id": asset.station_id,
            "route_id": asset.route_id,
            "level": asset.level,
            "condition": asset.condition,
        },
    )