from metro_sim.core.game_session import create_game_session
from metro_sim.player.actions.player_action_status import PlayerActionStatus
from metro_sim.player.actions.player_action_type import PlayerActionType
from metro_sim.player.actions.start_player_action_request import StartPlayerActionRequest
from metro_sim.player.services.player_action_cancel_service import cancel_player_action
from metro_sim.player.services.player_action_service import start_player_action


def test_cancel_player_action_moves_action_to_completed_history():
    session = create_game_session()

    start_result = start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.SUPPORT_MILITIA,
            target_id="paveletskaya_radial",
        ),
    )

    action_id = start_result.data["action_id"]

    result = cancel_player_action(
        session=session,
        player_id="player_001",
        action_id=action_id,
    )

    player = session.players["player_001"]

    assert result.success is True
    assert result.message == "player_action_cancelled"
    assert len(player.active_actions) == 0
    assert len(player.completed_actions) == 1
    assert player.completed_actions[0].status == PlayerActionStatus.CANCELLED


def test_cancel_player_action_fails_for_unknown_action():
    session = create_game_session()

    result = cancel_player_action(
        session=session,
        player_id="player_001",
        action_id="missing_action",
    )

    assert result.success is False
    assert result.message == "active_action_not_found"