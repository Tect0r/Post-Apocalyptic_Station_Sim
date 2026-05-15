from metro_sim.core.game_session import advance_tick, create_game_session
from metro_sim.player.actions.player_action_type import PlayerActionType
from metro_sim.player.services.crew_movement_service import start_crew_movement


def test_start_crew_movement_creates_movement_action():
    session = create_game_session()

    result = start_crew_movement(
        session=session,
        player_id="player_001",
        route_id="route_paveletskaya_hansa_ring",
    )

    player = session.players["player_001"]

    assert result.success is True
    assert result.message == "crew_movement_started"
    assert player.crew.is_traveling is True
    assert player.crew.destination_location_id == "hansa_ring"
    assert len(player.active_actions) == 1
    assert player.active_actions[0].action_type == PlayerActionType.MOVE_CREW


def test_crew_movement_completes_and_updates_location():
    session = create_game_session()

    start_crew_movement(
        session=session,
        player_id="player_001",
        route_id="route_paveletskaya_hansa_ring",
    )

    player = session.players["player_001"]
    action = player.active_actions[0]

    while session.world.current_tick < action.completes_at_tick:
        advance_tick(session)

    assert player.crew.current_location_id == "hansa_ring"
    assert player.crew.destination_location_id is None
    assert player.crew.is_traveling is False


def test_start_crew_movement_fails_if_route_not_connected():
    session = create_game_session()

    result = start_crew_movement(
        session=session,
        player_id="player_001",
        route_id="route_hansa_ring_polis",
    )

    assert result.success is False
    assert result.message == "route_not_connected_to_current_location"