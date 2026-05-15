from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.simulation.tick_orchestrator import process_world_tick


def test_process_world_tick_advances_current_tick_by_one():
    world = create_world()
    start_tick = world.current_tick

    result = process_world_tick(world)

    assert world.current_tick == start_tick + 1
    assert result.tick == world.current_tick


def test_process_world_tick_returns_station_reports():
    world = create_world()

    result = process_world_tick(world)

    assert result.station_reports
    assert set(result.station_reports.keys()) == set(world.stations.keys())


def test_process_world_tick_stores_logs():
    world = create_world()

    process_world_tick(world)

    assert hasattr(world, "logs")
    assert len(world.logs) > 0


def test_process_world_tick_applies_effects():
    world = create_world()

    station = next(iter(world.stations.values()))
    station.pressure["sabotage"] = 25
    station.stats["security"] = 50

    process_world_tick(world)

    assert station.stats["security"] < 50