from dataclasses import dataclass, field


@dataclass
class PlayerAsset:
    id: str
    name: str
    asset_type: str
    location_id: str | None = None
    condition: int = 100
    metadata: dict = field(default_factory=dict)