from metro_sim.world.factories.world_factory import create_world


def test_world_has_slice_stations():
    world = create_world()

    assert "paveletskaya_ring" in world.stations
    assert "paveletskaya_radial" in world.stations
    assert "sevastopolskaya" in world.stations
    assert len(world.stations) == 8


def test_world_has_slice_routes():
    world = create_world()

    assert len(world.routes) == 7


def test_world_has_factions():
    world = create_world()

    assert "hansa" in world.factions
    assert "independent" in world.factions
    assert "bandits" in world.factions
    assert "polis" in world.factions


def test_station_has_pressure_and_influence():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    assert "militia_support" in station.pressure
    assert "hansa" in station.faction_influence
    assert sum(station.faction_influence.values()) == 100