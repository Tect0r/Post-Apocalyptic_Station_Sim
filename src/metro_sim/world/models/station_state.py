from dataclasses import dataclass, field


@dataclass
class StationState:
    id: str
    name: str
    station_type: str
    description_key: str
    resources: dict[str, int]
    population: dict[str, int]
    stats: dict[str, int]
    pressure: dict[str, int] = field(default_factory=dict)
    faction_influence: dict[str, int] = field(default_factory=dict)
    buildings: dict = field(default_factory=dict)
    market: dict = field(default_factory=dict)