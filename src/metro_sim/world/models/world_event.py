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

    duration_ticks: int = 0
    ends_at_tick: int | None = None
    current_phase: str | None = None


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
    duration_ticks: int = 0,
    current_phase: str | None = None,
) -> WorldEvent:
    ends_at_tick = None

    if duration_ticks > 0:
        ends_at_tick = started_at_tick + duration_ticks

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
        duration_ticks=duration_ticks,
        ends_at_tick=ends_at_tick,
        current_phase=current_phase,
    )