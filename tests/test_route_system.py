from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.simulation.effect_system import apply_world_effects
from metro_sim.world.simulation.route_system import process_routes_tick


def test_route_system_creates_danger_pressure_for_connected_stations():
    world = create_world()

    route_id = next(iter(world.routes.keys()))
    route = world.routes[route_id]

    route.danger = 75
    route.condition = 100
    route.traffic = 0

    from_station_id = route.from_station_id
    to_station_id = route.to_station_id

    world.stations[from_station_id].pressure["danger"] = 0
    world.stations[to_station_id].pressure["danger"] = 0

    effects, logs = process_routes_tick(world)

    assert any(effect.reason == "dangerous_route_nearby" for effect in effects)
    assert len(logs) >= 1

    apply_world_effects(world=world, effects=effects)

    assert world.stations[from_station_id].pressure["danger"] == 1
    assert world.stations[to_station_id].pressure["danger"] == 1


def test_route_system_creates_supply_disruption_for_damaged_route():
    world = create_world()

    route_id = next(iter(world.routes.keys()))
    route = world.routes[route_id]

    route.danger = 0
    route.condition = 20
    route.traffic = 0

    from_station_id = route.from_station_id
    to_station_id = route.to_station_id

    world.stations[from_station_id].pressure["supply_disruption"] = 0
    world.stations[to_station_id].pressure["supply_disruption"] = 0

    effects, logs = process_routes_tick(world)

    assert any(effect.reason == "damaged_route_nearby" for effect in effects)
    assert len(logs) >= 1

    apply_world_effects(world=world, effects=effects)

    assert world.stations[from_station_id].pressure["supply_disruption"] == 1
    assert world.stations[to_station_id].pressure["supply_disruption"] == 1


def test_route_system_creates_security_risk_for_unsafe_high_traffic_route():
    world = create_world()

    route_id = next(iter(world.routes.keys()))
    route = world.routes[route_id]

    route.danger = 60
    route.condition = 100
    route.traffic = 60

    from_station_id = route.from_station_id
    to_station_id = route.to_station_id

    world.stations[from_station_id].pressure["security_risk"] = 0
    world.stations[to_station_id].pressure["security_risk"] = 0

    effects, logs = process_routes_tick(world)

    assert any(effect.reason == "unsafe_high_traffic_route" for effect in effects)
    assert len(logs) >= 1

    apply_world_effects(world=world, effects=effects)

    assert world.stations[from_station_id].pressure["security_risk"] == 1
    assert world.stations[to_station_id].pressure["security_risk"] == 1