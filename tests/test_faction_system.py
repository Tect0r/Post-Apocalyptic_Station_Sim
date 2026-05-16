from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.simulation.effect_system import apply_world_effects
from metro_sim.world.simulation.faction_system import process_factions_tick


def test_faction_system_strong_hansa_influence_increases_order():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    station.faction_influence["hansa"] = 70
    station.stats["order"] = 50

    effects, logs = process_factions_tick(world)
    apply_world_effects(world=world, effects=effects)

    assert station.stats["order"] == 51
    assert any(effect.reason == "strong_hansa_influence" for effect in effects)
    assert len(logs) >= 1


def test_faction_system_strong_bandit_influence_increases_smuggling_and_security_risk():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    station.faction_influence["bandits"] = 50
    station.pressure["smuggling"] = 0
    station.pressure["security_risk"] = 0

    effects, logs = process_factions_tick(world)
    apply_world_effects(world=world, effects=effects)

    assert station.pressure["smuggling"] == 1
    assert station.pressure["security_risk"] == 1
    assert any(effect.reason == "strong_bandit_influence" for effect in effects)
    assert len(logs) >= 1


def test_faction_system_weak_independent_influence_increases_faction_tension():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    station.faction_influence["independent"] = 10
    station.pressure["faction_tension"] = 0

    effects, logs = process_factions_tick(world)
    apply_world_effects(world=world, effects=effects)

    assert station.pressure["faction_tension"] == 1
    assert any(effect.reason == "weak_independent_influence" for effect in effects)
    assert len(logs) >= 1


def test_faction_system_bandit_route_control_increases_connected_station_pressure():
    world = create_world()

    route_id = next(iter(world.routes.keys()))
    route = world.routes[route_id]

    route.control["bandits"] = 50

    from_station_id = route.from_station_id
    to_station_id = route.to_station_id

    world.stations[from_station_id].pressure["danger"] = 0
    world.stations[to_station_id].pressure["danger"] = 0

    world.stations[from_station_id].pressure["security_risk"] = 0
    world.stations[to_station_id].pressure["security_risk"] = 0

    effects, logs = process_factions_tick(world)
    apply_world_effects(world=world, effects=effects)

    assert world.stations[from_station_id].pressure["danger"] == 1
    assert world.stations[to_station_id].pressure["danger"] == 1

    assert world.stations[from_station_id].pressure["security_risk"] == 1
    assert world.stations[to_station_id].pressure["security_risk"] == 1

    assert any(effect.reason == "bandit_route_control" for effect in effects)
    assert len(logs) >= 1


def test_faction_system_hansa_route_control_reduces_supply_disruption():
    world = create_world()

    route_id = next(iter(world.routes.keys()))
    route = world.routes[route_id]

    route.control["hansa"] = 70

    from_station_id = route.from_station_id
    to_station_id = route.to_station_id

    world.stations[from_station_id].pressure["supply_disruption"] = 5
    world.stations[to_station_id].pressure["supply_disruption"] = 5

    effects, logs = process_factions_tick(world)
    apply_world_effects(world=world, effects=effects)

    assert world.stations[from_station_id].pressure["supply_disruption"] == 4
    assert world.stations[to_station_id].pressure["supply_disruption"] == 4

    assert any(effect.reason == "hansa_route_control" for effect in effects)
    assert len(logs) >= 1