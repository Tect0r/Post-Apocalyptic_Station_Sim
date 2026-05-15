import json
from pathlib import Path
    
def load_json(name: str) -> dict:
    project_root = Path(__file__).resolve().parents[3]
    buildings_path = project_root / "data" / name

    with open(buildings_path, "r", encoding="utf-8") as file:
        return json.load(file)
    
def load_player_actions_data() -> dict:
    return load_json("player_actions.json")

def load_world_event_rules_data() -> dict:
    return load_json("world_event_rules.json")

def load_world_data() -> dict:
    return load_json("world.json")

def load_contracts_data() -> dict:
    return load_json("contracts.json")

def load_player_assets_data() -> dict:
    return load_json("player_assets.json")

def load_market_items_data() -> dict:
    return load_json("market_items.json")