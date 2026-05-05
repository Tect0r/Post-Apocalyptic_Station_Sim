

import math

from metro_sim.utils.file_loader import load_balancing, load_buildings_cost_data, load_buildings_effects_data


def calculate_trade_goods_consumption(station: dict) -> int:
    # Berechnet den Verbrauch von Handelsgütern basierend auf der Bevölkerung und den zugewiesenen Arbeitern
    balancing_dict = load_balancing()
    trade_goods_consumption = station['work_assignment']['trading'] * balancing_dict["trade_post"]["trade_capacity_per_worker_by_level"][str(station['infrastructure_levels']['trade_post'])]
    ammo_gained = station['work_assignment']['trading'] * balancing_dict["trade_goods"]["ammo_per_trade_good"]
    return trade_goods_consumption, ammo_gained

def calculate_power_consumption(station: dict) -> int:
    # Berechnet den Stromverbrauch basierend auf der Infrastruktur und den zugewiesenen Arbeitern
    building_cost = load_buildings_cost_data()
    power_consumption = 0
    # Slots von Station durchgehen
    station_slots = station.get("slots", {}).values()
    for slot in station_slots:
        current_building = slot.get("building")
        if current_building is not None:
            power_consumption += building_cost[current_building]["kwh_per_day_by_level"][str(slot.get("level", 0))]

    return power_consumption

def apply_food_consumption(station: dict) -> None:
    food_consumption = calculate_food_consumption(station)

    if station['resources']['pigs'] >= food_consumption:
        station['resources']['pigs'] -= food_consumption
        return
    else:
        food_consumption -= station['resources']['pigs']
        station['resources']['pigs'] = 0
    
    if station['resources']['mushrooms'] >= food_consumption:
        station['resources']['mushrooms'] -= food_consumption
    else:
        food_consumption -= station['resources']['mushrooms']
        station['resources']['mushrooms'] = 0

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

def calculate_ammo_consumption(station: dict) -> int:
    # Berechnet den Munitionsverbrauch basierend auf der Bevölkerung, den zugewiesenen Arbeitern und der Sicherheit
    balancing_dict = load_balancing()
    ammo_consumption = station['work_assignment']['guards'] * balancing_dict["guards"]["ammo_consumption_per_guard_by_level"][str(station['infrastructure_levels']['guard_post'])]
    return ammo_consumption

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

def calculate_stalker_den_consumption(station: dict) -> int:
    # Berechnet den Verbrauch von Handelsgütern basierend auf der Bevölkerung und den zugewiesenen Arbeitern
    balancing_dict = load_balancing()
    stalker_den_consumption = station['work_assignment']['stalker_expedition'] * balancing_dict["stalker_den"]["trade_goods_consumption_per_worker_by_level"][str(station['infrastructure_levels']['stalker_den'])]
    return stalker_den_consumption

def calculate_living_quarters_capacity(station: dict) -> int:
    # Berechnet die Kapazität der Unterkünfte basierend auf der Infrastruktur
    building_effects = load_buildings_effects_data()
    station_slots = station.get("slots", {}).values()
    for slot in station_slots:
        if slot.get("building") == "living_quarters":
            living_quarters_capacity = building_effects["living_quarters"]["effects_by_level"][str(slot.get("level", {}))]["population_capacity"]

    return living_quarters_capacity