from dataclasses import dataclass, field

from metro_sim.world.models.station_state import StationState


@dataclass
class WorldState:
    current_tick: int
    stations: dict[str, StationState]
    factions: dict = field(default_factory=dict)
    routes: dict = field(default_factory=dict)
    events: list = field(default_factory=list)