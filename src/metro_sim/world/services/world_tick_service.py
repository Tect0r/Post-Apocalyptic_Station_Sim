from metro_sim.services.report_service import create_empty_report
from metro_sim.services.tick_service import calculate_next_tick
from metro_sim.world.factories.station_factory import station_state_to_legacy_dict
from metro_sim.world.models.world_state import WorldState


def advance_world_tick(world: WorldState) -> dict:
    world.current_tick += 1

    world_report = {
        "tick": world.current_tick,
        "station_reports": {},
        "events": [],
    }

    for station_id, station in world.stations.items():
        station_report = create_empty_report()

        legacy_station = station_state_to_legacy_dict(station)
        calculate_next_tick(legacy_station, station_report)

        world_report["station_reports"][station_id] = station_report

    return world_report