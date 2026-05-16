from metro_sim.world.factories.world_factory import create_world


def test_create_initial_world_contains_paveletskaya():
    world = create_world()

    assert world.current_tick == 0
    assert "paveletskaya_radial" in world.stations

    station = world.stations["paveletskaya_radial"]

    assert station.id == "paveletskaya_radial"
    assert station.name is not None
    assert station.resources is not None
    assert station.population is not None