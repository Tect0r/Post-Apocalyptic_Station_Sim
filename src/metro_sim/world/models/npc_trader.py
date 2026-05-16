from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass
class NpcTrader:
    id: str
    name: str
    current_station_id: str
    home_station_id: str

    status: str = "idle"
    target_station_id: str | None = None
    active_movement_id: str | None = None

    inventory: dict[str, int] = field(default_factory=dict)
    data: dict[str, Any] = field(default_factory=dict)


def create_npc_trader(
    *,
    name: str,
    current_station_id: str,
    home_station_id: str,
    inventory: dict[str, int] | None = None,
    data: dict[str, Any] | None = None,
) -> NpcTrader:
    return NpcTrader(
        id=str(uuid4()),
        name=name,
        current_station_id=current_station_id,
        home_station_id=home_station_id,
        inventory=inventory or {},
        data=data or {},
    )