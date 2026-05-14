from datetime import datetime, timezone

from metro_sim.core.game_session import GameSession
from metro_sim.persistence.json_save_writer import write_json_file
from metro_sim.persistence.player_serializer import serialize_players
from metro_sim.persistence.save_paths import (
    get_metadata_save_path,
    get_players_save_path,
    get_world_save_path,
)
from metro_sim.persistence.world_serializer import serialize_world_state


SAVE_VERSION = 1


def save_game_session(session: GameSession, save_name: str) -> None:
    metadata = {
        "save_version": SAVE_VERSION,
        "save_name": save_name,
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "last_processed_at": session.last_processed_at,
    }

    write_json_file(
        get_metadata_save_path(save_name),
        metadata,
    )

    write_json_file(
        get_world_save_path(save_name),
        serialize_world_state(session.world),
    )

    write_json_file(
        get_players_save_path(save_name),
        serialize_players(session.players),
    )