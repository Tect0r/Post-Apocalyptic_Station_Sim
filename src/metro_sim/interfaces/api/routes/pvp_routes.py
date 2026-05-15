from fastapi import APIRouter, Depends, HTTPException

from metro_sim.auth.models.user_state import UserState
from metro_sim.interfaces.api.api_state import get_game_session, save_current_game_session
from metro_sim.interfaces.api.dependencies.auth_dependencies import get_current_user
from metro_sim.interfaces.api.schemas.pvp_schema import (
    AssetDamagePvpRequestSchema,
    PvpActionResponseSchema,
    StationPressurePvpRequestSchema,
)
from metro_sim.interfaces.api.schemas.response_builders import build_pvp_impact_response
from metro_sim.pvp.services.asset_pvp_service import damage_player_asset_indirectly
from metro_sim.pvp.services.station_pressure_pvp_service import influence_station_pressure

router = APIRouter(prefix="/pvp", tags=["pvp"])


@router.get("/impacts")
def get_pvp_impacts(
    current_user: UserState = Depends(get_current_user),
) -> dict:
    session = get_game_session()

    return {
        "impacts": [
            build_pvp_impact_response(impact)
            for impact in session.world.pvp_impacts[-50:]
        ]
    }


@router.post("/station-pressure", response_model=PvpActionResponseSchema)
def influence_station_pressure_route(
    request: StationPressurePvpRequestSchema,
    current_user: UserState = Depends(get_current_user),
) -> PvpActionResponseSchema:
    session = get_game_session()

    result = influence_station_pressure(
        session=session,
        source_player_id=current_user.player_id,
        station_id=request.station_id,
        pressure_key=request.pressure_key,
        amount=request.amount,
    )

    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)

    save_current_game_session()

    return PvpActionResponseSchema(
        success=result.success,
        message=result.message,
        data=result.data,
    )


@router.post("/damage-asset", response_model=PvpActionResponseSchema)
def damage_asset_route(
    request: AssetDamagePvpRequestSchema,
    current_user: UserState = Depends(get_current_user),
) -> PvpActionResponseSchema:
    session = get_game_session()

    result = damage_player_asset_indirectly(
        session=session,
        source_player_id=current_user.player_id,
        target_player_id=request.target_player_id,
        asset_id=request.asset_id,
        amount=request.amount,
    )

    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)

    save_current_game_session()

    return PvpActionResponseSchema(
        success=result.success,
        message=result.message,
        data=result.data,
    )