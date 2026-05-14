import json
from dataclasses import asdict
from pathlib import Path

from metro_sim.auth.models.user_state import UserState


USER_STORE_PATH = Path("saves/auth/users.json")


def load_users() -> dict[str, UserState]:
    if not USER_STORE_PATH.exists():
        return {}

    with USER_STORE_PATH.open("r", encoding="utf-8") as file:
        raw_users = json.load(file)

    return {
        user_id: UserState(**user_data)
        for user_id, user_data in raw_users.items()
    }


def save_users(users: dict[str, UserState]) -> None:
    USER_STORE_PATH.parent.mkdir(parents=True, exist_ok=True)

    serialized = {
        user_id: asdict(user)
        for user_id, user in users.items()
    }

    with USER_STORE_PATH.open("w", encoding="utf-8") as file:
        json.dump(serialized, file, indent=2, ensure_ascii=False)


def get_user_by_id(user_id: str) -> UserState | None:
    return load_users().get(user_id)


def get_user_by_email(email: str) -> UserState | None:
    normalized_email = email.lower().strip()

    for user in load_users().values():
        if user.email.lower() == normalized_email:
            return user

    return None


def get_user_by_username(username: str) -> UserState | None:
    normalized_username = username.lower().strip()

    for user in load_users().values():
        if user.username.lower() == normalized_username:
            return user

    return None


def add_user(user: UserState) -> None:
    users = load_users()
    users[user.id] = user
    save_users(users)