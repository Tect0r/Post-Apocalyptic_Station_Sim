from fastapi import APIRouter, Depends, HTTPException

from metro_sim.auth.models.user_state import UserState
from metro_sim.contracts.services.contract_acceptance_service import accept_contract
from metro_sim.contracts.services.contract_query_service import get_available_contracts, get_contract_by_id
from metro_sim.interfaces.api.api_state import (
    get_game_session,
    save_current_game_session,
)
from metro_sim.interfaces.api.dependencies.auth_dependencies import get_current_user
from metro_sim.interfaces.api.schemas.action_schema import ActionResponseSchema
from metro_sim.interfaces.api.schemas.response_builders import build_contract_response

router = APIRouter(prefix="/contracts", tags=["contracts"])


@router.get("")
def get_contracts(
    current_user: UserState = Depends(get_current_user),
) -> dict:
    session = get_game_session()

    return {
        "contracts": [
            build_contract_response(contract)
            for contract in get_available_contracts(session)
        ]
    }


@router.get("/{contract_id}")
def get_contract(
    contract_id: str,
    current_user: UserState = Depends(get_current_user),
) -> dict:
    session = get_game_session()
    contract = get_contract_by_id(session, contract_id)

    if contract is None:
        raise HTTPException(
            status_code=404,
            detail="contract_not_found",
        )

    return build_contract_response(contract)


@router.post("/{contract_id}/accept", response_model=ActionResponseSchema)
def accept_contract_route(
    contract_id: str,
    current_user: UserState = Depends(get_current_user),
) -> ActionResponseSchema:
    session = get_game_session()

    result = accept_contract(
        session=session,
        player_id=current_user.player_id,
        contract_id=contract_id,
    )

    if not result.success:
        raise HTTPException(
            status_code=400,
            detail=result.message,
        )

    save_current_game_session()

    return ActionResponseSchema(
        success=result.success,
        message=result.message,
        data=result.data,
    )