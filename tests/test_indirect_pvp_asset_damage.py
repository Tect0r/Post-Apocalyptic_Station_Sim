from metro_sim.core.game_session import create_game_session
from metro_sim.player.factories.player_factory import create_initial_player
from metro_sim.player.services.player_asset_service import add_player_asset
from metro_sim.pvp.services.asset_pvp_service import damage_player_asset_indirectly


def test_player_can_damage_other_player_asset_indirectly():
    session = create_game_session()

    target_player = create_initial_player(
        player_id="player_002",
        name="Target Player",
    )
    session.players[target_player.id] = target_player

    add_result = add_player_asset(
        session=session,
        player_id="player_002",
        asset_type="storage_room",
        station_id="paveletskaya_radial",
    )

    asset_id = add_result.data["asset_id"]
    asset = session.players["player_002"].assets[0]

    result = damage_player_asset_indirectly(
        session=session,
        source_player_id="player_001",
        target_player_id="player_002",
        asset_id=asset_id,
        amount=10,
    )

    assert result.success is True
    assert asset.condition == 90
    assert len(session.world.pvp_impacts) == 1


def test_player_cannot_damage_own_asset_indirectly():
    session = create_game_session()

    add_result = add_player_asset(
        session=session,
        player_id="player_001",
        asset_type="storage_room",
        station_id="paveletskaya_radial",
    )

    result = damage_player_asset_indirectly(
        session=session,
        source_player_id="player_001",
        target_player_id="player_001",
        asset_id=add_result.data["asset_id"],
        amount=10,
    )

    assert result.success is False
    assert result.message == "cannot_target_self"