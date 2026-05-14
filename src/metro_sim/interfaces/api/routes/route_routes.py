from fastapi import APIRouter, HTTPException

from metro_sim.interfaces.api.api_state import get_game_session
from metro_sim.interfaces.api.schemas.response_builders import build_route_response

router = APIRouter(tags=["routes"])


@router.get("/routes")
def get_routes() -> dict:
    session = get_game_session()

    return {
        "routes": {
            route_id: build_route_response(session, route_id)
            for route_id in session.world.routes.keys()
        }
    }


@router.get("/routes/{route_id}")
def get_route(route_id: str) -> dict:
    session = get_game_session()

    try:
        return build_route_response(session, route_id)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="route_not_found",
        )