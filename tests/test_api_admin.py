from fastapi.testclient import TestClient

from metro_sim.interfaces.api.app import app

client = TestClient(app)


def test_admin_saves_returns_save_name():
    response = client.post("/admin/save?save_name=test_api_save")

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["save_name"] == "test_api_save"


def test_admin_saves_list_contains_save():
    response = client.get("/admin/saves")

    assert response.status_code == 200
    assert "saves" in response.json()