from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.simulation.consumption_system import (
    calculate_station_consumption,
    process_consumption_tick,
)
from metro_sim.world.simulation.effect_system import apply_world_effects


def test_consumption_system_consumes_resources_on_interval_tick():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    station.population = 500
    station.resources["food"] = 100
    world.current_tick = 10

    effects, logs = process_consumption_tick(world)
    apply_world_effects(world=world, effects=effects)

    assert station.resources["food"] < 100
    assert len(logs) >= 1


def test_consumption_system_skips_non_interval_tick():
    world = create_world()
    world.current_tick = 9

    effects, logs = process_consumption_tick(world)

    assert effects == []
    assert logs == []


def test_consumption_system_skips_abandoned_station():
    world = create_world()
    station = world.stations["nagornaya"]

    station.inhabited = False
    station.resources["food"] = 100
    world.current_tick = 10

    effects, logs = process_consumption_tick(world)
    apply_world_effects(world=world, effects=effects)

    assert station.resources["food"] == 100


def test_calculate_station_consumption_scales_with_population():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    station.population = 100
    low_consumption = calculate_station_consumption(station)

    station.population = 500
    high_consumption = calculate_station_consumption(station)

    assert high_consumption["food"] > low_consumption["food"]
    assert high_consumption["water"] > low_consumption["water"]