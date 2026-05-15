from fastapi import APIRouter

from metro_sim.interfaces.api.api_state import get_game_session
from metro_sim.world.simulation.log_system import (
    get_debug_world_logs,
    get_logs_for_target,
    get_visible_world_logs,
)


router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("")
def get_logs(limit: int = 50, debug: bool = False) -> dict:
    session = get_game_session()

    if debug:
        logs = get_debug_world_logs(
            world=session.world,
            limit=limit,
        )
    else:
        logs = get_visible_world_logs(
            world=session.world,
            limit=limit,
        )

    return {
        "logs": logs,
    }


@router.get("/{target_type}/{target_id}")
def get_target_logs(
    target_type: str,
    target_id: str,
    limit: int = 50,
) -> dict:
    session = get_game_session()

    logs = get_logs_for_target(
        world=session.world,
        target_type=target_type,
        target_id=target_id,
        limit=limit,
    )

    return {
        "logs": logs,
    }