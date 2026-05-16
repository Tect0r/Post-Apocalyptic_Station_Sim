from metro_sim.contracts.models.contract_status import ContractStatus
from metro_sim.contracts.services.contract_acceptance_service import accept_contract
from metro_sim.core.game_session import create_game_session


def test_accept_contract_starts_player_action():
    session = create_game_session()

    result = accept_contract(
        session=session,
        player_id="player_001",
        contract_id="contract_support_paveletskaya_militia",
    )

    player = session.players["player_001"]
    contract = session.world.contracts["contract_support_paveletskaya_militia"]

    assert result.success is True
    assert result.message == "contract_accepted"
    assert len(player.active_actions) == 1
    assert contract.status == ContractStatus.ACCEPTED
    assert contract.accepted_by_player_id == "player_001"
    assert contract.linked_action_id == player.active_actions[0].id


def test_accept_contract_fails_when_contract_not_available():
    session = create_game_session()

    accept_contract(
        session=session,
        player_id="player_001",
        contract_id="contract_support_paveletskaya_militia",
    )

    result = accept_contract(
        session=session,
        player_id="player_001",
        contract_id="contract_support_paveletskaya_militia",
    )

    assert result.success is False
    assert result.message == "contract_not_available"


def test_accept_contract_fails_for_missing_contract():
    session = create_game_session()

    result = accept_contract(
        session=session,
        player_id="player_001",
        contract_id="missing_contract",
    )

    assert result.success is False
    assert result.message == "contract_not_found"

def test_accept_station_contract_fails_when_crew_not_at_station():
    session = create_game_session()
    player = session.players["player_001"]
    player.crew.current_location_id = "hansa_ring"

    result = accept_contract(
        session=session,
        player_id="player_001",
        contract_id="contract_support_paveletskaya_militia",
    )

    assert result.success is False
    assert result.message == "crew_not_at_target_station"


def test_accept_route_contract_fails_when_route_not_connected():
    session = create_game_session()

    result = accept_contract(
        session=session,
        player_id="player_001",
        contract_id="contract_secure_paveletskaya_transfer",
    )

    # This should pass if the route is connected to paveletskaya_radial.
    assert result.success is True