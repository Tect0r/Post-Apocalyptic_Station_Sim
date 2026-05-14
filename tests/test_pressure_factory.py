from metro_sim.world.factories.pressure_factory import create_default_station_pressure


def test_default_station_pressure_contains_expected_keys():
    pressure = create_default_station_pressure()

    assert pressure["sabotage"] == 0
    assert pressure["supply_support"] == 0
    assert pressure["militia_support"] == 0
    assert pressure["smuggling"] == 0
    assert pressure["medical_support"] == 0
    assert pressure["trade_activity"] == 0