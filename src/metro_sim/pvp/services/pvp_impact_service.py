from uuid import uuid4

from metro_sim.pvp.models.pvp_action_type import PvPActionType
from metro_sim.pvp.models.pvp_impact import PvPImpact


def add_pvp_impact(
    world,
    source_player_id: str,
    action_type: PvPActionType,
    target_type: str,
    target_id: str,
    effects: dict,
    target_player_id: str | None = None,
    detected: bool = False,
    reputation_cost: dict | None = None,
) -> PvPImpact:
    impact = PvPImpact(
        id=str(uuid4()),
        source_player_id=source_player_id,
        target_player_id=target_player_id,
        action_type=action_type,
        target_type=target_type,
        target_id=target_id,
        created_tick=world.current_tick,
        effects=effects,
        detected=detected,
        reputation_cost=reputation_cost or {},
    )

    world.pvp_impacts.append(impact)

    return impact