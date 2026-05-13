from metro_sim.world.factories.station_factory import create_initial_station_state
from metro_sim.world.models.world_state import WorldState


def create_initial_world() -> WorldState:
    station = create_initial_station_state("paveletskaya")

    return WorldState(
        current_tick=0,
        stations={
            station.id: station,
        },
        factions={},
        routes={},
        events=[],
    )