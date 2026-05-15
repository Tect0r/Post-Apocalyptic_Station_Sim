from metro_sim.contracts.services.contract_acceptance_service import accept_contract
from metro_sim.core.game_session import advance_tick, create_game_session


def test_contract_completion_creates_player_asset():
    session = create_game_session()
    player = session.players["player_001"]

    result = accept_contract(
        session=session,
        player_id="player_001",
        contract_id="contract_rent_paveletskaya_storage",
    )

    assert result.success is True

    action = player.active_actions[0]

    while session.world.current_tick < action.completes_at_tick:
        advance_tick(session)

    assert len(player.assets) == 1
    assert player.assets[0].asset_type == "storage_room"
    assert player.assets[0].station_id == "paveletskaya"