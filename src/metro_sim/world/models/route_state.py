from dataclasses import dataclass, field


@dataclass
class RouteState:
    id: str
    from_station_id: str
    to_station_id: str
    distance: int = 1
    travel_time_ticks: int = 60
    status: str = "open"
    danger_level: int = 0
    traffic: int = 0
    condition: int = 100
    modifiers: dict = field(default_factory=dict)
    control: dict[str, int] = field(default_factory=dict)
    pressure: dict[str, int] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)