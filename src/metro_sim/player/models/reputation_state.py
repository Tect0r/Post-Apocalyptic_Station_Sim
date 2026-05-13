from dataclasses import dataclass, field


@dataclass
class ReputationState:
    values: dict[str, int] = field(default_factory=dict)