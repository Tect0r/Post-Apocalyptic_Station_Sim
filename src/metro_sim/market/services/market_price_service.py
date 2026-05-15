from metro_sim.player.models.player_state import PlayerState
from metro_sim.utils.file_loader import load_market_items_data
from metro_sim.world.models.station_state import StationState


def get_station_market_prices(
    station: StationState,
    player: PlayerState | None = None,
) -> dict:
    market_items = load_market_items_data()
    price_modifiers = station.market.get("price_modifiers", {})

    prices = {}

    for item_id, item_data in market_items.items():
        if not item_data.get("tradeable", False):
            continue

        modifier = price_modifiers.get(item_id, 1.0)
        asset_modifier = get_player_asset_price_modifier(player, station.id)

        buy_price = round(item_data["base_buy_price"] * modifier * asset_modifier)
        sell_price = round(item_data["base_sell_price"] * modifier * asset_modifier)

        prices[item_id] = {
            "item_id": item_id,
            "label": item_data["label"],
            "category": item_data["category"],
            "buy_price": max(1, buy_price),
            "sell_price": max(1, sell_price),
            "stock": station.market.get("stock", {}).get(item_id, 0),
        }

    return prices


def get_player_asset_price_modifier(
    player: PlayerState | None,
    station_id: str,
) -> float:
    if player is None:
        return 1.0

    trade_bonus = 0

    for asset in player.assets:
        if asset.station_id != station_id:
            continue

        if asset.status != "active" and getattr(asset.status, "value", asset.status) != "active":
            continue

        trade_bonus += asset.effects.get("trade_bonus", 0)

    if trade_bonus <= 0:
        return 1.0

    return max(0.75, 1.0 - (trade_bonus / 100))