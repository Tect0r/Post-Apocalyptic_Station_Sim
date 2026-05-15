from metro_sim.pvp.models.pvp_action_type import PvPActionType


def is_pvp_action_on_cooldown(
    world,
    source_player_id: str,
    action_type: PvPActionType,
    target_type: str,
    target_id: str,
    cooldown_ticks: int,
) -> bool:
    for impact in reversed(world.pvp_impacts):
        if impact.source_player_id != source_player_id:
            continue

        if impact.action_type != action_type:
            continue

        if impact.target_type != target_type:
            continue

        if impact.target_id != target_id:
            continue

        return world.current_tick - impact.created_tick < cooldown_ticks

    return False