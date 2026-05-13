from dataclasses import dataclass, field


@dataclass
class InventoryState:
    items: dict[str, int] = field(default_factory=dict)