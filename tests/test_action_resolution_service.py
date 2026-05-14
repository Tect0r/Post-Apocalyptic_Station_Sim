from metro_sim.core.game_session import create_game_session
from metro_sim.player.actions.player_action_type import PlayerActionType
from metro_sim.player.actions.start_player_action_request import StartPlayerActionRequest
from metro_sim.player.services.player_action_service import start_player_action
from metro_sim.world.services.action_resolution_service import resolve_completed_player_actions


def test_action_resolution_keeps_action_active_before_completion_tick():
    session = create_game_session()

    start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.SUPPORT_MILITIA,
            target_id="paveletskaya",
        ),
    )

    completed_actions = resolve_completed_player_actions(
        session.world,
        session.players,
    )

    player = session.players["player_001"]

    assert completed_actions == []
    assert len(player.active_actions) == 1
    assert player.active_actions[0].status == "active"

def test_action_resolution_completes_action_and_applies_effects():
    session = create_game_session()
    player = session.players["player_001"]
    station = session.world.stations["paveletskaya"]

    fatigue_before = player.crew.fatigue
    reputation_before = player.reputation.values["paveletskaya"]
    pressure_before = station.pressure.get("militia_support", 0)

    start_result = start_player_action(
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
    assert completed_actions[0].status == "completed"
    assert len(player.active_actions) == 0

    assert player.crew.fatigue == fatigue_before + 5
    assert player.reputation.values["paveletskaya"] == reputation_before + 3
    assert station.pressure["militia_support"] == pressure_before + 8