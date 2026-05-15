from metro_sim.core.action_result import ActionResult
from metro_sim.player.models.player_state import PlayerState
from metro_sim.player.models.crew_member_status import CrewMemberStatus


def validate_crew_member_assignment(
    player: PlayerState,
    crew_member_ids: list[str],
) -> ActionResult:
    known_members = {
        member.id: member
        for member in player.crew.crew_members
    }

    if not crew_member_ids:
        return ActionResult(
            success=False,
            message="no_crew_members_assigned",
        )

    for crew_member_id in crew_member_ids:
        if crew_member_id not in known_members:
            return ActionResult(
                success=False,
                message="crew_member_not_found",
                data={"crew_member_id": crew_member_id},
            )

        member = known_members[crew_member_id]

        if member.status != CrewMemberStatus.AVAILABLE:
            return ActionResult(
                success=False,
                message="crew_member_not_available",
                data={
                    "crew_member_id": crew_member_id,
                    "status": member.status.value,
                },
            )

        if member.current_location_id != player.crew.current_location_id:
            return ActionResult(
                success=False,
                message="crew_member_not_at_crew_location",
                data={
                    "crew_member_id": crew_member_id,
                    "member_location": member.current_location_id,
                    "crew_location": player.crew.current_location_id,
                },
            )

    return ActionResult(
        success=True,
        message="crew_assignment_valid",
    )


def mark_crew_members_assigned(
    player: PlayerState,
    crew_member_ids: list[str],
    action_id: str,
) -> None:
    for member in player.crew.crew_members:
        if member.id in crew_member_ids:
            member.status = CrewMemberStatus.ASSIGNED
            member.assigned_action_id = action_id


def release_crew_members_from_action(
    player: PlayerState,
    action_id: str,
) -> None:
    for member in player.crew.crew_members:
        if member.assigned_action_id == action_id:
            member.status = CrewMemberStatus.AVAILABLE
            member.assigned_action_id = None