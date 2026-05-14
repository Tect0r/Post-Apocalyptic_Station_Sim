from metro_sim.core.action_result import ActionResult
from metro_sim.core.game_session import GameSession
from metro_sim.player.actions.player_action_status import PlayerActionStatus


def cancel_player_action(
    session: GameSession,
    player_id: str,
    action_id: str,
) -> ActionResult:
    if player_id not in session.players:
        return ActionResult(
            success=False,
            message="player_not_found",
            data={"player_id": player_id},
        )

    player = session.players[player_id]

    action_to_cancel = None

    for action in player.active_actions:
        if action.id == action_id:
            action_to_cancel = action
            break

    if action_to_cancel is None:
        return ActionResult(
            success=False,
            message="active_action_not_found",
            data={"action_id": action_id},
        )

    action_to_cancel.status = PlayerActionStatus.CANCELLED

    player.active_actions = [
        action
        for action in player.active_actions
        if action.id != action_id
    ]

    player.completed_actions.append(action_to_cancel)

    return ActionResult(
        success=True,
        message="player_action_cancelled",
        data={
            "action_id": action_to_cancel.id,
            "action_type": action_to_cancel.action_type.value,
            "status": action_to_cancel.status.value,
        },
    )