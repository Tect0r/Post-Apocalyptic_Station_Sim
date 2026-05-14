from metro_sim.core.game_session import GameSession
from metro_sim.persistence.json_save_reader import read_json_file
from metro_sim.persistence.player_deserializer import deserialize_players
from metro_sim.persistence.save_paths import get_players_save_path, get_world_save_path
from metro_sim.persistence.world_deserializer import deserialize_world_state


def load_game_session(save_name: str) -> GameSession:
    world_data = read_json_file(get_world_save_path(save_name))
    players_data = read_json_file(get_players_save_path(save_name))

    return GameSession(
        world=deserialize_world_state(world_data),
        players=deserialize_players(players_data),
    )