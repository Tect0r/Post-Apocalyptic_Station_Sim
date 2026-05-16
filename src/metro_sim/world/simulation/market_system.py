from metro_sim.world.models.world_effect import WorldEffect
from metro_sim.world.models.world_log_entry import WorldLogEntry, create_world_log_entry
from metro_sim.world.models.world_state import WorldState


BASE_ITEM_PRICES: dict[str, int] = {
    "food": 10,
    "water": 8,
    "medicine": 30,
    "ammo": 20,
    "trade_goods": 15,
    "parts": 25,
}


RESOURCE_KEYS = {
    "food",
    "water",
    "medicine",
    "ammo",
    "trade_goods",
    "parts",
}


def process_markets_tick(world: WorldState) -> tuple[list[WorldEffect], list[WorldLogEntry]]:
    effects: list[WorldEffect] = []
    logs: list[WorldLogEntry] = []

    for station_id, station in world.stations.items():
        station.id = station_id

        if not station.inhabited:
            continue

        station_effects, station_logs = process_station_market_tick(
            world=world,
            station_id=station_id,
        )

        effects.extend(station_effects)
        logs.extend(station_logs)

    return effects, logs


def process_station_market_tick(
    *,
    world: WorldState,
    station_id: str,
) -> tuple[list[WorldEffect], list[WorldLogEntry]]:
    station = world.stations[station_id]

    current_market = station.market or {}
    current_prices = current_market.get("item_prices", {})

    new_prices = calculate_station_item_prices(
        station_id=station_id,
        world=world,
    )

    effects = [
        WorldEffect(
            target_type="station",
            target_id=station_id,
            field_path=["market", "item_prices"],
            operation="set",
            value=new_prices,
            reason="market_prices_updated",
            source="market_system",
            importance="debug",
        )
    ]

    logs = [
        create_world_log_entry(
            tick=world.current_tick,
            category="market_processed",
            message=f"Market prices updated for {station_id}.",
            target_type="station",
            target_id=station_id,
            importance="debug",
            data={
                "old_prices": current_prices,
                "new_prices": new_prices,
            },
        )
    ]

    return effects, logs


def calculate_station_item_prices(
    *,
    station_id: str,
    world: WorldState,
) -> dict[str, int]:
    station = world.stations[station_id]

    prices: dict[str, int] = {}

    for item_id, base_price in BASE_ITEM_PRICES.items():
        prices[item_id] = calculate_item_price(
            world=world,
            station_id=station_id,
            item_id=item_id,
            base_price=base_price,
        )

    return prices


def calculate_item_price(
    *,
    world: WorldState,
    station_id: str,
    item_id: str,
    base_price: int,
) -> int:
    station = world.stations[station_id]

    population = max(1, int(station.population))
    stock = int(station.resources.get(item_id, 0))

    shortage_multiplier = calculate_shortage_multiplier(
        item_id=item_id,
        stock=stock,
        population=population,
    )

    pressure_multiplier = calculate_pressure_multiplier(
        station_pressure=station.pressure,
        item_id=item_id,
    )

    market_activity_multiplier = calculate_market_activity_multiplier(
        station_market=station.market,
    )

    price = base_price * shortage_multiplier * pressure_multiplier * market_activity_multiplier

    return max(1, int(round(price)))


def calculate_shortage_multiplier(
    *,
    item_id: str,
    stock: int,
    population: int,
) -> float:
    # For non-essential trade goods, do not scale as aggressively with population.
    if item_id == "trade_goods":
        if stock <= 5:
            return 1.4
        if stock >= 80:
            return 0.9
        return 1.0

    if item_id == "parts":
        if stock <= 3:
            return 1.5
        if stock >= 50:
            return 0.9
        return 1.0

    stock_per_100_people = stock / max(1, population / 100)

    thresholds = {
        "food": (20, 40),
        "water": (20, 40),
        "medicine": (2, 6),
        "ammo": (5, 15),
    }

    low_threshold, comfortable_threshold = thresholds.get(item_id, (10, 30))

    if stock_per_100_people < low_threshold:
        return 1.8

    if stock_per_100_people < comfortable_threshold:
        return 1.3

    return 1.0


def calculate_pressure_multiplier(
    *,
    station_pressure: dict,
    item_id: str,
) -> float:
    supply_disruption = int(station_pressure.get("supply_disruption", 0))
    danger = int(station_pressure.get("danger", 0))
    security_risk = int(station_pressure.get("security_risk", 0))
    unrest = int(station_pressure.get("unrest", 0))

    multiplier = 1.0

    if supply_disruption >= 20:
        multiplier += 0.25
    elif supply_disruption >= 10:
        multiplier += 0.10

    if item_id in {"ammo", "medicine"}:
        if danger >= 20:
            multiplier += 0.20
        if security_risk >= 20:
            multiplier += 0.15

    if item_id in {"food", "water"}:
        if unrest >= 20:
            multiplier += 0.10

    return multiplier


def calculate_market_activity_multiplier(
    *,
    station_market: dict,
) -> float:
    activity = int(station_market.get("activity", 0))

    if activity >= 70:
        return 0.95

    if activity <= 20:
        return 1.10

    return 1.0