
from metro_sim.services.simulation_service import simulate_next_day

def create_test_station() -> dict:
    return {
        "day": 1,
        "date": "01.01.2033",
        "population": {
            "total": 10
        },
        "ressources": {
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


def test_simulate_next_day_increases_day_by_one(monkeypatch):
    patch_dependencies(monkeypatch)
    station = create_test_station()

    simulate_next_day(station)

    assert station["day"] == 2


def test_simulate_next_day_increases_date_by_one_day(monkeypatch):
    patch_dependencies(monkeypatch)
    station = create_test_station()

    simulate_next_day(station)

    assert station["date"] == "02.01.2033"


def test_simulate_next_day_consumes_food(monkeypatch):
    patch_dependencies(monkeypatch)
    station = create_test_station()

    simulate_next_day(station)

    # Start 100 - Verbrauch 10 + Produktion 15
    assert station["ressources"]["food"] == 105


def test_simulate_next_day_does_not_consume_water_when_water_purification_works(monkeypatch):
    patch_dependencies(monkeypatch)
    station = create_test_station()

    simulate_next_day(station)

    # Start 100 - Verbrauch 0 + Produktion 20
    assert station["ressources"]["water"] == 120


def test_simulate_next_day_consumes_water_when_water_purification_is_broken(monkeypatch):
    patch_dependencies(monkeypatch)
    station = create_test_station()
    station["infrastructure_status"]["water_purification"] = 0

    simulate_next_day(station)

    # Start 100 - Verbrauch 10 + Produktion 0
    assert station["ressources"]["water"] == 90


def test_simulate_next_day_produces_food_when_power_and_food_production_work(monkeypatch):
    patch_dependencies(monkeypatch)
    station = create_test_station()

    simulate_next_day(station)

    # 5 Arbeiter * Produktionswert 3 = 15
    # Gleichzeitig werden 10 Nahrung verbraucht
    assert station["ressources"]["food"] == 105


def test_simulate_next_day_produces_water_when_power_and_water_purification_work(monkeypatch):
    patch_dependencies(monkeypatch)
    station = create_test_station()

    simulate_next_day(station)

    assert station["ressources"]["water"] == 120


def test_simulate_next_day_produces_trade_goods_when_power_works(monkeypatch):
    patch_dependencies(monkeypatch)
    station = create_test_station()

    simulate_next_day(station)

    # 4 Arbeiter * 1 * Level 2 = 8
    assert station["ressources"]["trade_goods"] == 8


def test_simulate_next_day_does_not_produce_when_power_is_down(monkeypatch):
    patch_dependencies(monkeypatch)
    station = create_test_station()
    station["infrastructure_status"]["power_generation"] = 0

    simulate_next_day(station)

    # Nahrung: 100 - 10 Verbrauch, keine Produktion
    assert station["ressources"]["food"] == 90

    # Wasser: keine Verbrauch, weil Wasseraufbereitung nicht defekt,
    # aber auch keine Produktion, weil kein Strom
    assert station["ressources"]["water"] == 100

    assert station["ressources"]["trade_goods"] == 0


def test_simulate_next_day_ressources_do_not_go_below_zero(monkeypatch):
    patch_dependencies(monkeypatch)
    station = create_test_station()
    station["ressources"]["food"] = 5
    station["ressources"]["water"] = 5
    station["infrastructure_status"]["water_purification"] = 0
    station["infrastructure_status"]["power_generation"] = 0

    simulate_next_day(station)

    assert station["ressources"]["food"] == 0
    assert station["ressources"]["water"] == 0


def test_simulate_next_day_lowers_morale_and_safety_when_food_reaches_zero(monkeypatch):
    patch_dependencies(monkeypatch)
    station = create_test_station()
    station["ressources"]["food"] = 5
    station["infrastructure_status"]["power_generation"] = 0

    simulate_next_day(station)

    assert station["stats"]["morale"] == 40
    assert station["stats"]["safety"] == 40


def test_simulate_next_day_lowers_morale_and_safety_when_water_reaches_zero(monkeypatch):
    patch_dependencies(monkeypatch)
    station = create_test_station()
    station["ressources"]["water"] = 5
    station["infrastructure_status"]["water_purification"] = 0
    station["infrastructure_status"]["power_generation"] = 0

    simulate_next_day(station)

    assert station["stats"]["morale"] == 40
    assert station["stats"]["safety"] == 40


def test_simulate_next_day_morale_and_safety_do_not_go_below_zero(monkeypatch):
    patch_dependencies(monkeypatch)
    station = create_test_station()
    station["ressources"]["food"] = 0
    station["ressources"]["water"] = 0
    station["stats"]["morale"] = 5
    station["stats"]["safety"] = 5
    station["infrastructure_status"]["water_purification"] = 0
    station["infrastructure_status"]["power_generation"] = 0

    simulate_next_day(station)

    assert station["stats"]["morale"] == 0
    assert station["stats"]["safety"] == 0
