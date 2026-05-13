from metro_sim.services.report_service import create_empty_report
from metro_sim.services.tick_service import calculate_next_tick
from metro_sim.world.factories.station_factory import station_state_to_legacy_dict
from metro_sim.world.models.station_state import StationState
from metro_sim.world.models.tick_result import StationTickResult

def simulate_station_tick(station: StationState) -> StationTickResult:
    station_report = create_empty_report()

    legacy_station = station_state_to_legacy_dict(station)
    calculate_next_tick(legacy_station, station_report)

    return StationTickResult(
        station_id=station.id,
        report=station_report,
        events=[],
    )
