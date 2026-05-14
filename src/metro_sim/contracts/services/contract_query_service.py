from metro_sim.contracts.models.contract_status import ContractStatus
from metro_sim.core.game_session import GameSession


def get_available_contracts(session: GameSession) -> list:
    return [
        contract
        for contract in session.world.contracts.values()
        if contract.status == ContractStatus.AVAILABLE
    ]


def get_contract_by_id(session: GameSession, contract_id: str):
    return session.world.contracts.get(contract_id)