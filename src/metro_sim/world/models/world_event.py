from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass
class WorldEvent:
    id: str
    event_type: str
    target_type: str
    target_id: str
    started_at_tick: int
    status: str = "completed"
    severity: int = 1
    causes: list[str] = field(default_factory=list)
    data: dict[str, Any] = field(default_factory=dict)


def create_world_event(
    *,
    event_type: str,
    target_type: str,
    target_id: str,
    started_at_tick: int,
    severity: int = 1,
    causes: list[str] | None = None,
    data: dict[str, Any] | None = None,
    status: str = "completed",
) -> WorldEvent:
    return WorldEvent(
        id=str(uuid4()),
        event_type=event_type,
        target_type=target_type,
        target_id=target_id,
        started_at_tick=started_at_tick,
        status=status,
        severity=severity,
        causes=causes or [],
        data=data or {},
    )