from metro_sim.models.state_factory import create_initial_station


def test_initial_station_has_expected_name():
    station = create_initial_station()

    assert station["name"] == "Paveletskaya"


def test_initial_station_has_resources():
    station = create_initial_station()

    assert "resources" in station
    assert "food" in station["resources"]
    assert "water" in station["resources"]
    assert "ammo" in station["resources"]
    assert "trade_goods" in station["resources"]
    assert "medicine" in station["resources"]
    assert "power_usage" in station["resources"]


def test_initial_population_is_consistent():
    station = create_initial_station()

    population = station["population"]

    assert population["total"] == population["employed"] + population["unemployed"]


def test_initial_work_assignment_does_not_exceed_working_population():
    station = create_initial_station()

    assigned_workers = sum(station["work_assignment"].values())

    assert assigned_workers <= station["population"]["employed"]


def test_initial_stats_are_between_0_and_100():
    station = create_initial_station()

    for value in station["stats"].values():
        assert 0 <= value <= 100


def test_initial_power_level_is_valid():
    station = create_initial_station()

    assert 0 <= station["stats"]["power_level"] <= 4