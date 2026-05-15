from fastapi import APIRouter

from metro_sim.core.game_summary_service import build_game_summary
from metro_sim.interfaces.api.api_state import get_game_session

router = APIRouter(tags=["factions"])


@router.get("/factions")
def get_factions() -> dict:
    session = get_game_session()
    summary = build_game_summary(session)

    return {
        "factions": summary["factions"]
    }