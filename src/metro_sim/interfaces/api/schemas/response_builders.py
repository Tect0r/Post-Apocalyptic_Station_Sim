from metro_sim.core.game_summary_service import build_game_summary
from metro_sim.core.game_session import GameSession


def build_world_response(session: GameSession) -> dict:
    summary = build_game_summary(session)

    return {
        "tick": summary["tick"],
        "stations": summary["stations"],
        "routes": summary["routes"],
        "factions": summary["factions"],
        "events": summary["events"],
        "players": summary["players"],
    }


def build_player_response(session: GameSession, player_id: str) -> dict:
    if player_id not in session.players:
        raise KeyError(player_id)

    player = session.players[player_id]

    return {
        "id": player.id,
        "name": player.name,
        "crew": {
            "members": player.crew.members,
            "health": player.crew.health,
            "morale": player.crew.morale,
            "fatigue": player.crew.fatigue,
            "specialization": player.crew.specialization,
        },
        "inventory": player.inventory.items,
        "reputation": player.reputation.values,
        "assets": [
            {
                "id": asset.id,
                "name": asset.name,
                "asset_type": asset.asset_type,
                "location_id": asset.location_id,
                "condition": asset.condition,
            }
            for asset in player.assets
        ],
        "active_actions": [
            {
                "id": action.id,
                "action_type": action.action_type.value,
                "target_type": action.target_type,
                "target_id": action.target_id,
                "started_tick": action.started_tick,
                "duration_ticks": action.duration_ticks,
                "completes_at_tick": action.completes_at_tick,
                "status": action.status,
            }
            for action in player.active_actions
        ],
    }


def build_station_response(session: GameSession, station_id: str) -> dict:
    summary = build_game_summary(session)

    if station_id not in summary["stations"]:
        raise KeyError(station_id)

    return summary["stations"][station_id]


def build_route_response(session: GameSession, route_id: str) -> dict:
    summary = build_game_summary(session)

    if route_id not in summary["routes"]:
        raise KeyError(route_id)

    return summary["routes"][route_id]


def build_public_player_summary(player) -> dict:
    return {
        "id": player.id,
        "name": player.name,
        "crew": {
            "members": player.crew.members,
            "health": player.crew.health,
            "morale": player.crew.morale,
            "fatigue": player.crew.fatigue,
            "specialization": player.crew.specialization,
        },
        "active_action_count": len(player.active_actions),
        "asset_count": len(player.assets),
    }
