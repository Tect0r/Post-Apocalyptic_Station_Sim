from dataclasses import dataclass, field


@dataclass
class RouteState:
    id: str
    from_station_id: str
    to_station_id: str
    distance: int
    danger_level: int
    status: str = "open"
    modifiers: dict = field(default_factory=dict)