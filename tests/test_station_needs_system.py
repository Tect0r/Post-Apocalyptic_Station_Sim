from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.simulation.effect_system import apply_world_effects
from metro_sim.world.simulation.station_system import process_station_tick


def test_food_shortage_reduces_morale_and_increases_unrest():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    station.inhabited = True
    station.population = 500
    station.resources["food"] = 50
    station.stats["morale"] = 50
    station.pressure["unrest"] = 0

    result = process_station_tick(
        station=station,
        current_tick=world.current_tick,
    )

    apply_world_effects(
        world=world,
        effects=result.effects,
    )

    assert station.stats["morale"] < 50
    assert station.pressure["unrest"] > 0


def test_water_shortage_reduces_health():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    station.inhabited = True
    station.population = 500
    station.resources["water"] = 50
    station.stats["health"] = 50

    result = process_station_tick(
        station=station,
        current_tick=world.current_tick,
    )

    apply_world_effects(
        world=world,
        effects=result.effects,
    )

    assert station.stats["health"] < 50


def test_medicine_shortage_increases_medical_support_pressure():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    station.inhabited = True
    station.population = 500
    station.resources["medicine"] = 1
    station.pressure["medical_support"] = 0

    result = process_station_tick(
        station=station,
        current_tick=world.current_tick,
    )

    apply_world_effects(
        world=world,
        effects=result.effects,
    )

    assert station.pressure["medical_support"] > 0


def test_ammo_shortage_reduces_security_and_increases_security_risk():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    station.inhabited = True
    station.population = 500
    station.resources["ammo"] = 5
    station.stats["security"] = 50
    station.pressure["security_risk"] = 0

    result = process_station_tick(
        station=station,
        current_tick=world.current_tick,
    )

    apply_world_effects(
        world=world,
        effects=result.effects,
    )

    assert station.stats["security"] < 50
    assert station.pressure["security_risk"] > 0


def test_abandoned_station_does_not_process_human_needs():
    world = create_world()
    station = world.stations["nagornaya"]

    station.inhabited = False
    station.population = 0
    station.resources["food"] = 0
    station.stats["morale"] = 0
    station.pressure["unrest"] = 0

    result = process_station_tick(
        station=station,
        current_tick=world.current_tick,
    )

    apply_world_effects(
        world=world,
        effects=result.effects,
    )

    assert station.stats["morale"] == 0
    assert station.pressure["unrest"] == 0


def test_abandoned_mutant_station_increases_danger_pressure():
    world = create_world()
    station = world.stations["nagornaya"]

    station.inhabited = False
    station.tags.append("mutant_activity")
    station.pressure["danger"] = 10

    result = process_station_tick(
        station=station,
        current_tick=world.current_tick,
    )

    apply_world_effects(
        world=world,
        effects=result.effects,
    )

    assert station.pressure["danger"] > 10