from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.services.pressure_service import (
    add_station_pressure,
    decay_station_pressure,
    reduce_station_pressure,
)


def test_add_station_pressure_increases_value():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    add_station_pressure(station, "militia_support", 8)

    assert station.pressure["militia_support"] == 8


def test_station_pressure_is_capped_at_100():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    add_station_pressure(station, "sabotage", 150)

    assert station.pressure["sabotage"] == 100


def test_reduce_station_pressure_does_not_go_below_zero():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    reduce_station_pressure(station, "smuggling", 10)

    assert station.pressure["smuggling"] == 0


def test_decay_station_pressure_reduces_all_values():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    station.pressure["militia_support"] = 8
    station.pressure["medical_support"] = 3

    decay_station_pressure(station, decay_amount=1)

    assert station.pressure["militia_support"] == 7
    assert station.pressure["medical_support"] == 2