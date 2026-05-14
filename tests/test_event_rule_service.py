from metro_sim.world.factories.station_factory import create_initial_station_state
from metro_sim.world.services.event_rule_service import station_matches_event_rule


def test_station_matches_event_rule_when_pressure_threshold_is_met():
    station = create_initial_station_state()
    station.pressure["militia_support"] = 25

    rule = {
        "station_pressure": {
            "militia_support": {
                "min": 20
            }
        }
    }

    assert station_matches_event_rule(station, rule) is True


def test_station_does_not_match_event_rule_when_pressure_is_too_low():
    station = create_initial_station_state()
    station.pressure["militia_support"] = 10

    rule = {
        "station_pressure": {
            "militia_support": {
                "min": 20
            }
        }
    }

    assert station_matches_event_rule(station, rule) is False