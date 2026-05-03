
from metro_sim.services.simulation_service import calculate_power_consumption
from metro_sim.utils.file_loader import load_balancing


def create_initial_station():
    balancing_dict = load_balancing()

    station= {
        "name": "Paveletskaya",
        "day": 1,
        "date": "01.01.2033",

    "population": {
        "total": balancing_dict["population"]["initial"],
        "employed": balancing_dict["population"]["start_employed"],
        "unemployed": balancing_dict["population"]["start_unemployed"]
    },

    "resources": {
        "food": balancing_dict["food"]["storage_start"],
        "water": balancing_dict["water"]["storage_start"],
        "medicine": 200,
        "power_consumption": 0,
        "trade_goods": balancing_dict["trade_goods"]["storage_start"],
        "ammo": 300
    },

    "stats": {
        "morale": 80,
        "comfort": 70,
        "safety": 90,
        "power_stability": 85,
        "power_level": 2
    },

    #0: broken, 1: basic, 2: improved, 3: advanced
    "infrastructure_status": {
        "food_production": 1,
        "water_purification": 1,
        "medical_facilities": 1,
        "defenses": 1,
        "power_generation": 1,
        "living_quarters": 1,
        "trade_goods_production": 1
    },

    #0: not build, 1:basic, 2: improved, 3: advanced
    "infrastructure_levels": {
        "food_production": 0,
        "water_purification": 0,
        "medical_facilities": 0,
        "defenses": 0,
        "power_generation": 0,
        "living_quarters": 0,
        "trade_goods_production": 0
    },

    "slots": {
        "slot_1": None,
        "slot_2": None,
        "slot_3": None,
        "slot_4": None
    },

    "work_assignment": {
        "food_production": 50,
        "service_work": 30,
        "trading_goods_production": 20,
        "trading": 15,
        "guards": 35
        }
    }  

    station["resources"]["power_consumption"] = calculate_power_consumption(station)

    return station