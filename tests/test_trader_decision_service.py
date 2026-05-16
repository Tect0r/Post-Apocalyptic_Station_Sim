from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.models.npc_trader import create_npc_trader
from metro_sim.world.simulation.trader_decision_service import (
    calculate_effective_risk_tolerance,
    calculate_route_risk,
    evaluate_trader_target,
)

def test_hansa_trader_has_lower_risk_on_hansa_controlled_route():
    world = create_world()

    route = world.routes["route_paveletskaya_ring_radial"]
    route.danger = 30
    route.condition = 100
    route.control["hansa"] = 80
    route.control["bandits"] = 0

    trader = create_npc_trader(
        name="Hansa Trader",
        current_station_id="paveletskaya_ring",
        home_station_id="paveletskaya_ring",
        data={
            "faction_id": "hansa"
        },
    )

    risk = calculate_route_risk(
        world=world,
        route_ids=["route_paveletskaya_ring_radial"],
        trader=trader,
    )

    assert risk < 30

def test_hansa_trader_has_higher_risk_on_bandit_controlled_route():
    world = create_world()

    route = world.routes["route_paveletskaya_ring_radial"]
    route.danger = 30
    route.condition = 100
    route.control["hansa"] = 0
    route.control["bandits"] = 80

    trader = create_npc_trader(
        name="Hansa Trader",
        current_station_id="paveletskaya_ring",
        home_station_id="paveletskaya_ring",
        data={
            "faction_id": "hansa"
        },
    )

    risk = calculate_route_risk(
        world=world,
        route_ids=["route_paveletskaya_ring_radial"],
        trader=trader,
    )

    assert risk > 30
    
def test_bandit_trader_has_lower_risk_on_bandit_controlled_route():
    world = create_world()

    route = world.routes["route_paveletskaya_ring_radial"]
    route.danger = 30
    route.condition = 100
    route.control["hansa"] = 0
    route.control["bandits"] = 80

    trader = create_npc_trader(
        name="Bandit Trader",
        current_station_id="paveletskaya_ring",
        home_station_id="paveletskaya_ring",
        data={
            "faction_id": "bandits"
        },
    )

    risk = calculate_route_risk(
        world=world,
        route_ids=["route_paveletskaya_ring_radial"],
        trader=trader,
    )

    assert risk < 30

def test_expected_profit_increases_effective_risk_tolerance():
    trader = create_npc_trader(
        name="Test Trader",
        current_station_id="paveletskaya_ring",
        home_station_id="paveletskaya_ring",
        data={
            "base_risk_tolerance": 30,
            "max_risk_tolerance": 80,
            "profit_risk_factor": 0.5,
        },
    )

    risk_tolerance = calculate_effective_risk_tolerance(
        trader=trader,
        expected_profit=40,
    )

    assert risk_tolerance == 50


def test_effective_risk_tolerance_is_capped():
    trader = create_npc_trader(
        name="Test Trader",
        current_station_id="paveletskaya_ring",
        home_station_id="paveletskaya_ring",
        data={
            "base_risk_tolerance": 30,
            "max_risk_tolerance": 60,
            "profit_risk_factor": 1.0,
        },
    )

    risk_tolerance = calculate_effective_risk_tolerance(
        trader=trader,
        expected_profit=100,
    )

    assert risk_tolerance == 60


def test_trader_target_evaluation_succeeds_for_reachable_profitable_target():
    world = create_world()

    trader = create_npc_trader(
        name="Test Trader",
        current_station_id="paveletskaya_ring",
        home_station_id="paveletskaya_ring",
        data={
            "base_risk_tolerance": 80,
            "max_risk_tolerance": 100,
            "profit_risk_factor": 0.2,
            "known_market_profit": {
                "paveletskaya_radial": 20
            }
        },
    )

    evaluation = evaluate_trader_target(
        world=world,
        trader=trader,
        target_station_id="paveletskaya_radial",
    )

    assert evaluation.success is True
    assert evaluation.expected_profit == 20
    assert evaluation.travel_time_ticks > 0