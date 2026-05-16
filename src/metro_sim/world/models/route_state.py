from dataclasses import dataclass, field


@dataclass
class RouteState:
    id: str
    from_station_id: str
    to_station_id: str
    travel_time_ticks: int
    status: str = "open"
    route_type: str = "tunnel"
    distance: int = 1
    danger: int = 0
    traffic: int = 0
    condition: int = 100
    modifiers: str | None = None
    control: dict[str, int] = field(default_factory=dict)
    pressure: dict = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)