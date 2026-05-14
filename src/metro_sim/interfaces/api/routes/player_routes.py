from fastapi import APIRouter, HTTPException

from metro_sim.interfaces.api.api_state import get_game_session
from metro_sim.interfaces.api.schemas.response_builders import build_player_response

router = APIRouter(prefix="/player", tags=["player"])

TEST_PLAYER_ID = "player_001"


@router.get("/me")
def get_me() -> dict:
    session = get_game_session()

    try:
        return build_player_response(session, TEST_PLAYER_ID)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="player_not_found",
        )


@router.get("/me/crew")
def get_my_crew() -> dict:
    player = get_me()
    return player["crew"]


@router.get("/me/actions")
def get_my_actions() -> dict:
    player = get_me()

    return {
        "active_actions": player["active_actions"]
    }