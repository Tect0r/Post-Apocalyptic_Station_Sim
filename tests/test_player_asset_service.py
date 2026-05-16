from metro_sim.core.game_session import create_game_session
from metro_sim.player.models.player_asset_status import PlayerAssetStatus
from metro_sim.player.services.player_asset_service import (
    add_player_asset,
    damage_player_asset,
    repair_player_asset,
    upgrade_player_asset,
)


def test_add_player_asset_to_station():
    session = create_game_session()

    result = add_player_asset(
        session=session,
        player_id="player_001",
        asset_type="storage_room",
        station_id="paveletskaya_radial",
    )

    player = session.players["player_001"]

    assert result.success is True
    assert len(player.assets) == 1
    assert player.assets[0].asset_type == "storage_room"
    assert player.assets[0].station_id == "paveletskaya_radial"
    assert player.assets[0].level == 1


def test_upgrade_player_asset_increases_level():
    session = create_game_session()

    add_result = add_player_asset(
        session=session,
        player_id="player_001",
        asset_type="storage_room",
        station_id="paveletskaya_radial",
    )

    asset_id = add_result.data["asset_id"]

    result = upgrade_player_asset(
        session=session,
        player_id="player_001",
        asset_id=asset_id,
    )

    player = session.players["player_001"]
    asset = player.assets[0]

    assert result.success is True
    assert asset.level == 2


def test_damage_player_asset_changes_condition_and_status():
    session = create_game_session()

    add_result = add_player_asset(
        session=session,
        player_id="player_001",
        asset_type="storage_room",
        station_id="paveletskaya_radial",
    )

    asset_id = add_result.data["asset_id"]

    result = damage_player_asset(
        session=session,
        player_id="player_001",
        asset_id=asset_id,
        amount=60,
    )

    player = session.players["player_001"]
    asset = player.assets[0]

    assert result.success is True
    assert asset.condition == 40
    assert asset.status == PlayerAssetStatus.DAMAGED


def test_repair_player_asset_increases_condition():
    session = create_game_session()

    add_result = add_player_asset(
        session=session,
        player_id="player_001",
        asset_type="storage_room",
        station_id="paveletskaya_radial",
    )

    asset_id = add_result.data["asset_id"]

    damage_player_asset(
        session=session,
        player_id="player_001",
        asset_id=asset_id,
        amount=60,
    )

    result = repair_player_asset(
        session=session,
        player_id="player_001",
        asset_id=asset_id,
    )

    player = session.players["player_001"]
    asset = player.assets[0]

    assert result.success is True
    assert asset.condition == 50