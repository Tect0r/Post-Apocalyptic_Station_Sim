from fastapi.testclient import TestClient

from metro_sim.interfaces.api.app import app

client = TestClient(app)


def test_admin_tick_advances_world_in_debug_mode():
    world_before = client.get("/world").json()
    tick_before = world_before["tick"]

    response = client.post("/admin/tick?ticks=1")

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["mode"] == "manual_debug_tick"
    assert response.json()["tick"] == tick_before + 1


def test_admin_saves_returns_save_name():
    response = client.post("/admin/save?save_name=test_api_save")

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["save_name"] == "test_api_save"


def test_admin_saves_list_contains_save():
    response = client.get("/admin/saves")

    assert response.status_code == 200
    assert "saves" in response.json()