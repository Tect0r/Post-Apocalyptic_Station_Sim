from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass
class WorldSnapshot:
    id: str
    tick: int
    stations: dict[str, Any] = field(default_factory=dict)
    routes: dict[str, Any] = field(default_factory=dict)
    factions: dict[str, Any] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)


def create_world_snapshot(
    *,
    tick: int,
    stations: dict[str, Any],
    routes: dict[str, Any],
    factions: dict[str, Any],
    events: list[dict[str, Any]],
) -> WorldSnapshot:
    return WorldSnapshot(
        id=str(uuid4()),
        tick=tick,
        stations=stations,
        routes=routes,
        factions=factions,
        events=events,
    )