
from metro_sim.services.power_service import calculate_power_consumption
from metro_sim.utils.file_loader import load_initial_data


def create_initial_station():
    initial_dict = load_initial_data()

    station= {
        "name": "Paveletskaya",
        "time": {
            "day": 1,
            "date": "01.01.2033",
            "hour": 6,
            "minute": 0,
            "ticks_total": 0
        },

        "population": {
            "total": initial_dict["population"]["total"],
            "employed": initial_dict["population"]["employed"],
            "unemployed": initial_dict["population"]["unemployed"],
            "children": initial_dict["population"]["children"],
            "elderly": initial_dict["population"]["elderly"]
        },

        "employment": {
            "mushroom_production": 0,
            "pig_production": 0,
            "kitchen_work": 0,
            "maintenance": 0,
            "trade_goods_production": 0,
            "trading": 0,
            "guards": 0,
            "medical": 0,
            "machine_shop": 0,
            "stalker_expedition": 0,
            "service_work": 0
        },

        "ressources": {
            "mushrooms": initial_dict["ressources"]["mushrooms"],
            "pigs": initial_dict["ressources"]["pig_meat"],
            "water": initial_dict["ressources"]["water"],
            "medicine": initial_dict["ressources"]["medicine"],
            "power_consumption": 0,
            "trade_goods": initial_dict["ressources"]["trade_goods"],
            "spare_parts": initial_dict["ressources"]["spare_parts"],
            "ammo": initial_dict["ressources"]["ammo"]
        },

        "stats": {
            "morale": initial_dict["stats"]["morale"],
            "comfort": initial_dict["stats"]["comfort"],
            "safety": initial_dict["stats"]["safety"],
            "power_stability": initial_dict["stats"]["power_stability"],
            "power_contract": initial_dict["stats"]["power_contract"]
        },

        #0: broken, 1: working
        "infrastructure_status": {
            "water_system": 1,
            "power_generation": 1
        },

        "slots": {
            "slot_1": {"building": None, "level": 0, "production_progress": 0},
            "slot_2": {"building": None, "level": 0, "production_progress": 0},
            "slot_3": {"building": None, "level": 0, "production_progress": 0},
            "slot_4": {"building": None, "level": 0, "production_progress": 0},
            "slot_5": {"building": None, "level": 0, "production_progress": 0},
            "slot_6": {"building": None, "level": 0, "production_progress": 0},
            "slot_7": {"building": "mushroom_farm", "level": 1, "production_progress": 0},
            "slot_8": {"building": "living_quarters", "level": 1, "production_progress": 0},
            "slot_9": {"building": None, "level": 0, "production_progress": 0},
            "slot_10": {"building": None, "level": 0, "production_progress": 0},
            "slot_11": {"building": None, "level": 0, "production_progress": 0},
            "slot_12": {"building": None, "level": 0, "production_progress": 0},
            "slot_13": {"building": None, "level": 0, "production_progress": 0},
            "slot_14": {"building": None, "level": 0, "production_progress": 0},
            "slot_15": {"building": None, "level": 0, "production_progress": 0},
            "slot_16": {"building": None, "level": 0, "production_progress": 0},
            "slot_17": {"building": None, "level": 0, "production_progress": 0},
            "slot_18": {"building": None, "level": 0, "production_progress": 0},
            "slot_19": {"building": None, "level": 0, "production_progress": 0},
            "slot_20": {"building": None, "level": 0, "production_progress": 0},
            "slot_21": {"building": None, "level": 0, "production_progress": 0},
        }
    }


    station["ressources"]["power_consumption"] = calculate_power_consumption(station)

    return station