from metro_sim.world.factories.world_factory import create_initial_world


def test_create_initial_world_contains_paveletskaya():
    world = create_initial_world()

    assert world.current_tick == 0
    assert "paveletskaya" in world.stations

    station = world.stations["paveletskaya"]

    assert station.id == "paveletskaya"
    assert station.name is not None
    assert station.resources is not None
    assert station.population is not None
    assert station.buildings is not None