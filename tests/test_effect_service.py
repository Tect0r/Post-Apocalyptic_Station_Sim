from metro_sim.world.factories.station_factory import create_initial_station_state
from metro_sim.world.services.event_effect_service import apply_world_event_effects


def test_world_event_effects_modify_pressure_and_influence():
    station = create_initial_station_state()
    station.pressure["militia_support"] = 25
    independent_before = station.faction_influence["independent"]

    effects = {
        "pressure": {
            "militia_support": -10
        },
        "faction_influence": {
            "independent": 4
        }
    }

    apply_world_event_effects(station, effects)

    assert station.pressure["militia_support"] == 15
    assert station.faction_influence["independent"] > independent_before
    assert sum(station.faction_influence.values()) == 100