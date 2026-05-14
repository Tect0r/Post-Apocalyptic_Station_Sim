from metro_sim.world.models.station_state import StationState
from metro_sim.world.services.influence_service import add_faction_influence, reduce_faction_influence
from metro_sim.world.services.pressure_service import add_station_pressure, reduce_station_pressure


def apply_world_event_effects(station: StationState, effects: dict) -> None:
    apply_pressure_effects(station, effects.get("pressure", {}))
    apply_faction_influence_effects(station, effects.get("faction_influence", {}))
    apply_station_stat_effects(station, effects.get("station_stats", {}))


def apply_pressure_effects(station: StationState, pressure_effects: dict[str, int]) -> None:
    for pressure_key, delta in pressure_effects.items():
        if delta >= 0:
            add_station_pressure(station, pressure_key, delta)
        else:
            reduce_station_pressure(station, pressure_key, abs(delta))


def apply_faction_influence_effects(station: StationState, influence_effects: dict[str, int]) -> None:
    for faction_key, delta in influence_effects.items():
        if delta >= 0:
            add_faction_influence(station, faction_key, delta)
        else:
            reduce_faction_influence(station, faction_key, abs(delta))


def apply_station_stat_effects(station: StationState, stat_effects: dict[str, int]) -> None:
    for stat_key, delta in stat_effects.items():
        if stat_key not in station.stats:
            continue

        station.stats[stat_key] += delta