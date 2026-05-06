import math

from metro_sim.utils.file_loader import load_balancing, load_buildings_cost_data, load_buildings_effects_data
from metro_sim.services.report_service import add_resource_change, add_stat_change


def apply_food_consumption(station: dict, report: dict) -> None:
    food_consumption = calculate_food_consumption(station)

    if station['ressources']['pigs'] >= food_consumption:
        station['ressources']['pigs'] -= food_consumption
        add_resource_change(report, "pigs", -food_consumption)
        return
    else:
        amount_left = food_consumption-station['ressources']['pigs']
        station['ressources']['pigs'] = 0
        add_resource_change(report, "pigs", -(amount_left-food_consumption))
    
    if station['ressources']['mushrooms'] >= amount_left:
        station['ressources']['mushrooms'] -= amount_left
        add_resource_change(report, "mushrooms", -amount_left)
    else:
        amount_not_covered = amount_left-station['ressources']['mushrooms']
        station['ressources']['mushrooms'] = 0
        add_resource_change(report, "mushrooms", -amount_not_covered)

def calculate_food_consumption(station: dict) -> int:
    # Berechnet den Nahrungsverbrauch basierend auf der Bevölkerung und den zugewiesenen Arbeitern
    # Nahrungsverbrauch gucken wegen pigs und mushrooms + kitchen
    balancing_dict = load_balancing()
    food_consumption = math.ceil((station['population']['total'] * balancing_dict["food"]["consumption_per_person_per_day"])/ len(balancing_dict["time"]["meal_hours"]))
    return food_consumption

def calculate_water_consumption(station: dict) -> int:
    # Berechnet den Wasserverbrauch basierend auf der Bevölkerung, den zugewiesenen Arbeitern und der Wasserreinigung
    balancing_dict = load_balancing()
    if station['infrastructure_status']['water_system'] == 0:
        water_consumption = station['population']['total'] * balancing_dict["water"]["consumption_per_person_on_failure"]
    else:
        water_consumption = 0
    return water_consumption


def calculate_spare_parts_consumption(station: dict) -> int:
    # Berechnet den Ersatzteilverbrauch basierend auf den zugewiesenen Arbeitern und der Infrastruktur
    balancing_dict = load_balancing()
    spare_parts_consumption = station['work_assignment']['maintenance'] * balancing_dict["maintenance"]["spare_parts_consumption_per_worker_by_level"][str(station['infrastructure_levels']['maintenance'])]
    return spare_parts_consumption

def calculate_bar_consumption(station: dict) -> int:
    # Berechnet den Verbrauch von Handelsgütern basierend auf der Bevölkerung und den zugewiesenen Arbeitern
    balancing_dict = load_balancing()
    bar_consumption = station['work_assignment']['service_work'] * balancing_dict["bar"]["trade_goods_consumption_per_worker_by_level"][str(station['infrastructure_levels']['bar'])]
    return bar_consumption

def calculate_consumption_for_tick(station: dict) -> dict:
    balancing = load_balancing()

    report = {
        "resource_changes": {},
        "stat_changes": {},
        "messages": []
    }

    is_meal_time = (
        station["time"]["hour"] in balancing["time"]["meal_hours"]
        and station["time"]["minute"] == 0
    )

    if is_meal_time:
        apply_food_consumption(station, report=report)

    return report