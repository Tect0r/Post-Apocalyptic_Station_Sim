from metro_sim.core.game_session import advance_tick, create_game_session
from metro_sim.contracts.services.contract_acceptance_service import accept_contract
from metro_sim.world.simulation.tick_orchestrator import process_world_tick


def test_simulation_tick_completes_contract_and_creates_player_asset():
    session = create_game_session()
    player = session.players["player_001"]

    # Player muss an der Hansa-/Ring-Seite sein, weil der Storage-Contract dort liegt.
    player.crew.current_location_id = "paveletskaya_ring"

    result = accept_contract(
        session=session,
        player_id="player_001",
        contract_id="contract_rent_paveletskaya_storage",
    )

    assert result.success is True
    assert len(player.active_actions) == 1

    action = player.active_actions[0]

    while session.world.current_tick < action.completes_at_tick:
        advance_tick(session)

    assert len(player.assets) == 1
    assert player.assets[0].asset_type == "storage_room"
    assert player.assets[0].station_id == "paveletskaya_ring"


def test_pure_world_tick_does_not_complete_player_contracts():
    session = create_game_session()
    player = session.players["player_001"]

    player.crew.current_location_id = "paveletskaya_ring"

    result = accept_contract(
        session=session,
        player_id="player_001",
        contract_id="contract_rent_paveletskaya_storage",
    )

    assert result.success is True

    action = player.active_actions[0]

    while session.world.current_tick < action.completes_at_tick:
        process_world_tick(session.world)

    assert len(player.assets) == 0
    assert len(player.active_actions) == 1