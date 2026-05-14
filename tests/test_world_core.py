from metro_sim.world.factories.world_factory import create_world


def test_world_has_three_stations():
    world = create_world()

    assert len(world.stations) == 3
    assert "paveletskaya" in world.stations
    assert "polis" in world.stations
    assert "hansa_ring" in world.stations


def test_world_has_routes():
    world = create_world()

    assert len(world.routes) == 3
    assert "route_paveletskaya_polis" in world.routes
    assert "route_paveletskaya_hansa_ring" in world.routes
    assert "route_hansa_ring_polis" in world.routes


def test_world_has_factions():
    world = create_world()

    assert "hansa" in world.factions
    assert "independent" in world.factions
    assert "bandits" in world.factions
    assert "polis" in world.factions


def test_station_has_pressure_and_influence():
    world = create_world()
    station = world.stations["paveletskaya"]

    assert "militia_support" in station.pressure
    assert "hansa" in station.faction_influence
    assert sum(station.faction_influence.values()) == 100