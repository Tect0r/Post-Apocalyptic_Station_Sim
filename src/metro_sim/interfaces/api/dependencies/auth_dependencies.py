from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from metro_sim.auth.repositories.user_repository import get_user_by_id
from metro_sim.auth.services.token_service import decode_access_token
from metro_sim.auth.models.user_state import UserState
from metro_sim.interfaces.api.api_state import ensure_player_exists


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> UserState:
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="invalid_token",
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="invalid_token",
        )

    user = get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="user_not_found",
        )

    ensure_player_exists(
        player_id=user.player_id,
        name=user.username,
    )

    return user