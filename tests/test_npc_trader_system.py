from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.models.npc_trader import create_npc_trader
from metro_sim.world.simulation.movement_system import process_world_movements
from metro_sim.world.simulation.npc_trader_system import process_npc_traders_tick


def test_npc_trader_system_starts_movement_for_idle_trader():
    world = create_world()

    trader = create_npc_trader(
        name="Test Trader",
        current_station_id="paveletskaya_ring",
        home_station_id="paveletskaya_ring",
        data={
            "preferred_targets": ["sevastopolskaya"]
        },
    )

    world.npc_traders = {
        trader.id: trader
    }

    logs = process_npc_traders_tick(world)

    assert trader.status == "traveling"
    assert trader.target_station_id == "sevastopolskaya"
    assert trader.active_movement_id is not None
    assert len(world.movements) == 1
    assert len(logs) == 1
    assert logs[0].category == "npc_trader_movement_started"


def test_npc_trader_system_does_not_start_movement_for_traveling_trader():
    world = create_world()

    trader = create_npc_trader(
        name="Test Trader",
        current_station_id="paveletskaya_ring",
        home_station_id="paveletskaya_ring",
        data={
            "preferred_targets": ["sevastopolskaya"]
        },
    )
    trader.status = "traveling"

    world.npc_traders = {
        trader.id: trader
    }

    logs = process_npc_traders_tick(world)

    assert len(world.movements) == 0
    assert logs == []


def test_npc_trader_arrival_updates_trader_location():
    world = create_world()

    trader = create_npc_trader(
        name="Test Trader",
        current_station_id="paveletskaya_ring",
        home_station_id="paveletskaya_ring",
        data={
            "preferred_targets": ["paveletskaya_radial"]
        },
    )

    world.npc_traders = {
        trader.id: trader
    }

    process_npc_traders_tick(world)

    movement = world.movements[0]
    world.current_tick = movement.arrives_at_tick

    logs = process_world_movements(world)

    assert movement.status == "completed"
    assert trader.status == "idle"
    assert trader.current_station_id == "paveletskaya_radial"
    assert trader.target_station_id is None
    assert trader.active_movement_id is None
    assert any(log.category == "movement_completed" for log in logs)


def test_npc_trader_system_ignores_invalid_target():
    world = create_world()

    trader = create_npc_trader(
        name="Test Trader",
        current_station_id="paveletskaya_ring",
        home_station_id="paveletskaya_ring",
        data={
            "preferred_targets": ["unknown_station"]
        },
    )

    world.npc_traders = {
        trader.id: trader
    }

    logs = process_npc_traders_tick(world)

    assert trader.status == "idle"
    assert len(world.movements) == 0
    assert logs == []