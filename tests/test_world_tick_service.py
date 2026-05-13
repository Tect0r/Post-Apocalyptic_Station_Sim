from metro_sim.world.factories.world_factory import create_initial_world
from metro_sim.world.services.world_tick_service import advance_world_tick
from metro_sim.world.factories.station_factory import create_initial_station_state

def test_advance_world_tick_increases_current_tick():
    world = create_initial_world()

    result = advance_world_tick(world)

    assert world.current_tick == 1
    assert result.tick == 1


def test_advance_world_tick_returns_station_report():
    world = create_initial_world()

    result = advance_world_tick(world)

    assert "paveletskaya" in result.station_reports
    assert isinstance(result.station_reports["paveletskaya"], dict)

def test_advance_world_tick_ticks_multiple_stations():
    world = create_initial_world()

    second_station = create_initial_station_state("polis")
    world.stations["polis"] = second_station

    result = advance_world_tick(world)

    assert world.current_tick == 1
    assert "paveletskaya" in result.station_reports
    assert "polis" in result.station_reports