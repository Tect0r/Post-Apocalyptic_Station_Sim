from metro_sim.world.factories.station_factory import (
    create_initial_station_state,
    station_state_to_legacy_dict,
)


def test_station_state_can_be_converted_to_legacy_dict():
    station_state = create_initial_station_state()

    legacy_station = station_state_to_legacy_dict(station_state)

    assert legacy_station["name"] == station_state.name
    assert legacy_station["resources"] is station_state.resources
    assert legacy_station["population"] is station_state.population
    assert legacy_station["slots"] is station_state.buildings
    assert legacy_station["time"] is station_state.time