from dataclasses import dataclass

from metro_sim.world.models.npc_trader import NpcTrader
from metro_sim.world.models.world_log_entry import WorldLogEntry, create_world_log_entry
from metro_sim.world.models.world_state import WorldState
from metro_sim.world.simulation.movement_system import start_world_movement
from metro_sim.world.simulation.trader_decision_service import (
    TraderTargetEvaluation,
    evaluate_trader_target,
    evaluation_to_dict,
)

@dataclass
class TraderTargetChoice:
    selected_station_id: str | None
    evaluations: list[TraderTargetEvaluation]

def process_npc_traders_tick(world: WorldState) -> list[WorldLogEntry]:
    logs: list[WorldLogEntry] = []

    for trader_id, trader in world.npc_traders.items():
        trader_logs = process_single_trader_tick(
            world=world,
            trader_id=trader_id,
            trader=trader,
        )

        logs.extend(trader_logs)

    return logs


def process_single_trader_tick(
    *,
    world: WorldState,
    trader_id: str,
    trader: NpcTrader,
) -> list[WorldLogEntry]:
    logs: list[WorldLogEntry] = []

    if trader.status == "resting":
        return process_resting_trader_tick(
            world=world,
            trader_id=trader_id,
            trader=trader,
        )

    if trader.status != "idle":
        return logs

    target_choice = choose_trader_target_station(
        world=world,
        trader=trader,
    )

    target_station_id = target_choice.selected_station_id

    trader.data["last_target_choice"] = {
        "selected_station_id": target_station_id,
        "evaluations": [
            evaluation_to_dict(evaluation)
            for evaluation in target_choice.evaluations
        ],
    }

    logs.append(
        create_world_log_entry(
            tick=world.current_tick,
            category="npc_trader_target_evaluated",
            message=f"Trader {trader.name} evaluated trade targets.",
            target_type="npc_trader",
            target_id=trader_id,
            importance="debug",
            data={
                "current_station_id": trader.current_station_id,
                "selected_station_id": target_station_id,
                "evaluations": [
                    evaluation_to_dict(evaluation)
                    for evaluation in target_choice.evaluations
                ],
            },
        )
    )

    if target_station_id is None:
        return logs

    if target_station_id == trader.current_station_id:
        return logs

    movement_result = start_world_movement(
        world=world,
        actor_type="npc_trader",
        actor_id=trader_id,
        from_station_id=trader.current_station_id,
        to_station_id=target_station_id,
    )

    if not movement_result.success or movement_result.movement is None:
        logs.append(
            create_world_log_entry(
                tick=world.current_tick,
                category="npc_trader_movement_failed",
                message=f"Trader {trader.name} could not find a path to {target_station_id}.",
                target_type="npc_trader",
                target_id=trader_id,
                importance="debug",
                data={
                    "error": movement_result.error,
                    "current_station_id": trader.current_station_id,
                    "target_station_id": target_station_id,
                },
            )
        )
        return logs

    movement = movement_result.movement

    trader.status = "traveling"
    trader.target_station_id = target_station_id
    trader.active_movement_id = movement.id

    selected_evaluation = next(
        (
            evaluation
            for evaluation in target_choice.evaluations
            if evaluation.station_id == target_station_id
        ),
        None,
    )

    logs.append(
        create_world_log_entry(
            tick=world.current_tick,
            category="npc_trader_movement_started",
            message=f"Trader {trader.name} started traveling to {target_station_id}.",
            target_type="npc_trader",
            target_id=trader_id,
            importance="normal",
            data={
                "movement_id": movement.id,
                "from_station_id": movement.from_station_id,
                "to_station_id": movement.to_station_id,
                "station_path": movement.station_path,
                "route_path": movement.route_path,
                "arrives_at_tick": movement.arrives_at_tick,
                "selected_evaluation": (
                    evaluation_to_dict(selected_evaluation)
                    if selected_evaluation is not None
                    else None
                ),
            },
        )
    )

    return logs


def process_resting_trader_tick(
    *,
    world: WorldState,
    trader_id: str,
    trader: NpcTrader,
) -> list[WorldLogEntry]:
    if trader.rest_until_tick is None:
        trader.status = "idle"
        return []

    if world.current_tick < trader.rest_until_tick:
        return []

    trader.status = "idle"
    trader.rest_until_tick = None

    return [
        create_world_log_entry(
            tick=world.current_tick,
            category="npc_trader_rest_completed",
            message=f"Trader {trader.name} is ready to travel again.",
            target_type="npc_trader",
            target_id=trader_id,
            importance="debug",
            data={
                "current_station_id": trader.current_station_id,
            },
        )
    ]

def choose_trader_target_station(
    *,
    world: WorldState,
    trader: NpcTrader,
) -> TraderTargetChoice:
    preferred_targets = trader.data.get("preferred_targets", [])

    evaluations: list[TraderTargetEvaluation] = []
    best_station_id = None
    best_score = -9999

    for station_id in preferred_targets:
        if station_id == trader.current_station_id:
            continue

        if station_id not in world.stations:
            continue

        evaluation = evaluate_trader_target(
            world=world,
            trader=trader,
            target_station_id=station_id,
        )

        evaluations.append(evaluation)

        if not evaluation.success:
            continue

        if evaluation.score > best_score:
            best_score = evaluation.score
            best_station_id = station_id

    return TraderTargetChoice(
        selected_station_id=best_station_id,
        evaluations=evaluations,
    )