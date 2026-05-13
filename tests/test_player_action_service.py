from metro_sim.core.game_session import create_game_session
from metro_sim.player.actions.player_action_type import PlayerActionType
from metro_sim.player.actions.start_player_action_request import StartPlayerActionRequest
from metro_sim.player.services.player_action_service import start_player_action


def test_start_player_action_adds_active_action_to_player():
    session = create_game_session()

    result = start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.SUPPORT_MILITIA,
            target_id="paveletskaya",
        ),
    )

    player = session.players["player_001"]

    assert result.success is True
    assert result.message == "player_action_started"
    assert len(player.active_actions) == 1

    action = player.active_actions[0]

    assert action.action_type == PlayerActionType.SUPPORT_MILITIA
    assert action.target_type == "station"
    assert action.target_id == "paveletskaya"
    assert action.status == "active"

def test_start_player_action_pays_action_cost():
    session = create_game_session()
    player = session.players["player_001"]

    ammo_before = player.inventory.items["ammo"]
    food_before = player.inventory.items["food"]

    result = start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.SUPPORT_MILITIA,
            target_id="paveletskaya",
        ),
    )

    assert result.success is True
    assert player.inventory.items["ammo"] == ammo_before - 10
    assert player.inventory.items["food"] == food_before - 3

def test_start_player_action_fails_for_missing_player():
    session = create_game_session()

    result = start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="missing_player",
            action_type=PlayerActionType.SUPPORT_MILITIA,
            target_id="paveletskaya",
        ),
    )

    assert result.success is False
    assert result.message == "player_not_found"


def test_start_player_action_fails_for_missing_station_target():
    session = create_game_session()

    result = start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.SUPPORT_MILITIA,
            target_id="missing_station",
        ),
    )

    assert result.success is False
    assert result.message == "target_station_not_found"


def test_start_player_action_fails_when_resources_are_missing():
    session = create_game_session()
    player = session.players["player_001"]
    player.inventory.items["ammo"] = 0

    result = start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.SUPPORT_MILITIA,
            target_id="paveletskaya",
        ),
    )

    assert result.success is False
    assert result.message == "not_enough_resources"
    assert len(player.active_actions) == 0