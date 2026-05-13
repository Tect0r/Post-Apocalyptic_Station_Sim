from dataclasses import dataclass, field

@dataclass
class StationTickResult:
    station_id: str
    report: dict
    events: list = field(default_factory=list)

@dataclass
class WorldTickResult:
    tick: int
    station_reports: dict[str, dict]
    events: list = field(default_factory=list)
