from dataclasses import dataclass

from metro_sim.world.models.world_log_entry import WorldLogEntry, create_world_log_entry
from metro_sim.world.models.world_movement import WorldMovement, create_world_movement
from metro_sim.world.models.world_state import WorldState
from metro_sim.world.services.pathfinding_service import find_station_path


@dataclass
class StartMovementResult:
    success: bool
    movement: WorldMovement | None = None
    error: str | None = None


def start_world_movement(
    *,
    world: WorldState,
    actor_type: str,
    actor_id: str,
    from_station_id: str,
    to_station_id: str,
) -> StartMovementResult:
    path_result = find_station_path(
        world=world,
        from_station_id=from_station_id,
        to_station_id=to_station_id,
    )

    if not path_result.success:
        return StartMovementResult(
            success=False,
            error=path_result.error,
        )

    movement = create_world_movement(
        actor_type=actor_type,
        actor_id=actor_id,
        from_station_id=from_station_id,
        to_station_id=to_station_id,
        station_path=path_result.station_ids,
        route_path=path_result.route_ids,
        started_at_tick=world.current_tick,
        arrives_at_tick=world.current_tick + path_result.total_travel_time_ticks,
        data={
            "total_travel_time_ticks": path_result.total_travel_time_ticks,
        },
    )

    world.movements.append(movement)

    return StartMovementResult(
        success=True,
        movement=movement,
    )


def process_world_movements(
    world: WorldState,
) -> list[WorldLogEntry]:
    logs: list[WorldLogEntry] = []

    for movement in world.movements:
        if movement.status != "active":
            continue

        if world.current_tick < movement.arrives_at_tick:
            continue

        movement.status = "completed"

        logs.append(
            create_world_log_entry(
                tick=world.current_tick,
                category="movement_completed",
                message=(
                    f"{movement.actor_type} {movement.actor_id} arrived at "
                    f"{movement.to_station_id}."
                ),
                target_type=movement.actor_type,
                target_id=movement.actor_id,
                importance="normal",
                data={
                    "movement_id": movement.id,
                    "from_station_id": movement.from_station_id,
                    "to_station_id": movement.to_station_id,
                    "station_path": movement.station_path,
                    "route_path": movement.route_path,
                    "started_at_tick": movement.started_at_tick,
                    "arrives_at_tick": movement.arrives_at_tick,
                },
            )
        )

    return logs