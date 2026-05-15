from dataclasses import dataclass, field

from metro_sim.player.models.player_asset_status import PlayerAssetStatus

@dataclass
class PlayerAsset:
    id: str
    owner_player_id: str
    name: str
    asset_type: str
    station_id: str | None = None
    route_id: str | None = None
    level: int = 1
    condition: int = 100
    status: PlayerAssetStatus = PlayerAssetStatus.ACTIVE
    effects: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)