from metro_sim.core.game_session import create_game_session
from metro_sim.market.services.market_trade_service import buy_market_item, sell_market_item


def test_buy_market_item_transfers_item_to_player():
    session = create_game_session()
    player = session.players["player_001"]

    ammo_before = player.inventory.items["ammo"]
    food_before = player.inventory.items["food"]

    result = buy_market_item(
        session=session,
        player_id="player_001",
        item_id="food",
        amount=2,
    )

    assert result.success is True
    assert player.inventory.items["food"] == food_before + 2
    assert player.inventory.items["ammo"] < ammo_before


def test_sell_market_item_transfers_currency_to_player():
    session = create_game_session()
    player = session.players["player_001"]

    player.inventory.items["food"] = 10
    ammo_before = player.inventory.items["ammo"]

    result = sell_market_item(
        session=session,
        player_id="player_001",
        item_id="food",
        amount=2,
    )

    assert result.success is True
    assert player.inventory.items["food"] == 8
    assert player.inventory.items["ammo"] > ammo_before


def test_buy_market_item_fails_when_not_enough_currency():
    session = create_game_session()
    player = session.players["player_001"]
    player.inventory.items["ammo"] = 0

    result = buy_market_item(
        session=session,
        player_id="player_001",
        item_id="medicine",
        amount=1,
    )

    assert result.success is False
    assert result.message == "not_enough_currency"