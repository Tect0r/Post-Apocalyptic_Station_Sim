from metro_sim.core.action_result import ActionResult
from metro_sim.core.game_session import GameSession
from metro_sim.pvp.models.pvp_action_type import PvPActionType
from metro_sim.pvp.services.pvp_cooldown_service import is_pvp_action_on_cooldown
from metro_sim.pvp.services.pvp_detection_service import roll_detection
from metro_sim.pvp.services.pvp_impact_service import add_pvp_impact
from metro_sim.utils.file_loader import load_pvp_rules_data
from metro_sim.world.services.pressure_service import add_station_pressure, reduce_station_pressure


def influence_station_pressure(
    session: GameSession,
    source_player_id: str,
    station_id: str,
    pressure_key: str,
    amount: int,
) -> ActionResult:
    if source_player_id not in session.players:
        return ActionResult(False, "player_not_found", {"player_id": source_player_id})

    if station_id not in session.world.stations:
        return ActionResult(False, "station_not_found", {"station_id": station_id})

    rules = load_pvp_rules_data()["pressure_station"]
    max_change = rules["max_pressure_change"]
    cooldown_ticks = rules["cooldown_ticks"]

    amount = max(-max_change, min(max_change, amount))

    if amount == 0:
        return ActionResult(False, "invalid_pressure_change", {"amount": amount})

    if is_pvp_action_on_cooldown(
        world=session.world,
        source_player_id=source_player_id,
        action_type=PvPActionType.PRESSURE_STATION,
        target_type="station",
        target_id=station_id,
        cooldown_ticks=cooldown_ticks,
    ):
        return ActionResult(False, "pvp_action_on_cooldown", {"station_id": station_id})

    station = session.world.stations[station_id]

    if amount > 0:
        add_station_pressure(station, pressure_key, amount)
    else:
        reduce_station_pressure(station, pressure_key, abs(amount))

    detected = roll_detection(rules.get("detection_chance", 0))

    impact = add_pvp_impact(
        world=session.world,
        source_player_id=source_player_id,
        action_type=PvPActionType.PRESSURE_STATION,
        target_type="station",
        target_id=station_id,
        effects={
            "pressure": {
                pressure_key: amount
            }
        },
        detected=detected,
        reputation_cost=rules.get("reputation_cost", {}),
    )

    return ActionResult(
        True,
        "station_pressure_influenced",
        {
            "impact_id": impact.id,
            "station_id": station_id,
            "pressure_key": pressure_key,
            "amount": amount,
            "detected": detected,
        },
    )