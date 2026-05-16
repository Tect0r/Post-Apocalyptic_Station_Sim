from metro_sim.core.game_session import advance_tick, create_game_session
from metro_sim.player.actions.player_action_type import PlayerActionType
from metro_sim.player.services.crew_movement_service import start_crew_movement
from metro_sim.player.models.crew_member_status import CrewMemberStatus


def test_start_crew_movement_creates_movement_action():
    session = create_game_session()

    result = start_crew_movement(
        session=session,
        player_id="player_001",
        route_id="route_paveletskaya_ring_radial",
    )

    player = session.players["player_001"]

    assert result.success is True
    assert result.message == "crew_movement_started"
    assert player.crew.is_traveling is True
    assert player.crew.destination_location_id == "paveletskaya_ring"
    assert len(player.active_actions) == 1
    assert player.active_actions[0].action_type == PlayerActionType.MOVE_CREW


def test_crew_movement_completes_and_updates_location():
    session = create_game_session()

    start_crew_movement(
        session=session,
        player_id="player_001",
        route_id="route_paveletskaya_ring_radial",
    )

    player = session.players["player_001"]
    action = player.active_actions[0]

    while session.world.current_tick < action.completes_at_tick:
        advance_tick(session)

    assert player.crew.current_location_id == "paveletskaya_ring"
    assert player.crew.destination_location_id is None
    assert player.crew.is_traveling is False


def test_start_crew_movement_succeeds_for_connected_route():
    session = create_game_session()

    result = start_crew_movement(
        session=session,
        player_id="player_001",
        route_id="route_paveletskaya_ring_radial",
    )

    assert result.success is True
    assert result.message == "crew_movement_started"
    assert result.data["route_id"] == "route_paveletskaya_ring_radial"

def test_start_crew_movement_fails_if_route_not_found():
    session = create_game_session()

    result = start_crew_movement(
        session=session,
        player_id="player_001",
        route_id="unknown_route",
    )

    assert result.success is False
    assert result.message == "route_not_found"

def test_crew_members_travel_with_crew_movement():
    session = create_game_session()

    start_crew_movement(
        session=session,
        player_id="player_001",
        route_id="route_paveletskaya_ring_radial",
    )

    player = session.players["player_001"]

    assert all(
        member.status == CrewMemberStatus.TRAVELING
        for member in player.crew.crew_members
    )

    action = player.active_actions[0]

    while session.world.current_tick < action.completes_at_tick:
        advance_tick(session)

    assert all(
        member.current_location_id == "paveletskaya_ring"
        for member in player.crew.crew_members
    )

    assert all(
        member.status == CrewMemberStatus.AVAILABLE
        for member in player.crew.crew_members
    )