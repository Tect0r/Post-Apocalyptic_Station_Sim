from metro_sim.world.factories.world_factory import create_initial_world
from metro_sim.world.services.world_tick_service import advance_world_tick


def test_advance_world_tick_increases_current_tick():
    world = create_initial_world()

    advance_world_tick(world)

    assert world.current_tick == 1


def test_advance_world_tick_returns_station_report():
    world = create_initial_world()

    report = advance_world_tick(world)

    assert "station_reports" in report
    assert "paveletskaya" in report["station_reports"]