from metro_sim.auth.repositories.user_repository import get_user_by_email
from metro_sim.auth.services.password_service import verify_password
from metro_sim.auth.services.token_service import create_access_token
from metro_sim.core.action_result import ActionResult


def login_user(email: str, password: str) -> ActionResult:
    user = get_user_by_email(email)

    if user is None:
        return ActionResult(False, "invalid_credentials")

    if not verify_password(password, user.password_hash):
        return ActionResult(False, "invalid_credentials")

    token = create_access_token(
        user_id=user.id,
        player_id=user.player_id,
    )

    return ActionResult(
        True,
        "login_successful",
        {
            "access_token": token,
            "token_type": "bearer",
            "user_id": user.id,
            "player_id": user.player_id,
            "username": user.username,
        },
    )