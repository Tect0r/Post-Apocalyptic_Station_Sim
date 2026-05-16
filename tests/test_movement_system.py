from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.simulation.movement_system import (
    process_world_movements,
    start_world_movement,
)


def test_start_world_movement_creates_active_movement():
    world = create_world()

    result = start_world_movement(
        world=world,
        actor_type="trader",
        actor_id="trader_001",
        from_station_id="paveletskaya_ring",
        to_station_id="sevastopolskaya",
    )

    assert result.success is True
    assert result.movement is not None
    assert len(world.movements) == 1

    movement = result.movement

    assert movement.actor_type == "trader"
    assert movement.actor_id == "trader_001"
    assert movement.from_station_id == "paveletskaya_ring"
    assert movement.to_station_id == "sevastopolskaya"
    assert movement.status == "active"
    assert movement.arrives_at_tick > movement.started_at_tick
    assert movement.station_path[0] == "paveletskaya_ring"
    assert movement.station_path[-1] == "sevastopolskaya"


def test_start_world_movement_fails_for_unknown_station():
    world = create_world()

    result = start_world_movement(
        world=world,
        actor_type="trader",
        actor_id="trader_001",
        from_station_id="unknown",
        to_station_id="sevastopolskaya",
    )

    assert result.success is False
    assert result.error == "from_station_not_found"
    assert len(world.movements) == 0


def test_process_world_movements_completes_arrived_movement():
    world = create_world()

    result = start_world_movement(
        world=world,
        actor_type="trader",
        actor_id="trader_001",
        from_station_id="paveletskaya_ring",
        to_station_id="sevastopolskaya",
    )

    movement = result.movement
    assert movement is not None

    world.current_tick = movement.arrives_at_tick

    logs = process_world_movements(world)

    assert movement.status == "completed"
    assert len(logs) == 1
    assert logs[0].category == "movement_completed"


def test_process_world_movements_keeps_movement_active_before_arrival():
    world = create_world()

    result = start_world_movement(
        world=world,
        actor_type="trader",
        actor_id="trader_001",
        from_station_id="paveletskaya_ring",
        to_station_id="sevastopolskaya",
    )

    movement = result.movement
    assert movement is not None

    world.current_tick = movement.arrives_at_tick - 1

    logs = process_world_movements(world)

    assert movement.status == "active"
    assert logs == []