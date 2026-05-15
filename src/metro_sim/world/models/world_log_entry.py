from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass
class WorldLogEntry:
    id: str
    tick: int
    category: str
    message: str
    target_type: str | None = None
    target_id: str | None = None
    importance: str = "normal"
    data: dict[str, Any] = field(default_factory=dict)


def create_world_log_entry(
    *,
    tick: int,
    category: str,
    message: str,
    target_type: str | None = None,
    target_id: str | None = None,
    importance: str = "normal",
    data: dict[str, Any] | None = None,
) -> WorldLogEntry:
    return WorldLogEntry(
        id=str(uuid4()),
        tick=tick,
        category=category,
        message=message,
        target_type=target_type,
        target_id=target_id,
        importance=importance,
        data=data or {},
    )