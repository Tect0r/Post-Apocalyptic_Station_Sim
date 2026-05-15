from fastapi import APIRouter, Depends, HTTPException

from metro_sim.auth.models.user_state import UserState
from metro_sim.interfaces.api.api_state import (
    get_game_session_with_processing,
    save_current_game_session,
)
from metro_sim.interfaces.api.dependencies.auth_dependencies import get_current_user
from metro_sim.interfaces.api.schemas.action_schema import ActionResponseSchema
from metro_sim.interfaces.api.schemas.movement_schema import StartMovementRequestSchema
from metro_sim.player.services.crew_movement_service import start_crew_movement

router = APIRouter(prefix="/player/me/movement", tags=["movement"])


@router.post("/start", response_model=ActionResponseSchema)
def start_movement(
    request: StartMovementRequestSchema,
    current_user: UserState = Depends(get_current_user),
) -> ActionResponseSchema:
    session = get_game_session_with_processing()

    result = start_crew_movement(
        session=session,
        player_id=current_user.player_id,
        route_id=request.route_id,
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