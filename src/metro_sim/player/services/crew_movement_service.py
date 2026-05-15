from uuid import uuid4

from metro_sim.core.action_result import ActionResult
from metro_sim.core.game_session import GameSession
from metro_sim.player.actions.player_action import PlayerAction
from metro_sim.player.actions.player_action_status import PlayerActionStatus
from metro_sim.player.actions.player_action_type import PlayerActionType
from metro_sim.player.models.crew_member_status import CrewMemberStatus


def start_crew_movement(
    session: GameSession,
    player_id: str,
    route_id: str,
) -> ActionResult:
    if player_id not in session.players:
        return ActionResult(
            success=False,
            message="player_not_found",
            data={"player_id": player_id},
        )

    if route_id not in session.world.routes:
        return ActionResult(
            success=False,
            message="route_not_found",
            data={"route_id": route_id},
        )

    player = session.players[player_id]
    crew = player.crew
    route = session.world.routes[route_id]

    if crew.is_traveling:
        return ActionResult(
            success=False,
            message="crew_already_traveling",
            data={"player_id": player_id},
        )

    if route.status != "open":
        return ActionResult(
            success=False,
            message="route_not_open",
            data={"route_id": route_id},
        )

    if crew.current_location_id not in (route.from_station_id, route.to_station_id):
        return ActionResult(
            success=False,
            message="route_not_connected_to_current_location",
            data={
                "current_location_id": crew.current_location_id,
                "route_id": route_id,
            },
        )

    destination_id = (
        route.to_station_id
        if crew.current_location_id == route.from_station_id
        else route.from_station_id
    )

    action = PlayerAction(
        id=str(uuid4()),
        player_id=player.id,
        action_type=PlayerActionType.MOVE_CREW,
        target_type="route",
        target_id=route.id,
        started_tick=session.world.current_tick,
        duration_ticks=route.travel_time_ticks,
        status=PlayerActionStatus.ACTIVE,
        assigned_crew_member_ids=[
            member.id
            for member in crew.crew_members
            if member.current_location_id == crew.current_location_id
        ],
        payload={
            "movement": {
                "from_station_id": crew.current_location_id,
                "to_station_id": destination_id,
                "route_id": route.id,
            }
        },
    )

    player.active_actions.append(action)

    crew.is_traveling = True
    crew.destination_location_id = destination_id

    for member in crew.crew_members:
        if member.current_location_id == crew.current_location_id:
            member.status = CrewMemberStatus.TRAVELING
            member.assigned_action_id = action.id

    return ActionResult(
        success=True,
        message="crew_movement_started",
        data={
            "action_id": action.id,
            "route_id": route.id,
            "from_station_id": crew.current_location_id,
            "to_station_id": destination_id,
            "started_tick": action.started_tick,
            "duration_ticks": action.duration_ticks,
            "completes_at_tick": action.completes_at_tick,
        },
    )