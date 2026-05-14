from dataclasses import asdict

from metro_sim.player.models.player_state import PlayerState


def serialize_player_state(player: PlayerState) -> dict:
    return asdict(player)


def serialize_players(players: dict[str, PlayerState]) -> dict:
    return {
        player_id: serialize_player_state(player)
        for player_id, player in players.items()
    }