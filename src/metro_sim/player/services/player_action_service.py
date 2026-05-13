from uuid import uuid4

from metro_sim.core.action_result import ActionResult
from metro_sim.core.game_session import GameSession
from metro_sim.player.actions.player_action import PlayerAction
from metro_sim.player.actions.start_player_action_request import StartPlayerActionRequest
from metro_sim.player.services.inventory_service import can_afford, pay_cost
from metro_sim.utils.file_loader import load_player_actions_data


def start_player_action(
    session: GameSession,
    request: StartPlayerActionRequest,
) -> ActionResult:
    if request.player_id not in session.players:
        return ActionResult(
            success=False,
            message="player_not_found",
            data={"player_id": request.player_id},
        )

    action_definitions = load_player_actions_data()
    action_type = request.action_type.value

    if action_type not in action_definitions:
        return ActionResult(
            success=False,
            message="unknown_action_type",
            data={"action_type": action_type},
        )

    action_definition = action_definitions[action_type]
    player = session.players[request.player_id]

    target_type = action_definition["target_type"]
    target_id = request.target_id

    if target_type == "station" and target_id not in session.world.stations:
        return ActionResult(
            success=False,
            message="target_station_not_found",
            data={"target_id": target_id},
        )

    if target_type == "route" and target_id not in session.world.routes:
        return ActionResult(
            success=False,
            message="target_route_not_found",
            data={"target_id": target_id},
        )

    cost = action_definition.get("cost", {})

    if not can_afford(player.inventory, cost):
        return ActionResult(
            success=False,
            message="not_enough_resources",
            data={"cost": cost},
        )

    pay_cost(player.inventory, cost)

    action = PlayerAction(
        id=str(uuid4()),
        player_id=player.id,
        action_type=request.action_type,
        target_type=target_type,
        target_id=target_id,
        started_tick=session.world.current_tick,
        duration_ticks=action_definition["duration_ticks"],
        status="active",
        payload={
            "definition": action_definition,
        },
    )

    player.active_actions.append(action)

    return ActionResult(
        success=True,
        message="player_action_started",
        data={
            "action_id": action.id,
            "action_type": action.action_type.value,
            "target_type": action.target_type,
            "target_id": action.target_id,
            "started_tick": action.started_tick,
            "duration_ticks": action.duration_ticks,
            "completes_at_tick": action.completes_at_tick,
        },
    )