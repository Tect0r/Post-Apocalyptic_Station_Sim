from uuid import uuid4

from metro_sim.player.models.player_asset import PlayerAsset
from metro_sim.player.models.player_asset_status import PlayerAssetStatus


def create_player_asset(
    owner_player_id: str,
    asset_type: str,
    asset_definition: dict,
    station_id: str | None = None,
    route_id: str | None = None,
    metadata: dict | None = None,
) -> PlayerAsset:
    level = 1
    effects_by_level = asset_definition.get("effects_by_level", {})

    return PlayerAsset(
        id=str(uuid4()),
        owner_player_id=owner_player_id,
        name=asset_definition["label"],
        asset_type=asset_type,
        station_id=station_id,
        route_id=route_id,
        level=level,
        condition=asset_definition.get("base_condition", 100),
        status=PlayerAssetStatus.ACTIVE,
        effects=effects_by_level.get(str(level), {}),
        metadata=metadata or {},
    )