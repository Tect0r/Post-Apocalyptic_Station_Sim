from metro_sim.core.action_result import ActionResult
from metro_sim.core.game_session import GameSession
from metro_sim.player.actions.forbidden_station_actions import FORBIDDEN_PLAYER_ACTION_TYPES
from metro_sim.player.actions.player_action import PlayerAction
from metro_sim.player.actions.player_action_type import PlayerActionType


def dispatch_player_action(
    session: GameSession,
    action: PlayerAction,
) -> ActionResult:
    if action.type.value in FORBIDDEN_PLAYER_ACTION_TYPES:
        return ActionResult(
            success=False,
            message="forbidden_direct_station_action",
            data={"action_type": action.type.value},
        )

    if action.player_id not in session.players:
        return ActionResult(
            success=False,
            message="player_not_found",
            data={"player_id": action.player_id},
        )

    if action.type == PlayerActionType.START_EXPEDITION:
        return ActionResult(
            success=False,
            message="action_not_implemented_yet",
            data={"action_type": action.type.value},
        )

    if action.type == PlayerActionType.SECURE_ROUTE:
        return ActionResult(
            success=False,
            message="action_not_implemented_yet",
            data={"action_type": action.type.value},
        )

    if action.type == PlayerActionType.RENT_STORAGE:
        return ActionResult(
            success=False,
            message="action_not_implemented_yet",
            data={"action_type": action.type.value},
        )

    if action.type == PlayerActionType.SUPPORT_REPAIR_TEAM:
        return ActionResult(
            success=False,
            message="action_not_implemented_yet",
            data={"action_type": action.type.value},
        )

    if action.type == PlayerActionType.FUND_MILITIA:
        return ActionResult(
            success=False,
            message="action_not_implemented_yet",
            data={"action_type": action.type.value},
        )

    return ActionResult(
        success=False,
        message="unknown_player_action",
        data={"action_type": action.type.value},
    )