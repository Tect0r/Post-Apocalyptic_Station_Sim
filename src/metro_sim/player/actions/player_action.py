from dataclasses import dataclass, field
from typing import Any

from metro_sim.player.actions.player_action_type import PlayerActionType


@dataclass
class PlayerAction:
    type: PlayerActionType
    player_id: str
    target_id: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)