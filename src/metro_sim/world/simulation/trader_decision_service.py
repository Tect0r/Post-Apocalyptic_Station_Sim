from dataclasses import dataclass

from metro_sim.world.models.npc_trader import NpcTrader
from metro_sim.world.models.world_state import WorldState
from metro_sim.world.services.pathfinding_service import find_station_path


@dataclass
class TraderTargetEvaluation:
    station_id: str
    success: bool
    expected_profit: int
    route_risk: int
    travel_time_ticks: int
    effective_risk_tolerance: int
    score: int
    error: str | None = None


def evaluate_trader_target(
    *,
    world: WorldState,
    trader: NpcTrader,
    target_station_id: str,
) -> TraderTargetEvaluation:
    path_result = find_station_path(
        world=world,
        from_station_id=trader.current_station_id,
        to_station_id=target_station_id,
    )

    if not path_result.success:
        return TraderTargetEvaluation(
            station_id=target_station_id,
            success=False,
            expected_profit=0,
            route_risk=0,
            travel_time_ticks=0,
            effective_risk_tolerance=0,
            score=-9999,
            error=path_result.error,
        )

    expected_profit = get_expected_profit(
        trader=trader,
        target_station_id=target_station_id,
    )

    route_risk = calculate_route_risk(
        world=world,
        route_ids=path_result.route_ids,
        trader=trader,
    )

    effective_risk_tolerance = calculate_effective_risk_tolerance(
        trader=trader,
        expected_profit=expected_profit,
    )

    if route_risk > effective_risk_tolerance:
        return TraderTargetEvaluation(
            station_id=target_station_id,
            success=False,
            expected_profit=expected_profit,
            route_risk=route_risk,
            travel_time_ticks=path_result.total_travel_time_ticks,
            effective_risk_tolerance=effective_risk_tolerance,
            score=-9999,
            error="route_too_risky",
        )

    score = calculate_target_score(
        expected_profit=expected_profit,
        route_risk=route_risk,
        travel_time_ticks=path_result.total_travel_time_ticks,
    )

    return TraderTargetEvaluation(
        station_id=target_station_id,
        success=True,
        expected_profit=expected_profit,
        route_risk=route_risk,
        travel_time_ticks=path_result.total_travel_time_ticks,
        effective_risk_tolerance=effective_risk_tolerance,
        score=score,
    )


def get_expected_profit(
    *,
    trader: NpcTrader,
    target_station_id: str,
) -> int:
    known_market_profit = trader.data.get("known_market_profit", {})
    return int(known_market_profit.get(target_station_id, 0))


def calculate_route_risk(
    *,
    world: WorldState,
    route_ids: list[str],
    trader: NpcTrader | None = None,
) -> int:
    if not route_ids:
        return 0

    total_risk = 0

    for route_id in route_ids:
        route = world.routes[route_id]

        route_risk = route.danger
        route_risk += max(0, 100 - route.condition) // 2
        route_risk += calculate_faction_route_risk_modifier(
            trader=trader,
            route_control=route.control,
        )

        route_risk = max(0, route_risk)
        total_risk += route_risk

    return total_risk // len(route_ids)


def calculate_effective_risk_tolerance(
    *,
    trader: NpcTrader,
    expected_profit: int,
) -> int:
    base_risk_tolerance = int(
        trader.data.get(
            "base_risk_tolerance",
            trader.data.get("risk_tolerance", 30),
        )
    )

    max_risk_tolerance = int(trader.data.get("max_risk_tolerance", 80))
    profit_risk_factor = float(trader.data.get("profit_risk_factor", 0.0))

    effective_risk_tolerance = int(
        base_risk_tolerance + expected_profit * profit_risk_factor
    )

    return min(max_risk_tolerance, effective_risk_tolerance)


def calculate_target_score(
    *,
    expected_profit: int,
    route_risk: int,
    travel_time_ticks: int,
) -> int:
    travel_penalty = travel_time_ticks // 20

    return expected_profit - route_risk - travel_penalty

def evaluation_to_dict(evaluation: TraderTargetEvaluation) -> dict:
    return {
        "station_id": evaluation.station_id,
        "success": evaluation.success,
        "expected_profit": evaluation.expected_profit,
        "route_risk": evaluation.route_risk,
        "travel_time_ticks": evaluation.travel_time_ticks,
        "effective_risk_tolerance": evaluation.effective_risk_tolerance,
        "score": evaluation.score,
        "error": evaluation.error,
    }

def calculate_faction_route_risk_modifier(
    *,
    trader: NpcTrader | None,
    route_control: dict[str, int],
) -> int:
    if trader is None:
        return 0

    trader_faction_id = trader.data.get("faction_id")

    if trader_faction_id is None:
        return 0

    modifier = 0

    own_control = route_control.get(trader_faction_id, 0)
    bandit_control = route_control.get("bandits", 0)
    hansa_control = route_control.get("hansa", 0)
    polis_control = route_control.get("polis", 0)

    # Own faction controls the route: safer for this trader.
    if own_control >= 50:
        modifier -= 15
    elif own_control >= 25:
        modifier -= 8

    # Bandit control is dangerous for most traders,
    # but less dangerous for bandit traders.
    if bandit_control >= 40 and trader_faction_id != "bandits":
        modifier += 20
    elif bandit_control >= 40 and trader_faction_id == "bandits":
        modifier -= 10

    # Hansa-controlled routes are safer for Hansa and somewhat safer for independents.
    if hansa_control >= 60:
        if trader_faction_id == "hansa":
            modifier -= 12
        elif trader_faction_id == "independent":
            modifier -= 4
        elif trader_faction_id == "bandits":
            modifier += 10

    # Polis control increases safety for Polis and independents, but not for bandits.
    if polis_control >= 50:
        if trader_faction_id == "polis":
            modifier -= 12
        elif trader_faction_id == "independent":
            modifier -= 5
        elif trader_faction_id == "bandits":
            modifier += 10

    return modifier