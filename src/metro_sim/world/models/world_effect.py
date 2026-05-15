from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


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
    id: str = field(default_factory=lambda: str(uuid4()))