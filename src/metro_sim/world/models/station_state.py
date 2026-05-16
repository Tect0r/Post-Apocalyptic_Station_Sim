from dataclasses import dataclass, field


@dataclass
class StationState:
    id: str
    name: str
    population: int
    resources: dict
    stats: dict
    pressure: dict
    faction_influence: dict

    complex_id: str | None = None
    line: str | None = None
    station_type: str = "station"
    inhabited: bool = True
    ui: dict = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    market: dict = field(default_factory=dict)
    description_key: str | None = None