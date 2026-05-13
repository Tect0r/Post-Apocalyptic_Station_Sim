from dataclasses import dataclass, field


@dataclass
class StationState:
    id: str
    name: str
    resources: dict
    population: dict
    stats: dict
    buildings: dict
    time: dict
    power: dict = field(default_factory=dict)
    water_system: dict = field(default_factory=dict)
    maintenance: dict = field(default_factory=dict)
    pressure: dict = field(default_factory=dict)
    faction_influence: dict = field(default_factory=dict)