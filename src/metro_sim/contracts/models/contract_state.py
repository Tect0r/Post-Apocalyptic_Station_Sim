from dataclasses import dataclass, field

from metro_sim.contracts.models.contract_status import ContractStatus


@dataclass
class ContractState:
    id: str
    title: str
    description_key: str
    issuer_type: str
    issuer_id: str
    target_type: str
    target_id: str
    action_type: str
    duration_ticks: int
    cost: dict[str, int] = field(default_factory=dict)
    reward: dict[str, int] = field(default_factory=dict)
    effects: dict = field(default_factory=dict)
    status: ContractStatus = ContractStatus.AVAILABLE
    accepted_by_player_id: str | None = None
    linked_action_id: str | None = None
    created_tick: int = 0
    accepted_tick: int | None = None
    completed_tick: int | None = None