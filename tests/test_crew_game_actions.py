from metro_sim.core.game_session import advance_tick, create_game_session
from metro_sim.player.actions.player_action_type import PlayerActionType
from metro_sim.player.actions.start_player_action_request import StartPlayerActionRequest
from metro_sim.player.services.player_action_service import start_player_action


def complete_action(session, duration_ticks: int) -> None:
    for _ in range(duration_ticks):
        advance_tick(session)


def test_player_can_complete_station_action():
    session = create_game_session()
    player = session.players["player_001"]

    result = start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.SUPPORT_MILITIA,
            target_id="paveletskaya_radial",
        ),
    )

    assert result.success is True

    action = player.active_actions[0]
    complete_action(session, action.duration_ticks)

    assert len(player.active_actions) == 0
    assert player.crew.fatigue > 10
    assert session.world.stations["paveletskaya_radial"].pressure["militia_support"] > 0


def test_player_can_complete_route_action():
    session = create_game_session()
    player = session.players["player_001"]

    result = start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.SECURE_ROUTE,
            target_id="route_paveletskaya_ring_radial",
        ),
    )

    assert result.success is True

    action = player.active_actions[0]
    complete_action(session, action.duration_ticks)

    route = session.world.routes["route_paveletskaya_ring_radial"]

    assert len(player.active_actions) == 0
    assert route.pressure["security"] > 0


def test_player_can_gain_asset_from_action():
    session = create_game_session()
    player = session.players["player_001"]

    result = start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.RENT_STORAGE,
            target_id="paveletskaya_radial",
        ),
    )

    assert result.success is True

    action = player.active_actions[0]
    complete_action(session, action.duration_ticks)

    assert len(player.assets) == 1
    assert player.assets[0].asset_type == "storage_room"
    assert player.assets[0].station_id == "paveletskaya_radial"


def test_player_can_gain_inventory_from_action():
    session = create_game_session()
    player = session.players["player_001"]

    parts_before = player.inventory.items["parts"]

    result = start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.START_STALKER_EXPEDITION,
            target_id="paveletskaya_radial",
        ),
    )

    assert result.success is True

    action = player.active_actions[0]
    complete_action(session, action.duration_ticks)

    assert player.inventory.items["parts"] > parts_before