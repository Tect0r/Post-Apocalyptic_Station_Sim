from fastapi import APIRouter, Depends, HTTPException

from metro_sim.auth.models.user_state import UserState
from metro_sim.interfaces.api.api_state import get_game_session, save_current_game_session
from metro_sim.interfaces.api.dependencies.auth_dependencies import get_current_user
from metro_sim.interfaces.api.schemas.asset_schema import (
    AddAssetRequestSchema,
    AssetActionResponseSchema,
)
from metro_sim.interfaces.api.schemas.response_builders import build_player_asset_response
from metro_sim.player.services.player_asset_service import (
    add_player_asset,
    repair_player_asset,
    upgrade_player_asset,
)

router = APIRouter(prefix="/player/me/assets", tags=["assets"])


@router.get("")
def get_my_assets(
    current_user: UserState = Depends(get_current_user),
) -> dict:
    session = get_game_session()
    player = session.players[current_user.player_id]

    return {
        "assets": [
            build_player_asset_response(asset)
            for asset in player.assets
        ]
    }


@router.post("", response_model=AssetActionResponseSchema)
def add_asset_debug(
    request: AddAssetRequestSchema,
    current_user: UserState = Depends(get_current_user),
) -> AssetActionResponseSchema:
    session = get_game_session()

    result = add_player_asset(
        session=session,
        player_id=current_user.player_id,
        asset_type=request.asset_type,
        station_id=request.station_id,
        route_id=request.route_id,
        metadata={
            "source": "debug_api",
        },
    )

    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)

    save_current_game_session()

    return AssetActionResponseSchema(
        success=result.success,
        message=result.message,
        data=result.data,
    )


@router.post("/{asset_id}/upgrade", response_model=AssetActionResponseSchema)
def upgrade_asset(
    asset_id: str,
    current_user: UserState = Depends(get_current_user),
) -> AssetActionResponseSchema:
    session = get_game_session()

    result = upgrade_player_asset(
        session=session,
        player_id=current_user.player_id,
        asset_id=asset_id,
    )

    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)

    save_current_game_session()

    return AssetActionResponseSchema(
        success=result.success,
        message=result.message,
        data=result.data,
    )


@router.post("/{asset_id}/repair", response_model=AssetActionResponseSchema)
def repair_asset(
    asset_id: str,
    current_user: UserState = Depends(get_current_user),
) -> AssetActionResponseSchema:
    session = get_game_session()

    result = repair_player_asset(
        session=session,
        player_id=current_user.player_id,
        asset_id=asset_id,
    )

    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)

    save_current_game_session()

    return AssetActionResponseSchema(
        success=result.success,
        message=result.message,
        data=result.data,
    )