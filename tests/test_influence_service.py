from metro_sim.world.factories.station_factory import create_initial_station_state
from metro_sim.world.services.influence_service import (
    add_faction_influence,
    reduce_faction_influence,
)


def test_add_faction_influence_keeps_total_at_100():
    station = create_initial_station_state()

    add_faction_influence(station, "hansa", 20)

    assert sum(station.faction_influence.values()) == 100
    assert station.faction_influence["hansa"] > 48


def test_reduce_faction_influence_keeps_total_at_100():
    station = create_initial_station_state()

    reduce_faction_influence(station, "hansa", 20)

    assert sum(station.faction_influence.values()) == 100
    assert station.faction_influence["hansa"] < 48