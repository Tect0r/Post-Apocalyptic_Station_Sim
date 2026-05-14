from fastapi import APIRouter

from metro_sim.core.game_session import advance_tick
from metro_sim.interfaces.api.api_state import (
    get_game_session,
    load_game_session_into_memory,
    save_current_game_session,
    reset_game_session
)
from metro_sim.persistence.save_index_service import list_save_games

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/tick")
def tick_world(ticks: int = 1) -> dict:
    session = get_game_session()

    for _ in range(ticks):
        advance_tick(session)

    save_current_game_session()

    return {
        "success": True,
        "tick": session.world.current_tick,
        "ticks_advanced": ticks,
    }


@router.post("/save")
def save_game(save_name: str = "api_dev_save") -> dict:
    save_current_game_session(save_name)

    return {
        "success": True,
        "save_name": save_name,
    }


@router.post("/load")
def load_game(save_name: str = "api_dev_save") -> dict:
    session = load_game_session_into_memory(save_name)

    return {
        "success": True,
        "save_name": save_name,
        "tick": session.world.current_tick,
    }


@router.get("/saves")
def get_saves() -> dict:
    return {
        "saves": list_save_games()
    }

@router.post("/reset")
def reset_game() -> dict:
    session = reset_game_session()
    save_current_game_session()

    return {
        "success": True,
        "tick": session.world.current_tick,
    }