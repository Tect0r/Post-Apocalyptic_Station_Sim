from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.models.npc_trader import create_npc_trader
from metro_sim.world.simulation.trader_decision_service import (
    calculate_effective_risk_tolerance,
    evaluate_trader_target,
)


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