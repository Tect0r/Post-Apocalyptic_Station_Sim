from dataclasses import dataclass


@dataclass
class UserState:
    id: str
    email: str
    username: str
    password_hash: str
    player_id: str
    created_at: str