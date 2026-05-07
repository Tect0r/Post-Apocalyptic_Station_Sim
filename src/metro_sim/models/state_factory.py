
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
            "employed": 0,
            "unemployed": initial_dict["population"]["unemployed"],
            "children": initial_dict["population"]["children"],
            "elderly": initial_dict["population"]["elderly"]
        },

        "resources": {
            "mushrooms": initial_dict["resources"]["mushrooms"],
            "pigs": initial_dict["resources"]["pig_meat"],
            "water": initial_dict["resources"]["water"],
            "medicine": initial_dict["resources"]["medicine"],
            "power_consumption": 0,
            "trade_goods": initial_dict["resources"]["trade_goods"],
            "spare_parts": initial_dict["resources"]["spare_parts"],
            "ammo": initial_dict["resources"]["ammo"]
        },

        "stats": {
            "morale": initial_dict["stats"]["morale"],
            "comfort": initial_dict["stats"]["comfort"],
            "safety": initial_dict["stats"]["safety"],
            "discontent" : 0,
            "power_stability": initial_dict["stats"]["power_stability"],
            "power_contract": initial_dict["stats"]["power_contract"]
        },

        #0: broken, 1: working
        "infrastructure_status": {
            "water_system": 1,
            "power_line": 1
        },

        "slots": {
            "slot_1": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
            "slot_2": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
            "slot_3": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
            "slot_4": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
            "slot_5": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
            "slot_6": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
            "slot_7": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
            "slot_8": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
            "slot_9": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
            "slot_10": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
            "slot_11": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
            "slot_12": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
            "slot_13": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
            "slot_14": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
            "slot_15": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
            "slot_16": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
            "slot_17": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
            "slot_18": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
            "slot_19": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
            "slot_20": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
            "slot_21": {"building": None, "level": 0, "production_progress": 0, "employed_worker" : 0, "building_status" : 1},
        }
    }


    station["resources"]["power_consumption"] = calculate_power_consumption(station)

    return station