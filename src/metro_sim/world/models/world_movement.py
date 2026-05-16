from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass
class WorldMovement:
    id: str
    actor_type: str
    actor_id: str

    from_station_id: str
    to_station_id: str

    station_path: list[str]
    route_path: list[str]

    started_at_tick: int
    arrives_at_tick: int

    status: str = "active"
    data: dict[str, Any] = field(default_factory=dict)


def create_world_movement(
    *,
    actor_type: str,
    actor_id: str,
    from_station_id: str,
    to_station_id: str,
    station_path: list[str],
    route_path: list[str],
    started_at_tick: int,
    arrives_at_tick: int,
    data: dict[str, Any] | None = None,
) -> WorldMovement:
    return WorldMovement(
        id=str(uuid4()),
        actor_type=actor_type,
        actor_id=actor_id,
        from_station_id=from_station_id,
        to_station_id=to_station_id,
        station_path=station_path,
        route_path=route_path,
        started_at_tick=started_at_tick,
        arrives_at_tick=arrives_at_tick,
        data=data or {},
    )