from datetime import datetime, timezone
from uuid import uuid4

from metro_sim.auth.models.user_state import UserState
from metro_sim.auth.repositories.user_repository import (
    add_user,
    get_user_by_email,
    get_user_by_username,
)
from metro_sim.auth.services.password_service import hash_password
from metro_sim.core.action_result import ActionResult


def register_user(
    email: str,
    username: str,
    password: str,
) -> ActionResult:
    email = email.lower().strip()
    username = username.strip()

    if get_user_by_email(email) is not None:
        return ActionResult(False, "email_already_registered")

    if get_user_by_username(username) is not None:
        return ActionResult(False, "username_already_registered")

    user_id = str(uuid4())
    player_id = f"player_{user_id}"

    user = UserState(
        id=user_id,
        email=email,
        username=username,
        password_hash=hash_password(password),
        player_id=player_id,
        created_at=datetime.now(timezone.utc).isoformat(),
    )

    add_user(user)

    return ActionResult(
        True,
        "user_registered",
        {
            "user_id": user.id,
            "player_id": user.player_id,
            "username": user.username,
            "email": user.email,
        },
    )