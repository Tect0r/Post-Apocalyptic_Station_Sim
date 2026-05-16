from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.simulation.effect_system import apply_world_effects
from metro_sim.world.simulation.production_system import process_production_tick


def test_production_system_adds_resources_on_interval_tick():
    world = create_world()
    station = world.stations["paveletskaya_ring"]

    station.resources["trade_goods"] = 0
    world.current_tick = 10

    effects, logs = process_production_tick(world)
    apply_world_effects(world=world, effects=effects)

    assert station.resources["trade_goods"] > 0
    assert len(logs) >= 1


def test_production_system_skips_non_interval_tick():
    world = create_world()
    world.current_tick = 9

    effects, logs = process_production_tick(world)

    assert effects == []
    assert logs == []


def test_production_system_skips_abandoned_station():
    world = create_world()
    station = world.stations["nagornaya"]

    station.inhabited = False
    station.resources["food"] = 0
    world.current_tick = 10

    effects, logs = process_production_tick(world)
    apply_world_effects(world=world, effects=effects)

    assert station.resources["food"] == 0