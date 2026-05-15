from metro_sim.core.game_session import advance_tick, create_game_session
from metro_sim.persistence.load_game_service import load_game_session
from metro_sim.persistence.save_game_service import save_game_session
from metro_sim.player.actions.player_action_type import PlayerActionType
from metro_sim.player.actions.start_player_action_request import StartPlayerActionRequest
from metro_sim.player.services.player_action_service import start_player_action
from metro_sim.player.actions.player_action_status import PlayerActionStatus
from metro_sim.player.services.player_action_cancel_service import cancel_player_action
from metro_sim.contracts.models.contract_status import ContractStatus
from metro_sim.contracts.services.contract_acceptance_service import accept_contract
from metro_sim.player.services.crew_movement_service import start_crew_movement
from metro_sim.player.services.player_asset_service import add_player_asset
from metro_sim.market.services.market_trade_service import buy_market_item
from metro_sim.pvp.services.station_pressure_pvp_service import influence_station_pressure


def test_save_and_load_preserves_pvp_impacts():
    session = create_game_session()

    influence_station_pressure(
        session=session,
        source_player_id="player_001",
        station_id="paveletskaya",
        pressure_key="sabotage",
        amount=5,
    )

    save_game_session(session, "test_pvp_impacts")
    loaded_session = load_game_session("test_pvp_impacts")

    assert len(loaded_session.world.pvp_impacts) == 1
    assert loaded_session.world.pvp_impacts[0].source_player_id == "player_001"
    assert loaded_session.world.pvp_impacts[0].target_id == "paveletskaya"

def test_save_and_load_game_session_roundtrip():
    session = create_game_session()

    advance_tick(session)
    save_game_session(session, "test_roundtrip")

    loaded_session = load_game_session("test_roundtrip")

    assert loaded_session.world.current_tick == session.world.current_tick
    assert loaded_session.world.stations.keys() == session.world.stations.keys()
    assert loaded_session.world.routes.keys() == session.world.routes.keys()
    assert loaded_session.world.factions.keys() == session.world.factions.keys()
    assert loaded_session.players.keys() == session.players.keys()

def test_save_and_load_preserves_active_actions():
    session = create_game_session()

    result = start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.SUPPORT_MILITIA,
            target_id="paveletskaya",
        ),
    )

    assert result.success is True

    save_game_session(session, "test_active_action")
    loaded_session = load_game_session("test_active_action")

    loaded_player = loaded_session.players["player_001"]

    assert len(loaded_player.active_actions) == 1
    assert loaded_player.active_actions[0].action_type == PlayerActionType.SUPPORT_MILITIA
    assert loaded_player.active_actions[0].target_id == "paveletskaya"

def test_save_and_load_preserves_world_events():
    session = create_game_session()
    station = session.world.stations["paveletskaya"]
    station.pressure["militia_support"] = 25

    advance_tick(session)

    assert len(session.world.events) >= 1

    save_game_session(session, "test_events")
    loaded_session = load_game_session("test_events")

    assert len(loaded_session.world.events) == len(session.world.events)
    assert loaded_session.world.events[0].event_type == session.world.events[0].event_type

def test_save_and_load_preserves_player_assets():
    session = create_game_session()

    result = start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.RENT_STORAGE,
            target_id="paveletskaya",
        ),
    )

    for _ in range(result.data["duration_ticks"]):
        advance_tick(session)

    player = session.players["player_001"]
    assert len(player.assets) == 1

    save_game_session(session, "test_assets")
    loaded_session = load_game_session("test_assets")

    loaded_player = loaded_session.players["player_001"]

    assert len(loaded_player.assets) == 1
    assert loaded_player.assets[0].asset_type == "storage_room"
    assert loaded_player.assets[0].station_id == "paveletskaya"


def test_save_and_load_preserves_completed_actions():
    session = create_game_session()

    start_result = start_player_action(
        session,
        StartPlayerActionRequest(
            player_id="player_001",
            action_type=PlayerActionType.SUPPORT_MILITIA,
            target_id="paveletskaya",
        ),
    )

    cancel_player_action(
        session=session,
        player_id="player_001",
        action_id=start_result.data["action_id"],
    )

    save_game_session(session, "test_completed_actions")
    loaded_session = load_game_session("test_completed_actions")

    loaded_player = loaded_session.players["player_001"]

    assert len(loaded_player.completed_actions) == 1
    assert loaded_player.completed_actions[0].status == PlayerActionStatus.CANCELLED

def test_save_and_load_preserves_contract_state():
    session = create_game_session()

    accept_contract(
        session=session,
        player_id="player_001",
        contract_id="contract_support_paveletskaya_militia",
    )

    save_game_session(session, "test_contract_state")
    loaded_session = load_game_session("test_contract_state")

    contract = loaded_session.world.contracts["contract_support_paveletskaya_militia"]

    assert contract.status == ContractStatus.ACCEPTED
    assert contract.accepted_by_player_id == "player_001"
    assert contract.linked_action_id is not None

def test_save_and_load_preserves_crew_movement_state():
    session = create_game_session()

    start_crew_movement(
        session=session,
        player_id="player_001",
        route_id="route_paveletskaya_hansa_ring",
    )

    save_game_session(session, "test_crew_movement")
    loaded_session = load_game_session("test_crew_movement")

    loaded_player = loaded_session.players["player_001"]

    assert loaded_player.crew.current_location_id == "paveletskaya"
    assert loaded_player.crew.destination_location_id == "hansa_ring"
    assert loaded_player.crew.is_traveling is True
    assert len(loaded_player.active_actions) == 1

def test_save_and_load_preserves_crew_members():
    session = create_game_session()
    player = session.players["player_001"]

    save_game_session(session, "test_crew_members")
    loaded_session = load_game_session("test_crew_members")
    loaded_player = loaded_session.players["player_001"]

    assert len(loaded_player.crew.crew_members) == len(player.crew.crew_members)
    assert loaded_player.crew.crew_members[0].id == player.crew.crew_members[0].id
    assert loaded_player.crew.crew_members[0].skills == player.crew.crew_members[0].skills


def test_save_and_load_preserves_expanded_player_assets():
    session = create_game_session()

    add_player_asset(
        session=session,
        player_id="player_001",
        asset_type="storage_room",
        station_id="paveletskaya",
    )

    save_game_session(session, "test_expanded_assets")
    loaded_session = load_game_session("test_expanded_assets")

    loaded_player = loaded_session.players["player_001"]
    asset = loaded_player.assets[0]

    assert asset.owner_player_id == "player_001"
    assert asset.asset_type == "storage_room"
    assert asset.station_id == "paveletskaya"
    assert asset.route_id is None
    assert asset.level == 1
    assert asset.condition == 100

def test_save_and_load_preserves_market_stock_after_trade():
    session = create_game_session()
    station = session.world.stations["paveletskaya"]

    stock_before = station.market["stock"]["food"]

    buy_market_item(
        session=session,
        player_id="player_001",
        item_id="food",
        amount=2,
    )

    save_game_session(session, "test_market_stock")
    loaded_session = load_game_session("test_market_stock")

    loaded_station = loaded_session.world.stations["paveletskaya"]

    assert loaded_station.market["stock"]["food"] == stock_before - 2