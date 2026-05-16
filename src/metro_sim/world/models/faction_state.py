from dataclasses import dataclass, field


@dataclass
class FactionState:
    id: str
    name: str
    resources: dict[str, int] = field(default_factory=dict)
    relations: dict[str, int] = field(default_factory=dict)
    controlled_stations: list[str] = field(default_factory=list)
    type: str = "generic"  
    tags: list[str] = field(default_factory=list)