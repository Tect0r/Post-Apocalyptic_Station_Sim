from metro_sim.core.action_result import ActionResult
from metro_sim.core.game_session import GameSession
from metro_sim.market.services.market_price_service import get_station_market_prices


CURRENCY_ITEM_ID = "ammo"


def buy_market_item(
    session: GameSession,
    player_id: str,
    item_id: str,
    amount: int,
) -> ActionResult:
    if amount <= 0:
        return ActionResult(False, "invalid_amount", {"amount": amount})

    if player_id not in session.players:
        return ActionResult(False, "player_not_found", {"player_id": player_id})

    player = session.players[player_id]
    station_id = player.crew.current_location_id

    if station_id not in session.world.stations:
        return ActionResult(False, "station_not_found", {"station_id": station_id})

    station = session.world.stations[station_id]
    prices = get_station_market_prices(station, player)

    if item_id not in prices:
        return ActionResult(False, "item_not_tradeable", {"item_id": item_id})

    stock = station.market.get("stock", {}).get(item_id, 0)

    if stock < amount:
        return ActionResult(False, "not_enough_market_stock", {"item_id": item_id, "stock": stock})

    total_price = prices[item_id]["buy_price"] * amount
    player_currency = player.inventory.items.get(CURRENCY_ITEM_ID, 0)

    if player_currency < total_price:
        return ActionResult(
            False,
            "not_enough_currency",
            {
                "currency": CURRENCY_ITEM_ID,
                "required": total_price,
                "available": player_currency,
            },
        )

    player.inventory.items[CURRENCY_ITEM_ID] = player_currency - total_price
    player.inventory.items[item_id] = player.inventory.items.get(item_id, 0) + amount
    station.market["stock"][item_id] = stock - amount

    return ActionResult(
        True,
        "market_item_bought",
        {
            "station_id": station_id,
            "item_id": item_id,
            "amount": amount,
            "total_price": total_price,
            "currency": CURRENCY_ITEM_ID,
        },
    )


def sell_market_item(
    session: GameSession,
    player_id: str,
    item_id: str,
    amount: int,
) -> ActionResult:
    if amount <= 0:
        return ActionResult(False, "invalid_amount", {"amount": amount})

    if player_id not in session.players:
        return ActionResult(False, "player_not_found", {"player_id": player_id})

    if item_id == CURRENCY_ITEM_ID:
        return ActionResult(False, "cannot_sell_currency", {"item_id": item_id})

    player = session.players[player_id]
    station_id = player.crew.current_location_id

    if station_id not in session.world.stations:
        return ActionResult(False, "station_not_found", {"station_id": station_id})

    player_amount = player.inventory.items.get(item_id, 0)

    if player_amount < amount:
        return ActionResult(
            False,
            "not_enough_items",
            {
                "item_id": item_id,
                "required": amount,
                "available": player_amount,
            },
        )

    station = session.world.stations[station_id]
    prices = get_station_market_prices(station, player)

    if item_id not in prices:
        return ActionResult(False, "item_not_tradeable", {"item_id": item_id})

    total_value = prices[item_id]["sell_price"] * amount

    player.inventory.items[item_id] = player_amount - amount
    player.inventory.items[CURRENCY_ITEM_ID] = player.inventory.items.get(CURRENCY_ITEM_ID, 0) + total_value
    
    if station.market is None:
        station.market = {}
    
    station.market.setdefault("stock", {})

    station.market["stock"][item_id] = station.market["stock"].get(item_id, 0) + amount

    return ActionResult(
        True,
        "market_item_sold",
        {
            "station_id": station_id,
            "item_id": item_id,
            "amount": amount,
            "total_value": total_value,
            "currency": CURRENCY_ITEM_ID,
        },
    )