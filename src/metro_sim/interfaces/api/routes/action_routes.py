from fastapi import APIRouter, Depends, HTTPException

from metro_sim.auth.models.user_state import UserState
from metro_sim.interfaces.api.api_state import (
    get_game_session_with_processing,
    save_current_game_session,
)
from metro_sim.interfaces.api.dependencies.auth_dependencies import get_current_user
from metro_sim.interfaces.api.schemas.action_schema import (
    ActionResponseSchema,
    StartActionRequestSchema,
)
from metro_sim.player.actions.player_action_type import PlayerActionType
from metro_sim.player.actions.start_player_action_request import StartPlayerActionRequest
from metro_sim.player.services.player_action_service import start_player_action

router = APIRouter(prefix="/player/me/actions", tags=["actions"])


@router.post("", response_model=ActionResponseSchema)
def start_action(
    request: StartActionRequestSchema,
    current_user: UserState = Depends(get_current_user),
) -> ActionResponseSchema:
    session = get_game_session_with_processing()

    try:
        action_type = PlayerActionType(request.action_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="unknown_action_type",
        )

    result = start_player_action(
        session,
        StartPlayerActionRequest(
            player_id=current_user.player_id,
            action_type=action_type,
            target_id=request.target_id,
        ),
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