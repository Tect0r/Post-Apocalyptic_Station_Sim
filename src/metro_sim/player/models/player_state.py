from dataclasses import dataclass, field

from metro_sim.player.models.crew_state import CrewState
from metro_sim.player.models.inventory_state import InventoryState
from metro_sim.player.models.player_asset import PlayerAsset
from metro_sim.player.models.reputation_state import ReputationState


@dataclass
class PlayerState:
    id: str
    name: str
    crew: CrewState
    inventory: InventoryState
    reputation: ReputationState
    assets: list[PlayerAsset] = field(default_factory=list)
    active_actions: list = field(default_factory=list)