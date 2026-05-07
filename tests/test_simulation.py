
from metro_sim.services.simulation_service import simulate_next_day

def create_test_station() -> dict:
    return {
        "day": 1,
        "date": "01.01.2033",
        "population": {
            "total": 10
        },
        "resources": {
            "food": 100,
            "water": 100,
            "trade_goods": 0
        },
        "stats": {
            "morale": 50,
            "safety": 50
        },
        "work_assignment": {
            "food_production": 5,
            "trading_goods_production": 4
        },
        "infrastructure_status": {
            "power_generation": 1,
            "food_production": 1,
            "water_purification": 1
        },
        "infrastructure_levels": {
            "food_production": "1",
            "water_purification": "1",
            "trade_goods_production": 2
        }
    }


def create_test_balancing() -> dict:
    return {
        "food": {
            "consumption_per_person": 1,
            "production_per_day": {
                "0": 0,
                "1": 3,
                "2": 4,
                "3": 5
            }
        },
        "water": {
            "consumption_per_person": 1,
            "refill_per_day": {
                "0": 0,
                "1": 20,
                "2": 30,
                "3": 40
            }
        }
    }


def patch_dependencies(monkeypatch) -> None:
    monkeypatch.setattr(
        "metro_sim.services.simulation_service.load_balancing",
        create_test_balancing
    )

    monkeypatch.setattr(
        "metro_sim.services.simulation_service.show_day_transition_report",
        lambda station, report: None
    )
