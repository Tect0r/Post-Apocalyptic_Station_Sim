from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.services.influence_service import (
    add_faction_influence,
    reduce_faction_influence,
)


def test_add_faction_influence_keeps_total_at_100():
    world = create_world()
    station = world.stations["paveletskaya"]

    add_faction_influence(station, "hansa", 48)

    assert sum(station.faction_influence.values()) == 100
    assert station.faction_influence["hansa"] > 48


def test_reduce_faction_influence_keeps_total_at_100():
    world = create_world()
    station = world.stations["paveletskaya"]

    reduce_faction_influence(station, "hansa", 48)

    assert sum(station.faction_influence.values()) == 100
    assert station.faction_influence["hansa"] < 48