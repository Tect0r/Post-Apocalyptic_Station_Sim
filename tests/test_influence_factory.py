from metro_sim.world.factories.influence_factory import create_default_station_influence


def test_default_station_influence_sums_to_100():
    influence = create_default_station_influence()

    assert sum(influence.values()) == 100


def test_default_station_influence_contains_expected_factions():
    influence = create_default_station_influence()

    assert "hansa" in influence
    assert "independent" in influence
    assert "bandits" in influence
    assert "red_line" in influence
    assert "polis" in influence
    assert "reich" in influence