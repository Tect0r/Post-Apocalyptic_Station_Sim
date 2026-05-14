from fastapi.testclient import TestClient

from metro_sim.interfaces.api.app import app
from tests.api_test_helpers import authenticated_test_user

client = TestClient(app)


def test_get_contracts_returns_available_contracts():
    with authenticated_test_user(client) as auth:
        response = client.get(
            "/contracts",
            headers=auth["headers"],
        )

        assert response.status_code == 200
        assert "contracts" in response.json()
        assert len(response.json()["contracts"]) > 0


def test_get_single_contract():
    with authenticated_test_user(client) as auth:
        response = client.get(
            "/contracts/contract_support_paveletskaya_militia",
            headers=auth["headers"],
        )

        assert response.status_code == 200
        assert response.json()["id"] == "contract_support_paveletskaya_militia"


def test_accept_contract_via_api():
    with authenticated_test_user(client) as auth:
        response = client.post(
            "/contracts/contract_support_paveletskaya_militia/accept",
            headers=auth["headers"],
        )

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["message"] == "contract_accepted"
        assert "action_id" in response.json()["data"]