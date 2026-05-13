from dataclasses import dataclass, field


@dataclass
class FactionState:
    id: str
    name: str
    resources: dict = field(default_factory=dict)
    relations: dict = field(default_factory=dict)
    controlled_stations: list[str] = field(default_factory=list)