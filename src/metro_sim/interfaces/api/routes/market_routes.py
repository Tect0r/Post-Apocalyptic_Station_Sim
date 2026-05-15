from fastapi import APIRouter, Depends, HTTPException

from metro_sim.auth.models.user_state import UserState
from metro_sim.interfaces.api.api_state import get_game_session, save_current_game_session
from metro_sim.interfaces.api.dependencies.auth_dependencies import get_current_user
from metro_sim.interfaces.api.schemas.market_schema import (
    MarketTradeRequestSchema,
    MarketTradeResponseSchema,
)
from metro_sim.market.services.market_price_service import get_station_market_prices
from metro_sim.market.services.market_trade_service import buy_market_item, sell_market_item

router = APIRouter(prefix="/market", tags=["market"])


@router.get("")
def get_current_station_market(
    current_user: UserState = Depends(get_current_user),
) -> dict:
    session = get_game_session()
    player = session.players[current_user.player_id]
    station_id = player.crew.current_location_id

    if station_id not in session.world.stations:
        raise HTTPException(status_code=404, detail="station_not_found")

    station = session.world.stations[station_id]

    return {
        "station_id": station_id,
        "prices": get_station_market_prices(station, player),
        "stock": station.market.get("stock", {}),
    }


@router.get("/stations/{station_id}")
def get_station_market(
    station_id: str,
    current_user: UserState = Depends(get_current_user),
) -> dict:
    session = get_game_session()
    player = session.players[current_user.player_id]

    if station_id not in session.world.stations:
        raise HTTPException(status_code=404, detail="station_not_found")

    station = session.world.stations[station_id]

    return {
        "station_id": station_id,
        "prices": get_station_market_prices(station, player),
        "stock": station.market.get("stock", {}),
        "accessible": player.crew.current_location_id == station_id,
    }


@router.post("/buy", response_model=MarketTradeResponseSchema)
def buy_item(
    request: MarketTradeRequestSchema,
    current_user: UserState = Depends(get_current_user),
) -> MarketTradeResponseSchema:
    session = get_game_session()

    result = buy_market_item(
        session=session,
        player_id=current_user.player_id,
        item_id=request.item_id,
        amount=request.amount,
    )

    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)

    save_current_game_session()

    return MarketTradeResponseSchema(
        success=result.success,
        message=result.message,
        data=result.data,
    )


@router.post("/sell", response_model=MarketTradeResponseSchema)
def sell_item(
    request: MarketTradeRequestSchema,
    current_user: UserState = Depends(get_current_user),
) -> MarketTradeResponseSchema:
    session = get_game_session()

    result = sell_market_item(
        session=session,
        player_id=current_user.player_id,
        item_id=request.item_id,
        amount=request.amount,
    )

    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)

    save_current_game_session()

    return MarketTradeResponseSchema(
        success=result.success,
        message=result.message,
        data=result.data,
    )