from metro_sim.player.actions.player_action_status import PlayerActionStatus
from metro_sim.player.actions.player_action_type import PlayerActionType
from metro_sim.player.actions.start_player_action_request import StartPlayerActionRequest
from metro_sim.player.models.crew_member_status import CrewMemberStatus
from metro_sim.core.game_session import create_game_session
from metro_sim.player.services.player_action_service import start_player_action
from metro_sim.core.game_session import advance_tick


def test_start_action_can_assign_crew_members():
    session = create_game_session()
    player = session.players["player_001"]

    result = start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.SUPPORT_MILITIA,
            target_id="paveletskaya",
            assigned_crew_member_ids=["crew_001", "crew_002"],
        ),
    )

    assert result.success is True

    action = player.active_actions[0]

    assert action.assigned_crew_member_ids == ["crew_001", "crew_002"]

    assigned_members = [
        member
        for member in player.crew.crew_members
        if member.id in action.assigned_crew_member_ids
    ]

    assert all(member.status == CrewMemberStatus.ASSIGNED for member in assigned_members)
    assert all(member.assigned_action_id == action.id for member in assigned_members)


def test_start_action_fails_for_busy_crew_member():
    session = create_game_session()

    start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.SUPPORT_MILITIA,
            target_id="paveletskaya",
            assigned_crew_member_ids=["crew_001"],
        ),
    )

    result = start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.REPAIR_WATER_FILTER,
            target_id="paveletskaya",
            assigned_crew_member_ids=["crew_001"],
        ),
    )

    assert result.success is False
    assert result.message == "crew_member_not_available"

def test_assigned_crew_members_are_released_after_action_completion():
    session = create_game_session()
    player = session.players["player_001"]

    start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.SUPPORT_MILITIA,
            target_id="paveletskaya",
            assigned_crew_member_ids=["crew_001"],
        ),
    )

    action = player.active_actions[0]

    while session.world.current_tick < action.completes_at_tick:
        advance_tick(session)

    member = player.crew.crew_members[0]

    assert member.status == CrewMemberStatus.AVAILABLE
    assert member.assigned_action_id is None