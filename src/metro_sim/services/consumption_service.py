import math

from metro_sim.utils.file_loader import load_balancing, load_buildings_cost_data, load_buildings_effects_data
import metro_sim.services.report_service as report_service


def apply_food_consumption(station: dict, report: dict) -> None:
    food_consumption = calculate_food_consumption(station)

    if station['resources']['pigs'] >= food_consumption:
        station['resources']['pigs'] -= food_consumption
        report_service.add_resource_change(report, "pigs", -food_consumption)
        return
    else:
        amount_left = food_consumption-station['resources']['pigs']
        station['resources']['pigs'] = 0
        report_service.add_resource_change(report, "pigs", -(amount_left-food_consumption))
    
    if station['resources']['mushrooms'] >= amount_left:
        station['resources']['mushrooms'] -= amount_left
        report_service.add_resource_change(report, "mushrooms", -amount_left)
    else:
        amount_not_covered = amount_left-station['resources']['mushrooms']
        station['resources']['mushrooms'] = 0
        report_service.add_resource_change(report, "mushrooms", -amount_not_covered)

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
    
    # geh alle infrastructures durch (slots + power + water) und calc die instandhaltung
    # wie geht man damit um, wenn nicht genug spare_parts da sind?

    return 0

def calculate_bar_consumption(station: dict) -> int:
    # Berechnet den Verbrauch von Handelsgütern basierend auf der Bevölkerung und den zugewiesenen Arbeitern
    balancing_dict = load_balancing()
    bar_consumption = station['work_assignment']['service_work'] * balancing_dict["bar"]["trade_goods_consumption_per_worker_by_level"][str(station['infrastructure_levels']['bar'])]
    return bar_consumption

def calculate_consumption_for_tick(station: dict) -> dict:
    balancing = load_balancing()

    report = report_service.create_empty_report()

    is_meal_time = (
        station["time"]["hour"] in balancing["time"]["meal_hours"]
        and station["time"]["minute"] == 0
    )

    if is_meal_time:
        apply_food_consumption(station, report=report)

    return report