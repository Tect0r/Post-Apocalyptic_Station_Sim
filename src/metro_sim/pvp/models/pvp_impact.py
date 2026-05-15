from dataclasses import dataclass, field

from metro_sim.pvp.models.pvp_action_type import PvPActionType


@dataclass
class PvPImpact:
    id: str
    source_player_id: str
    target_player_id: str | None
    action_type: PvPActionType
    target_type: str
    target_id: str
    created_tick: int
    effects: dict = field(default_factory=dict)
    detected: bool = False
    reputation_cost: dict = field(default_factory=dict)