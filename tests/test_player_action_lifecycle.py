from metro_sim.core.game_session import create_game_session
from metro_sim.player.actions.player_action_status import PlayerActionStatus
from metro_sim.player.actions.player_action_type import PlayerActionType
from metro_sim.player.actions.start_player_action_request import StartPlayerActionRequest
from metro_sim.player.services.player_action_service import start_player_action
from metro_sim.world.services.action_resolution_service import resolve_completed_player_actions


def test_completed_action_is_added_to_completed_history():
    session = create_game_session()

    start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.SUPPORT_MILITIA,
            target_id="paveletskaya",
        ),
    )

    player = session.players["player_001"]
    action = player.active_actions[0]

    session.world.current_tick = action.completes_at_tick

    completed_actions = resolve_completed_player_actions(
        session.world,
        session.players,
    )

    assert len(completed_actions) == 1
    assert len(player.active_actions) == 0
    assert len(player.completed_actions) == 1
    assert player.completed_actions[0].status == PlayerActionStatus.COMPLETED