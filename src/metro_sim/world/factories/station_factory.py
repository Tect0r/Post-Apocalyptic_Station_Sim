from metro_sim.models.state_factory import create_initial_station
from metro_sim.world.models.station_state import StationState
from metro_sim.world.factories.influence_factory import create_default_station_influence
from metro_sim.world.factories.pressure_factory import create_default_station_pressure


def create_initial_station_state(station_id: str = "paveletskaya") -> StationState:
    station_dict = create_initial_station()

    return StationState(
        id=station_id,
        name=station_dict["name"],
        resources=station_dict["resources"],
        population=station_dict["population"],
        stats=station_dict["stats"],
        buildings=station_dict["slots"],
        time=station_dict["time"],
        power=station_dict["power"],
        water_system=station_dict["water_system"],
        maintenance=station_dict["maintenance"],
        pressure=create_default_station_pressure(),
        faction_influence=create_default_station_influence(),
    )

def station_state_to_legacy_dict(station: StationState) -> dict:
    return {
        "name": station.name,
        "time": station.time,
        "population": station.population,
        "resources": station.resources,
        "power": station.power,
        "water_system": station.water_system,
        "stats": station.stats,
        "maintenance": station.maintenance,
        "slots": station.buildings,
    }