import json
from pathlib import Path
from typing import Any


def read_json_file(path: str | Path) -> Any:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"JSON file does not exist: {path}")

    if path.stat().st_size == 0:
        raise ValueError(f"JSON file is empty: {path}")

    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON file: {path}. Error: {error}") from error