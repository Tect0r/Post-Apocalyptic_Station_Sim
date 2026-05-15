from uuid import uuid4

from metro_sim.contracts.models.contract_status import ContractStatus
from metro_sim.core.action_result import ActionResult
from metro_sim.core.game_session import GameSession
from metro_sim.player.actions.player_action import PlayerAction
from metro_sim.player.actions.player_action_status import PlayerActionStatus
from metro_sim.player.actions.player_action_type import PlayerActionType
from metro_sim.player.services.inventory_service import can_afford, pay_cost


def accept_contract(
    session: GameSession,
    player_id: str,
    contract_id: str,
) -> ActionResult:
    if player_id not in session.players:
        return ActionResult(
            success=False,
            message="player_not_found",
            data={"player_id": player_id},
        )

    if contract_id not in session.world.contracts:
        return ActionResult(
            success=False,
            message="contract_not_found",
            data={"contract_id": contract_id},
        )

    player = session.players[player_id]
    contract = session.world.contracts[contract_id]

    if contract.status != ContractStatus.AVAILABLE:
        return ActionResult(
            success=False,
            message="contract_not_available",
            data={
                "contract_id": contract_id,
                "status": contract.status.value,
            },
        )

    if player.crew.is_traveling:
        return ActionResult(
            success=False,
            message="crew_is_traveling",
            data={"player_id": player_id},
        )
    
    if contract.target_type == "station":
        if player.crew.current_location_id != contract.target_id:
            return ActionResult(
                success=False,
                message="crew_not_at_target_station",
                data={
                    "current_location_id": player.crew.current_location_id,
                    "target_id": contract.target_id,
                },
            )

    if contract.target_type == "route":
        route = session.world.routes.get(contract.target_id)

        if route is None:
            return ActionResult(
                success=False,
                message="route_not_found",
                data={"route_id": contract.target_id},
            )

        if player.crew.current_location_id not in (route.from_station_id, route.to_station_id):
            return ActionResult(
                success=False,
                message="route_not_connected_to_current_location",
                data={
                    "current_location_id": player.crew.current_location_id,
                    "route_id": route.id,
                },
            )

    if not can_afford(player.inventory, contract.cost):
        return ActionResult(
            success=False,
            message="not_enough_resources",
            data={"cost": contract.cost},
        )

    pay_cost(player.inventory, contract.cost)

    action = PlayerAction(
        id=str(uuid4()),
        player_id=player.id,
        action_type=PlayerActionType(contract.action_type),
        target_type=contract.target_type,
        target_id=contract.target_id,
        started_tick=session.world.current_tick,
        duration_ticks=contract.duration_ticks,
        status=PlayerActionStatus.ACTIVE,
        payload={
            "contract_id": contract.id,
            "definition": {
                "effects": contract.effects,
                "reward": contract.reward,
            },
        },
    )

    player.active_actions.append(action)

    contract.status = ContractStatus.ACCEPTED
    contract.accepted_by_player_id = player.id
    contract.linked_action_id = action.id
    contract.accepted_tick = session.world.current_tick

    return ActionResult(
        success=True,
        message="contract_accepted",
        data={
            "contract_id": contract.id,
            "action_id": action.id,
            "action_type": action.action_type.value,
            "target_type": action.target_type,
            "target_id": action.target_id,
            "started_tick": action.started_tick,
            "duration_ticks": action.duration_ticks,
            "completes_at_tick": action.completes_at_tick,
        },
    )