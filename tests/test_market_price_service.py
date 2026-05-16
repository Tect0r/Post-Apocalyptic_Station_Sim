from metro_sim.market.services.market_price_service import get_station_market_prices
from metro_sim.world.factories.world_factory import create_world


def test_station_market_prices_include_tradeable_items():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    prices = get_station_market_prices(station)

    assert "food" in prices
    assert "water" in prices
    assert "medicine" in prices
    assert prices["food"]["buy_price"] > 0
    assert prices["food"]["sell_price"] > 0


def test_station_market_prices_include_stock():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    prices = get_station_market_prices(station)

    assert "stock" in prices["food"]