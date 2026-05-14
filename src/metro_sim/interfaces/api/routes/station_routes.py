from fastapi import APIRouter, HTTPException

from metro_sim.interfaces.api.api_state import get_game_session
from metro_sim.interfaces.api.schemas.response_builders import build_station_response

router = APIRouter(tags=["stations"])


@router.get("/stations")
def get_stations() -> dict:
    session = get_game_session()

    return {
        "stations": {
            station_id: build_station_response(session, station_id)
            for station_id in session.world.stations.keys()
        }
    }


@router.get("/stations/{station_id}")
def get_station(station_id: str) -> dict:
    session = get_game_session()

    try:
        return build_station_response(session, station_id)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="station_not_found",
        )