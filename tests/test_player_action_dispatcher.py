from metro_sim.core.game_session import create_game_session
from metro_sim.player.actions.player_action import PlayerAction
from metro_sim.player.actions.player_action_dispatcher import dispatch_player_action
from metro_sim.player.actions.player_action_type import PlayerActionType


def test_dispatch_player_action_fails_for_unknown_player():
    session = create_game_session()

    result = dispatch_player_action(
        session,
        PlayerAction(
            type=PlayerActionType.START_EXPEDITION,
            player_id="missing_player",
        ),
    )

    assert result.success is False
    assert result.message == "player_not_found"


def test_dispatch_player_action_accepts_known_player_but_action_is_not_implemented():
    session = create_game_session()

    result = dispatch_player_action(
        session,
        PlayerAction(
            type=PlayerActionType.START_EXPEDITION,
            player_id="player_001",
        ),
    )

    assert result.success is False
    assert result.message == "action_not_implemented_yet"
    assert result.data["action_type"] == "start_expedition"