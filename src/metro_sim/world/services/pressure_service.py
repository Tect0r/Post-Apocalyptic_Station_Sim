from metro_sim.world.models.station_state import StationState


MIN_PRESSURE = 0
MAX_PRESSURE = 100


def add_station_pressure(
    station: StationState,
    pressure_key: str,
    amount: int,
) -> None:
    current_value = station.pressure.get(pressure_key, 0)
    station.pressure[pressure_key] = clamp_pressure(current_value + amount)


def reduce_station_pressure(
    station: StationState,
    pressure_key: str,
    amount: int,
) -> None:
    current_value = station.pressure.get(pressure_key, 0)
    station.pressure[pressure_key] = clamp_pressure(current_value - amount)


def decay_station_pressure(
    station: StationState,
    decay_amount: int = 1,
) -> None:
    for pressure_key in list(station.pressure.keys()):
        reduce_station_pressure(station, pressure_key, decay_amount)


def clamp_pressure(value: int) -> int:
    return max(MIN_PRESSURE, min(MAX_PRESSURE, value))