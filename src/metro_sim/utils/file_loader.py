import json
from pathlib import Path

def load_balancing() -> dict:
    project_root = Path(__file__).resolve().parents[3]
    balancing_path = project_root / "data" / "balancing.json"

    with open(balancing_path, "r", encoding="utf-8") as file:
        return json.load(file)
    
def load_map_data() -> dict:
    project_root = Path(__file__).resolve().parents[3]
    map_path = project_root / "data" / "map.json"

    with open(map_path, "r", encoding="utf-8") as file:
        return json.load(file)

def load_buildings_effects_data() -> dict:
    project_root = Path(__file__).resolve().parents[3]
    map_path = project_root / "data" / "buildings_effects.json"

    with open(map_path, "r", encoding="utf-8") as file:
        return json.load(file)

def load_buildings_ascii_data() -> dict:
    project_root = Path(__file__).resolve().parents[3]
    buildings_path = project_root / "data" / "buildings_ascii.json"

    with open(buildings_path, "r", encoding="utf-8") as file:
        return json.load(file)
    
def load_buildings_cost_data() -> dict:
    project_root = Path(__file__).resolve().parents[3]
    buildings_path = project_root / "data" / "buildings_costs.json"

    with open(buildings_path, "r", encoding="utf-8") as file:
        return json.load(file)
    
def load_initial_data() -> dict:
    project_root = Path(__file__).resolve().parents[3]
    buildings_path = project_root / "data" / "initial.json"

    with open(buildings_path, "r", encoding="utf-8") as file:
        return json.load(file)
    
def load_production_data() -> dict:
    project_root = Path(__file__).resolve().parents[3]
    buildings_path = project_root / "data" / "building_production.json"

    with open(buildings_path, "r", encoding="utf-8") as file:
        return json.load(file)
    
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