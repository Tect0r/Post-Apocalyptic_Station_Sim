from uuid import uuid4

from fastapi.testclient import TestClient

from metro_sim.auth.repositories.user_repository import delete_user_by_id
from metro_sim.interfaces.api.app import app
from tests.api_test_helpers import authenticated_test_user


client = TestClient(app)


def test_register_and_login_user():
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
        assert register_response.json()["success"] is True

        user_id = register_response.json()["data"]["user_id"]

        login_response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": password,
            },
        )

        assert login_response.status_code == 200
        data = login_response.json()

        assert data["success"] is True
        assert "access_token" in data["data"]

    finally:
        if user_id is not None:
            delete_user_by_id(user_id)


def test_player_me_requires_authentication():
    response = client.get("/player/me")

    assert response.status_code in (401, 403)


def test_player_me_returns_authenticated_player():
    with authenticated_test_user(client) as auth:
        response = client.get(
            "/player/me",
            headers=auth["headers"],
        )

        assert response.status_code == 200
        assert response.json()["name"] == auth["username"]