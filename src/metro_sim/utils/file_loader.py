import json
from pathlib import Path

def load_balancing() -> dict:
    project_root = Path(__file__).resolve().parents[3]
    balancing_path = project_root / "data" / "balancing.json"

    with open(balancing_path, "r", encoding="utf-8") as file:
        return json.load(file)