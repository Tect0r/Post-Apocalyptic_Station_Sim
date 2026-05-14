from pathlib import Path


SAVE_ROOT = Path("saves")


def get_save_directory(save_name: str) -> Path:
    return SAVE_ROOT / save_name


def get_world_save_path(save_name: str) -> Path:
    return get_save_directory(save_name) / "world_state.json"


def get_players_save_path(save_name: str) -> Path:
    return get_save_directory(save_name) / "players.json"


def get_metadata_save_path(save_name: str) -> Path:
    return get_save_directory(save_name) / "metadata.json"