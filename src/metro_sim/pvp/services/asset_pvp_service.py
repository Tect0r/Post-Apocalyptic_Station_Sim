from metro_sim.core.action_result import ActionResult
from metro_sim.core.game_session import GameSession
from metro_sim.player.services.player_asset_service import damage_player_asset
from metro_sim.pvp.models.pvp_action_type import PvPActionType
from metro_sim.pvp.services.pvp_cooldown_service import is_pvp_action_on_cooldown
from metro_sim.pvp.services.pvp_detection_service import roll_detection
from metro_sim.pvp.services.pvp_impact_service import add_pvp_impact
from metro_sim.utils.file_loader import load_pvp_rules_data


def damage_player_asset_indirectly(
    session: GameSession,
    source_player_id: str,
    target_player_id: str,
    asset_id: str,
    amount: int,
) -> ActionResult:
    if source_player_id not in session.players:
        return ActionResult(False, "source_player_not_found", {"player_id": source_player_id})

    if target_player_id not in session.players:
        return ActionResult(False, "target_player_not_found", {"player_id": target_player_id})

    if source_player_id == target_player_id:
        return ActionResult(False, "cannot_target_self", {"player_id": source_player_id})

    rules = load_pvp_rules_data()["damage_asset"]
    max_damage = rules["max_condition_damage"]
    cooldown_ticks = rules["cooldown_ticks"]

    amount = max(1, min(max_damage, amount))

    if is_pvp_action_on_cooldown(
        world=session.world,
        source_player_id=source_player_id,
        action_type=PvPActionType.DAMAGE_ASSET,
        target_type="asset",
        target_id=asset_id,
        cooldown_ticks=cooldown_ticks,
    ):
        return ActionResult(False, "pvp_action_on_cooldown", {"asset_id": asset_id})

    result = damage_player_asset(
        session=session,
        player_id=target_player_id,
        asset_id=asset_id,
        amount=amount,
    )

    if not result.success:
        return result

    detected = roll_detection(rules.get("detection_chance", 0))

    impact = add_pvp_impact(
        world=session.world,
        source_player_id=source_player_id,
        target_player_id=target_player_id,
        action_type=PvPActionType.DAMAGE_ASSET,
        target_type="asset",
        target_id=asset_id,
        effects={
            "asset_condition_damage": amount
        },
        detected=detected,
        reputation_cost=rules.get("reputation_cost", {}),
    )

    return ActionResult(
        True,
        "player_asset_damaged_indirectly",
        {
            "impact_id": impact.id,
            "target_player_id": target_player_id,
            "asset_id": asset_id,
            "amount": amount,
            "detected": detected,
        },
    )