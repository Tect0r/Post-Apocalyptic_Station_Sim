from metro_sim.world.models.faction_type import FactionType


def create_default_station_influence() -> dict[str, int]:
    return {
        FactionType.HANSA.value: 48,
        FactionType.INDEPENDENT.value: 32,
        FactionType.BANDITS.value: 9,
        FactionType.RED_LINE.value: 7,
        FactionType.POLIS.value: 4,
        FactionType.REICH.value: 0
    }