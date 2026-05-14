from metro_sim.world.models.station_state import StationState
from metro_sim.world.models.tick_result import StationTickResult
from metro_sim.world.services.pressure_service import decay_station_pressure


def simulate_station_tick(station: StationState) -> StationTickResult:
    decay_station_pressure(station, decay_amount=1)
    apply_basic_station_drift(station)

    return StationTickResult(
        station_id=station.id,
        report={
            "station_id": station.id,
            "pressure": station.pressure,
            "stats": station.stats,
            "faction_influence": station.faction_influence,
        },
        events=[],
    )


def apply_basic_station_drift(station: StationState) -> None:
    if station.pressure.get("sabotage", 0) >= 20:
        station.stats["security"] = max(0, station.stats.get("security", 0) - 1)

    if station.pressure.get("medical_support", 0) >= 10:
        station.stats["health"] = min(100, station.stats.get("health", 0) + 1)

    if station.pressure.get("militia_support", 0) >= 10:
        station.stats["order"] = min(100, station.stats.get("order", 0) + 1)

    if station.pressure.get("smuggling", 0) >= 15:
        station.stats["order"] = max(0, station.stats.get("order", 0) - 1)