from dataclasses import dataclass, field


@dataclass
class RouteState:
    id: str
    from_station_id: str
    to_station_id: str
    distance: int
    danger_level: int
    travel_time_ticks: int
    status: str = "open"
    control: dict[str, int] = field(default_factory=dict)
    modifiers: dict = field(default_factory=dict)