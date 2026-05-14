from fastapi import APIRouter

from metro_sim.interfaces.api.api_state import get_game_session
from metro_sim.interfaces.api.schemas.response_builders import build_world_response

router = APIRouter(tags=["world"])


@router.get("/world")
def get_world() -> dict:
    session = get_game_session()
    return build_world_response(session)