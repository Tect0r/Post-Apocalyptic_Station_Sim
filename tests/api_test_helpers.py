from contextlib import contextmanager
from uuid import uuid4

from metro_sim.auth.repositories.user_repository import delete_user_by_id
from metro_sim.interfaces.api.api_state import reset_game_session


def register_and_login_test_user(client, reset_session: bool = True):
    if reset_session:
        reset_game_session()

    unique_id = uuid4().hex

    email = f"user_{unique_id}@example.com"
    username = f"user_{unique_id[:8]}"
    password = "password123"

    user_id = None

    try:
        register_response = client.post(
            "/auth/register",
            json={
                "email": email,
                "username": username,
                "password": password,
            },
        )

        assert register_response.status_code == 200

        register_data = register_response.json()["data"]
        user_id = register_data["user_id"]

        login_response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": password,
            },
        )

        assert login_response.status_code == 200

        token = login_response.json()["data"]["access_token"]

        return {
            "email": email,
            "username": username,
            "password": password,
            "user_id": user_id,
            "player_id": register_data["player_id"],
            "token": token,
            "headers": {
                "Authorization": f"Bearer {token}",
            },
        }

    except Exception:
        if user_id is not None:
            delete_user_by_id(user_id)

        raise


def cleanup_test_user(auth: dict) -> None:
    delete_user_by_id(auth["user_id"])


@contextmanager
def authenticated_test_user(client, reset_session: bool = True):
    auth = register_and_login_test_user(
        client,
        reset_session=reset_session,
    )

    try:
        yield auth
    finally:
        cleanup_test_user(auth)