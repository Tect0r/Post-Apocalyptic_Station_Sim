from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.simulation.effect_system import apply_world_effects
from metro_sim.world.simulation.market_system import (
    calculate_item_price,
    calculate_station_item_prices,
    process_markets_tick,
)


def test_market_system_updates_item_prices_for_inhabited_station():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    station.inhabited = True
    station.market["item_prices"] = {
        "food": 10,
        "water": 8,
        "medicine": 30,
        "ammo": 20,
        "trade_goods": 15,
        "parts": 25,
    }

    effects, logs = process_markets_tick(world)
    apply_world_effects(world=world, effects=effects)

    assert station.market["item_prices"]
    assert "food" in station.market["item_prices"]
    assert "medicine" in station.market["item_prices"]
    assert any(effect.reason == "market_prices_updated" for effect in effects)
    assert len(logs) >= 1


def test_food_shortage_increases_food_price():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    station.population = 500
    station.resources["food"] = 20
    station.pressure["supply_disruption"] = 0
    station.market["activity"] = 50

    price = calculate_item_price(
        world=world,
        station_id="paveletskaya_radial",
        item_id="food",
        base_price=10,
    )

    assert price > 10


def test_high_supply_disruption_increases_prices():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    station.population = 500
    station.resources["food"] = 500
    station.pressure["supply_disruption"] = 25
    station.market["activity"] = 50

    price = calculate_item_price(
        world=world,
        station_id="paveletskaya_radial",
        item_id="food",
        base_price=10,
    )

    assert price > 10


def test_high_market_activity_stabilizes_prices():
    world = create_world()
    station = world.stations["paveletskaya_ring"]

    station.population = 500
    station.resources["food"] = 500
    station.pressure["supply_disruption"] = 0
    station.market["activity"] = 80

    price = calculate_item_price(
        world=world,
        station_id="paveletskaya_ring",
        item_id="food",
        base_price=10,
    )

    assert price <= 10


def test_market_system_skips_abandoned_station():
    world = create_world()
    station = world.stations["nagornaya"]

    station.inhabited = False
    station.market["item_prices"] = {}

    effects, logs = process_markets_tick(world)
    apply_world_effects(world=world, effects=effects)

    assert station.market["item_prices"] == {}