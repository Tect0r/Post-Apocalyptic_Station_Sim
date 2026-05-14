from dataclasses import dataclass, field
from typing import Any


@dataclass
class WorldEvent:
    id: str
    tick: int
    station_id: str | None
    event_type: str
    severity: int
    description_key: str
    effects: dict[str, Any] = field(default_factory=dict)
    source: str = "world"