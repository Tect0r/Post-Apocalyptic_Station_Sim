from metro_sim.world.models.station_state import StationState


MIN_INFLUENCE = 0
MAX_TOTAL_INFLUENCE = 100


def add_faction_influence(
    station: StationState,
    faction_key: str,
    amount: int,
) -> None:
    current_value = station.faction_influence.get(faction_key, 0)
    station.faction_influence[faction_key] = max(MIN_INFLUENCE, current_value + amount)
    normalize_station_influence(station)


def reduce_faction_influence(
    station: StationState,
    faction_key: str,
    amount: int,
) -> None:
    current_value = station.faction_influence.get(faction_key, 0)
    station.faction_influence[faction_key] = max(MIN_INFLUENCE, current_value - amount)
    normalize_station_influence(station)


def normalize_station_influence(station: StationState) -> None:
    total = sum(station.faction_influence.values())

    if total <= 0:
        return

    normalized = {
        faction_key: round((value / total) * MAX_TOTAL_INFLUENCE)
        for faction_key, value in station.faction_influence.items()
    }

    difference = MAX_TOTAL_INFLUENCE - sum(normalized.values())

    if difference != 0:
        strongest_faction = max(normalized, key=normalized.get)
        normalized[strongest_faction] += difference

    station.faction_influence = normalized