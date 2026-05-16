from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.services.world_tick_service import advance_world_tick

def test_advance_world_tick_increases_current_tick():
    world = create_world()

    result = advance_world_tick(world)

    assert world.current_tick == 1
    assert result.tick == 1


def test_advance_world_tick_returns_station_report():
    world = create_world()

    result = advance_world_tick(world)

    assert "paveletskaya_radial" in result.station_reports
    assert isinstance(result.station_reports["paveletskaya_radial"], dict)

def test_advance_world_tick_ticks_multiple_stations():
    world = create_world()

    result = advance_world_tick(world)

    assert world.current_tick == 1
    assert "paveletskaya_radial" in result.station_reports
    assert "dobryninskaya_serpukhovskaya" in result.station_reports