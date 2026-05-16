from metro_sim.core.game_session import create_game_session
from metro_sim.player.actions.player_action_type import PlayerActionType
from metro_sim.player.actions.start_player_action_request import StartPlayerActionRequest
from metro_sim.player.services.player_action_service import start_player_action
from metro_sim.world.services.action_resolution_service import resolve_completed_player_actions


def test_completed_player_action_adds_station_pressure():
    session = create_game_session()
    station = session.world.stations["paveletskaya_radial"]

    start_result = start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.SUPPORT_MILITIA,
            target_id="paveletskaya_radial",
        ),
    )

    player = session.players["player_001"]
    action = player.active_actions[0]

    session.world.current_tick = action.completes_at_tick

    resolve_completed_player_actions(session.world, session.players)

    assert station.pressure["militia_support"] == 8