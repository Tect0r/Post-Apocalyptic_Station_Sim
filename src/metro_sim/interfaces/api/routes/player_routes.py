from fastapi import APIRouter, Depends, HTTPException

from metro_sim.auth.models.user_state import UserState
from metro_sim.interfaces.api.api_state import get_game_session
from metro_sim.interfaces.api.dependencies.auth_dependencies import get_current_user
from metro_sim.interfaces.api.schemas.response_builders import build_player_response

router = APIRouter(prefix="/player", tags=["player"])


@router.get("/me")
def get_me(current_user: UserState = Depends(get_current_user)) -> dict:
    session = get_game_session()

    try:
        return build_player_response(session, current_user.player_id)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="player_not_found",
        )


@router.get("/me/crew")
def get_my_crew(current_user: UserState = Depends(get_current_user)) -> dict:
    player = get_me(current_user)
    return player["crew"]


@router.get("/me/actions")
def get_my_actions(current_user: UserState = Depends(get_current_user)) -> dict:
    player = get_me(current_user)

    return {
        "active_actions": player["active_actions"]
    }