from dataclasses import dataclass, field
from typing import Any

from metro_sim.player.actions.player_action_type import PlayerActionType


@dataclass
class PlayerAction:
    id: str
    player_id: str
    action_type: PlayerActionType
    target_type: str
    target_id: str
    started_tick: int
    duration_ticks: int
    status: str = "active"
    payload: dict[str, Any] = field(default_factory=dict)

    @property
    def completes_at_tick(self) -> int:
        return self.started_tick + self.duration_ticks