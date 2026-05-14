from metro_sim.world.models.pressure_type import PressureType


def create_default_station_pressure() -> dict[str, int]:
    return {
        pressure_type.value: 0
        for pressure_type in PressureType
    }