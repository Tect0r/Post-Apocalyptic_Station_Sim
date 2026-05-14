from metro_sim.contracts.models.contract_state import ContractState


def create_contract_state(
    contract_id: str,
    contract_data: dict,
    created_tick: int = 0,
) -> ContractState:
    return ContractState(
        id=contract_id,
        title=contract_data["title"],
        description_key=contract_data["description_key"],
        issuer_type=contract_data["issuer_type"],
        issuer_id=contract_data["issuer_id"],
        target_type=contract_data["target_type"],
        target_id=contract_data["target_id"],
        action_type=contract_data["action_type"],
        duration_ticks=contract_data["duration_ticks"],
        cost=contract_data.get("cost", {}),
        reward=contract_data.get("reward", {}),
        effects=contract_data.get("effects", {}),
        created_tick=created_tick,
    )