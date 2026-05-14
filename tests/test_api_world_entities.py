from fastapi.testclient import TestClient

from metro_sim.interfaces.api.app import app

client = TestClient(app)


def test_get_stations_returns_stations():
    response = client.get("/stations")

    assert response.status_code == 200
    assert "stations" in response.json()
    assert "paveletskaya" in response.json()["stations"]


def test_get_station_returns_single_station():
    response = client.get("/stations/paveletskaya")

    assert response.status_code == 200
    assert response.json()["id"] == "paveletskaya"


def test_get_missing_station_returns_404():
    response = client.get("/stations/missing_station")

    assert response.status_code == 404
    assert response.json()["detail"] == "station_not_found"


def test_get_routes_returns_routes():
    response = client.get("/routes")

    assert response.status_code == 200
    assert "routes" in response.json()


def test_get_missing_route_returns_404():
    response = client.get("/routes/missing_route")

    assert response.status_code == 404
    assert response.json()["detail"] == "route_not_found"