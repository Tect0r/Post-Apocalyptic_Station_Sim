from dataclasses import dataclass
from typing import Any

@dataclass
class ActionResult:
    success: bool
    message: str
    data: dict[str, Any] | None = None