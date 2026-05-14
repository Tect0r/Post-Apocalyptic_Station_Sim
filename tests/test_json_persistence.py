from metro_sim.core.game_session import advance_tick, create_game_session
from metro_sim.persistence.load_game_service import load_game_session
from metro_sim.persistence.save_game_service import save_game_session
from metro_sim.player.actions.player_action_type import PlayerActionType
from metro_sim.player.actions.start_player_action_request import StartPlayerActionRequest
from metro_sim.player.services.player_action_service import start_player_action


def test_save_and_load_game_session_roundtrip():
    session = create_game_session()

    advance_tick(session)
    save_game_session(session, "test_roundtrip")

    loaded_session = load_game_session("test_roundtrip")

    assert loaded_session.world.current_tick == session.world.current_tick
    assert loaded_session.world.stations.keys() == session.world.stations.keys()
    assert loaded_session.world.routes.keys() == session.world.routes.keys()
    assert loaded_session.world.factions.keys() == session.world.factions.keys()
    assert loaded_session.players.keys() == session.players.keys()

def test_save_and_load_preserves_active_actions():
    session = create_game_session()

    result = start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.SUPPORT_MILITIA,
            target_id="paveletskaya",
        ),
    )

    assert result.success is True

    save_game_session(session, "test_active_action")
    loaded_session = load_game_session("test_active_action")

    loaded_player = loaded_session.players["player_001"]

    assert len(loaded_player.active_actions) == 1
    assert loaded_player.active_actions[0].action_type == PlayerActionType.SUPPORT_MILITIA
    assert loaded_player.active_actions[0].target_id == "paveletskaya"

def test_save_and_load_preserves_world_events():
    session = create_game_session()
    station = session.world.stations["paveletskaya"]
    station.pressure["militia_support"] = 25

    advance_tick(session)

    assert len(session.world.events) >= 1

    save_game_session(session, "test_events")
    loaded_session = load_game_session("test_events")

    assert len(loaded_session.world.events) == len(session.world.events)
    assert loaded_session.world.events[0].event_type == session.world.events[0].event_type

def test_save_and_load_preserves_player_assets():
    session = create_game_session()

    result = start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.RENT_STORAGE,
            target_id="paveletskaya",
        ),
    )

    for _ in range(result.data["duration_ticks"]):
        advance_tick(session)

    player = session.players["player_001"]
    assert len(player.assets) == 1

    save_game_session(session, "test_assets")
    loaded_session = load_game_session("test_assets")

    loaded_player = loaded_session.players["player_001"]

    assert len(loaded_player.assets) == 1
    assert loaded_player.assets[0].asset_type == "storage_room"
    assert loaded_player.assets[0].location_id == "paveletskaya"