import pytest

from metro_sim.services.worker_assignment_service import assign_workers_to_building


@pytest.fixture
def station():
    return {
        "slots": {
            "slot_1": {
                "building": None,
                "level": 0,
                "production_progress": 0,
            },
            "slot_2": {
                "building": "mushroom_farm",
                "level": 3,
                "production_progress": 20,
                "assigned_workers": 0,
            },
        },
        "population": {
            "worker_available": 10,
        },
    }


@pytest.fixture
def production_data():
    return {
        "mushroom_farm": {
            "levels": {
                "3": {
                    "max_workers": 10,
                }
            }
        }
    }


def patch_production_data(monkeypatch, production_data):
    monkeypatch.setattr(
        "metro_sim.services.worker_assignment_service.loader.load_production_data",
        lambda: production_data,
    )


def test_slot_is_not_in_station(station):
    result = assign_workers_to_building(station, "slot_9999", 10)

    assert result.success is False
    assert result.message == "slot_not_found"


def test_building_is_none(station):
    result = assign_workers_to_building(station, "slot_1", 10)

    assert result.success is False
    assert result.message == "slot_has_no_building"


def test_worker_amount_below_zero(station, production_data, monkeypatch):
    patch_production_data(monkeypatch, production_data)

    result = assign_workers_to_building(station, "slot_2", -10)

    assert result.success is False
    assert result.message == "invalid_worker_amount"


def test_too_many_workers_for_building(station, production_data, monkeypatch):
    patch_production_data(monkeypatch, production_data)

    result = assign_workers_to_building(station, "slot_2", 11)

    assert result.success is False
    assert result.message == "too_many_workers_for_building"


def test_not_enough_workers_available(station, production_data, monkeypatch):
    production_data["mushroom_farm"]["levels"]["3"]["max_workers"] = 20
    patch_production_data(monkeypatch, production_data)

    station["population"]["worker_available"] = 10

    result = assign_workers_to_building(station, "slot_2", 11)

    assert result.success is False
    assert result.message == "not_enough_available_workers"


def test_successful_assignment(station, production_data, monkeypatch):
    patch_production_data(monkeypatch, production_data)

    result = assign_workers_to_building(station, "slot_2", 10)

    assert result.success is True
    assert result.message == "workers_assigned"

    assert station["slots"]["slot_2"]["assigned_workers"] == 10
    assert station["population"]["worker_available"] == 0