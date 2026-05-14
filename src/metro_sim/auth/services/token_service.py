from datetime import datetime, timezone

from jose import JWTError, jwt

from metro_sim.auth.services.auth_config import (
    ACCESS_TOKEN_EXPIRE_DELTA,
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
)


def create_access_token(user_id: str, player_id: str) -> str:
    now = datetime.now(timezone.utc)
    expires_at = now + ACCESS_TOKEN_EXPIRE_DELTA

    payload = {
        "sub": user_id,
        "player_id": player_id,
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
    }

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except JWTError as error:
        raise ValueError("invalid_token") from error