import json
from pathlib import Path
from typing import Any


def read_json_file(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)