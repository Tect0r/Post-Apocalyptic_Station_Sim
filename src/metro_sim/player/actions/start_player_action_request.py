from dataclasses import dataclass

from metro_sim.player.actions.player_action_type import PlayerActionType


@dataclass
class StartPlayerActionRequest:
    player_id: str
    action_type: PlayerActionType
    target_id: str