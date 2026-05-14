from metro_sim.world.factories.station_factory import create_initial_station_state
from metro_sim.world.services.pressure_service import (
    add_station_pressure,
    decay_station_pressure,
    reduce_station_pressure,
)


def test_add_station_pressure_increases_value():
    station = create_initial_station_state()

    add_station_pressure(station, "militia_support", 8)

    assert station.pressure["militia_support"] == 8


def test_station_pressure_is_capped_at_100():
    station = create_initial_station_state()

    add_station_pressure(station, "sabotage", 150)

    assert station.pressure["sabotage"] == 100


def test_reduce_station_pressure_does_not_go_below_zero():
    station = create_initial_station_state()

    reduce_station_pressure(station, "smuggling", 10)

    assert station.pressure["smuggling"] == 0


def test_decay_station_pressure_reduces_all_values():
    station = create_initial_station_state()
    station.pressure["militia_support"] = 8
    station.pressure["medical_support"] = 3

    decay_station_pressure(station, decay_amount=1)

    assert station.pressure["militia_support"] == 7
    assert station.pressure["medical_support"] == 2