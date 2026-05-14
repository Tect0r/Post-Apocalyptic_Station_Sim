from metro_sim.core.game_session import advance_tick, create_game_session
from metro_sim.player.models.player_state import PlayerState
from metro_sim.world.models.world_state import WorldState
from metro_sim.player.actions.player_action_type import PlayerActionType
from metro_sim.player.actions.start_player_action_request import StartPlayerActionRequest
from metro_sim.player.services.player_action_service import start_player_action


def test_create_game_session_contains_world_and_player():
    session = create_game_session()

    assert isinstance(session.world, WorldState)
    assert isinstance(session.players["player_001"], PlayerState)


def test_create_game_session_player_does_not_control_station():
    session = create_game_session()

    station = session.world.stations["paveletskaya"]

    assert session.players["player_001"].id != station.id
    assert not hasattr(session.players["player_001"], "station")
    assert not hasattr(session.players["player_001"], "controlled_station")


def test_advance_tick_ticks_world_but_keeps_player_present():
    session = create_game_session()

    advance_tick(session)

    assert session.world.current_tick == 1
    assert session.players["player_001"].id == "player_001"
    assert session.last_report is not None

def test_create_game_session_contains_initial_player():
    session = create_game_session()

    assert "player_001" in session.players
    assert session.players["player_001"].crew.members == 6

def test_game_tick_completes_player_action_after_duration():
    session = create_game_session()
    player = session.players["player_001"]

    result = start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.SUPPORT_MILITIA,
            target_id="paveletskaya",
        ),
    )

    player = session.players["player_001"]
    action = player.active_actions[0]

    while session.world.current_tick < action.completes_at_tick:
        advance_tick(session)

    assert len(player.active_actions) == 0
    assert player.crew.fatigue >= 15
    assert session.world.stations["paveletskaya"].pressure["militia_support"] == 8