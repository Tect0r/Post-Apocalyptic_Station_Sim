from metro_sim.world.factories.station_factory import create_initial_station_state
from metro_sim.world.services.station_tick_service import simulate_station_tick


def test_simulate_station_tick_returns_station_tick_result():
    station = create_initial_station_state("paveletskaya")

    result = simulate_station_tick(station)

    assert result.station_id == "paveletskaya"
    assert isinstance(result.report, dict)
    assert isinstance(result.events, list)


def test_simulate_station_tick_changes_station_time():
    station = create_initial_station_state("paveletskaya")

    hour_before = station.time["hour"]

    simulate_station_tick(station)

    hour_after = station.time["hour"]

    assert hour_after != hour_before or station.time != {}