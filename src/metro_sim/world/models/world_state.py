from dataclasses import dataclass, field
from metro_sim.world.models.station_state import StationState
from metro_sim.world.models.world_log_entry import WorldLogEntry
from metro_sim.world.models.world_event import WorldEvent
from metro_sim.world.models.world_snapshot import WorldSnapshot
from metro_sim.world.models.world_movement import WorldMovement


@dataclass
class WorldState:
    current_tick: int
    stations: dict[str, StationState]
    factions: dict = field(default_factory=dict)
    routes: dict = field(default_factory=dict)
    events: list[WorldEvent] = field(default_factory=list)
    contracts: dict = field(default_factory=dict)
    pvp_impacts: list = field(default_factory=list)
    logs: list[WorldLogEntry] = field(default_factory=list)
    snapshots: list[WorldSnapshot] = field(default_factory=list)
    movements: list[WorldMovement] = field(default_factory=list)