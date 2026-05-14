from metro_sim.player.actions.player_action import PlayerAction
from metro_sim.player.models.player_state import PlayerState
from metro_sim.world.models.world_state import WorldState
from metro_sim.world.services.pressure_service import add_station_pressure


def resolve_completed_player_actions(
    world: WorldState,
    players: dict[str, PlayerState],
) -> list[PlayerAction]:
    completed_actions: list[PlayerAction] = []

    for player in players.values():
        still_active_actions: list[PlayerAction] = []

        for action in player.active_actions:
            if action.status != "active":
                still_active_actions.append(action)
                continue

            if world.current_tick < action.completes_at_tick:
                still_active_actions.append(action)
                continue

            _apply_action_effects(world, player, action)
            action.status = "completed"
            completed_actions.append(action)

        player.active_actions = still_active_actions

    return completed_actions


def _apply_action_effects(
    world: WorldState,
    player: PlayerState,
    action: PlayerAction,
) -> None:
    effects = action.payload.get("definition", {}).get("effects", {})

    _apply_crew_effects(player, effects.get("crew", {}))
    _apply_player_reputation_effects(player, action, effects.get("player_reputation", {}))
    _apply_station_pressure_effects(world, action, effects.get("station_pressure", {}))


def _apply_crew_effects(player: PlayerState, crew_effects: dict[str, int]) -> None:
    for key, delta in crew_effects.items():
        if hasattr(player.crew, key):
            current_value = getattr(player.crew, key)
            setattr(player.crew, key, current_value + delta)


def _apply_player_reputation_effects(
    player: PlayerState,
    action: PlayerAction,
    reputation_effects: dict[str, int],
) -> None:
    for target, delta in reputation_effects.items():
        if target == "station":
            reputation_key = action.target_id
        else:
            reputation_key = target

        current_value = player.reputation.values.get(reputation_key, 0)
        player.reputation.values[reputation_key] = current_value + delta


def _apply_station_pressure_effects(
    world: WorldState,
    action: PlayerAction,
    pressure_effects: dict[str, int],
) -> None:
    if action.target_type != "station":
        return

    if action.target_id not in world.stations:
        return

    station = world.stations[action.target_id]

    for pressure_key, delta in pressure_effects.items():
        add_station_pressure(station, pressure_key, delta)