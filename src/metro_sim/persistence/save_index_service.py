from metro_sim.persistence.json_save_reader import read_json_file
from metro_sim.persistence.save_paths import SAVE_ROOT, get_metadata_save_path


def list_save_games() -> list[dict]:
    if not SAVE_ROOT.exists():
        return []

    saves = []

    for save_dir in SAVE_ROOT.iterdir():
        if not save_dir.is_dir():
            continue

        metadata_path = get_metadata_save_path(save_dir.name)

        if not metadata_path.exists():
            continue

        metadata = read_json_file(metadata_path)
        saves.append(metadata)

    return saves