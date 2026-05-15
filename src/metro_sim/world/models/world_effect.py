from dataclasses import dataclass
from typing import Any


@dataclass
class WorldEffect:
    target_type: str
    target_id: str
    field_path: list[str]
    operation: str
    value: Any
    reason: str
    source: str = "system"
    importance: str = "normal"