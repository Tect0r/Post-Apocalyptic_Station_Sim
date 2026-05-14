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
    }


def build_player_response(session: GameSession, player_id: str) -> dict:
    summary = build_game_summary(session)
    player = summary["player"]

    if player["id"] != player_id:
        raise KeyError(player_id)

    return player


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