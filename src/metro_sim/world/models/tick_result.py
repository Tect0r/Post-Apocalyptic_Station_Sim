from dataclasses import dataclass, field

from metro_sim.world.models.world_effect import WorldEffect
from metro_sim.world.models.world_log_entry import WorldLogEntry
from metro_sim.world.models.world_event import WorldEvent


@dataclass
class StationTickResult:
    station_id: str
    report: dict
    effects: list[WorldEffect] = field(default_factory=list)
    logs: list[WorldLogEntry] = field(default_factory=list)


@dataclass
class WorldTickResult:
    tick: int
    station_reports: dict[str, dict] = field(default_factory=dict)
    effects: list[WorldEffect] = field(default_factory=list)
    logs: list[WorldLogEntry] = field(default_factory=list)
    events: list[WorldEvent] = field(default_factory=list)