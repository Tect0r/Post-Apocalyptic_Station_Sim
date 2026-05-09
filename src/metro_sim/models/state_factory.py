
from metro_sim.services.power_service import calculate_power_consumption
from metro_sim.utils.file_loader import load_initial_data


def create_initial_station():
    initial_dict = load_initial_data()

    station= {
        "name": initial_dict["station"]["name"],
        "time": {
            "day": initial_dict["time"]["day"],
            "date": initial_dict["time"]["date"],
            "hour": initial_dict["time"]["hour"],
            "minute": initial_dict["time"]["minute"],
            "ticks_total": initial_dict["time"]["ticks_total"]
        },

        "population": {
            "total": initial_dict["population"]["total"],
            "worker_unavailable": 0,
            "worker_available": initial_dict["population"]["unemployed"],
            "children": initial_dict["population"]["children"],
            "elderly": initial_dict["population"]["elderly"]
        },

        "resources": {
            # Nahrung / Versorgung
            "food": {
                "mushrooms": initial_dict["resources"]["mushrooms"],
                "pigs": initial_dict["resources"]["pigs"],
                "pig_meat": 0,
                "soup": 0,
                "meat_soup": 0,
                "water": initial_dict["resources"]["water"],
            },

            "mechanical": {
                "trade_goods": initial_dict["resources"]["trade_goods"],
                "spare_parts": initial_dict["resources"]["spare_parts"],
                "scrap": 0,
                "mechanical_parts": 0,
                "power_units": 0,
            },

            "combat": {
                "ammo": initial_dict["resources"]["ammo"],
                "fuel": 0,
                "rare_loot": 0,
                "medicine": initial_dict["resources"]["medicine"],
                "chemicals": 0,
            },

            "trash" : {
                "organic_waste": 0
            }
        },

        "power": {
            "contract": initial_dict["stats"]["power_contract"],
            "consumption_kwh": 0,
            "available_kwh": 0,
            "local_kwh": 0,
            "contract_kwh": 0,
            "stability": initial_dict["stats"]["power_stability"],
            "maintenance_condition" : 100,
            #"working" | "broken"
            "infrastructure_status": "working"
        },

        "water_system" : {
            "maintenance_condition" : 100,
            #"working" | "broken"
            "infrastructure_status": "working"
        },

        "stats": {
            "morale": initial_dict["stats"]["morale"],
            "comfort": initial_dict["stats"]["comfort"],
            "safety": initial_dict["stats"]["safety"],
            "discontent": 0,

            # temporäre / abgeleitete Effektwerte
            "maintenance_points": 0,
            "combat_readiness": 0,
            "administration_points": 0,
            "market_value": 0,
            "treated_patients": 0
        },

        "slots": {
            "slot_0": {
                "building": "tunnel_scavenging",
                "level": 1,
                "production_progress": 0,
                "assigned_workers": 0,
                "building_status": "working",
                "maintenance_condition": 100
            }
        } | {
            f"slot_{index}": create_empty_slot()
            for index in range(1, 22)
        }
    }

    station["power"]["consumption_kwh"] = calculate_power_consumption(station)

    return station

def create_empty_slot() -> dict:
    return {
        "building": None,
        "level": 0,
        "production_progress": 0,
        "assigned_workers": 0,
        "building_status": "working",
        "maintenance_condition" : 100
    }