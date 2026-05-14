from uuid import uuid4

from fastapi.testclient import TestClient

from metro_sim.interfaces.api.app import app

client = TestClient(app)


def test_register_and_login_user():
    unique_id = uuid4().hex
    email = f"user_{unique_id}@example.com"
    username = f"user_{unique_id[:8]}"
    password = "password123"

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

def test_player_me_requires_authentication():
    response = client.get("/player/me")

    assert response.status_code in (401, 403)


def test_player_me_returns_authenticated_player():
    unique_id = uuid4().hex
    email = f"player_{unique_id}@example.com"
    username = f"player_{unique_id[:8]}"
    password = "password123"

    client.post(
        "/auth/register",
        json={
            "email": email,
            "username": username,
            "password": password,
        },
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    token = login_response.json()["data"]["access_token"]

    response = client.get(
        "/player/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == username