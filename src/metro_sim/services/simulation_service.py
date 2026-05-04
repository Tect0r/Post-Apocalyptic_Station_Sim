
from datetime import datetime, timedelta

from metro_sim.ui.cli import show_day_transition_report
from metro_sim.utils.file_loader import load_balancing

def calculate_power_consumption(station: dict) -> int:
    # Berechnet den Stromverbrauch basierend auf der Infrastruktur und den zugewiesenen Arbeitern
    balancing_dict = load_balancing()
    power_consumption = 0
    power_consumption += balancing_dict["power"]["building_consumption_kwh_per_day_by_level"]["living_quarters"][str(station['infrastructure_levels']['living_quarters'])]
    power_consumption += balancing_dict["power"]["building_consumption_kwh_per_day_by_level"]["food_production"][str(station['infrastructure_levels']['food_production'])]
    power_consumption += balancing_dict["power"]["building_consumption_kwh_per_day_by_level"]["water_system"][str(station['infrastructure_levels']['water_system'])]
    power_consumption += balancing_dict["power"]["building_consumption_kwh_per_day_by_level"]["trade_goods_production"][str(station['infrastructure_levels']['trade_goods_production'])]
    power_consumption += balancing_dict["power"]["building_consumption_kwh_per_day_by_level"]["trade_post"][str(station['infrastructure_levels']['trade_post'])]
    power_consumption += balancing_dict["power"]["building_consumption_kwh_per_day_by_level"]["guard_post"][str(station['infrastructure_levels']['guard_post'])]
    power_consumption += balancing_dict["power"]["building_consumption_kwh_per_day_by_level"]["bar"][str(station['infrastructure_levels']['bar'])]

    return power_consumption

def calculate_food_consumption(station: dict) -> int:
    # Berechnet den Nahrungsverbrauch basierend auf der Bevölkerung und den zugewiesenen Arbeitern
    balancing_dict = load_balancing()
    food_consumption = station['population']['total'] * balancing_dict["food"]["consumption_per_person"]
    return food_consumption

def calculate_water_consumption(station: dict) -> int:
    # Berechnet den Wasserverbrauch basierend auf der Bevölkerung, den zugewiesenen Arbeitern und der Wasserreinigung
    balancing_dict = load_balancing()
    if station['infrastructure_status']['water_system'] == 0:
        water_consumption = station['population']['total'] * balancing_dict["water"]["consumption_per_person"]
    else:
        water_consumption = 0
    return water_consumption

def calculate_trade_goods_consumption(station: dict) -> int:
    # Berechnet den Verbrauch von Handelsgütern basierend auf der Bevölkerung und den zugewiesenen Arbeitern
    balancing_dict = load_balancing()
    trade_goods_consumption = station['work_assignment']['trading'] * balancing_dict["trade_post"]["trade_capacity_per_worker_by_level"][str(station['infrastructure_levels']['trade_post'])]
    ammo_gained = station['work_assignment']['trading'] * balancing_dict["trade_goods"]["ammo_per_trade_good"]
    return trade_goods_consumption, ammo_gained

def calculate_food_production(station: dict) -> int:
    # Berechnet die Nahrungsproduktion basierend auf den zugewiesenen Arbeitern und der Infrastruktur
    balancing_dict = load_balancing()
    if station['infrastructure_status']['food_production'] > 0:
        food_production = station['work_assignment']['food_production'] * (balancing_dict["food_production"]["production_per_worker_by_level"][str(station['infrastructure_levels']['food_production'])])
    else:
        food_production = 0
    return food_production

def calculate_water_production(station: dict) -> int:
    # Berechnet die Wasserproduktion basierend auf den zugewiesenen Arbeitern und der Wasserreinigung
    balancing_dict = load_balancing()
    if station['infrastructure_status']['water_system'] > 0:
        water_production = balancing_dict["water_system"]["refill_per_day_by_level"][str(station['infrastructure_levels']['water_system'])]
    else:            
        water_production = 0
    return water_production

def calculate_trade_goods_production(station: dict) -> int:
    # Berechnet die Produktion von Handelsgütern basierend auf den zugewiesenen Arbeitern und der Infrastruktur
    balancing_dict = load_balancing()
    trade_goods_production = station['work_assignment']['trading_goods_production'] * (balancing_dict["trade_goods_production"]["production_per_worker_by_level"][str(station['infrastructure_levels']['trade_goods_production'])])
    return trade_goods_production


def simulate_next_day(station: dict) -> None:
    # Simuliert die Ereignisse des nächsten Tages und aktualisiert den Stationsstatus entsprechend
    balancing_dict = load_balancing()

    #Datum
    station['day'] += 1
    date_format = "%d.%m.%Y"
    new_date = datetime.strptime(station['date'], date_format) + timedelta(days=1)
    station['date'] = new_date.strftime(date_format)

    #Produktion
    food_produced = calculate_food_production(station)
    water_produced = calculate_water_production(station)
    station['resources']['food'] += food_produced
    station['resources']['water'] += water_produced

    food_consumed = calculate_food_consumption(station)
    water_consumed = calculate_water_consumption(station)
    station['resources']['food'] = max(0, station['resources']['food'] - food_consumed)
    station['resources']['water'] = max(0, station['resources']['water'] - water_consumed)

    #Trade
    trade_goods_produced = calculate_trade_goods_production(station)
    station['resources']['trade_goods'] += trade_goods_produced

    trade_goods_consumed, ammo_gained = calculate_trade_goods_consumption(station)
    station['resources']['trade_goods'] = max(0, station['resources']['trade_goods'] - trade_goods_consumed)
    station['resources']['ammo'] += ammo_gained

    #Stromverbrauch
    station['resources']['power_consumption'] = calculate_power_consumption(station)

    if(station['resources']['food'] == 0 or station['resources']['water'] == 0):
        station['stats']['morale'] = max(0, station['stats']['morale'] - 10)
        station['stats']['safety'] = max(0, station['stats']['safety'] - 10)

    #Events


    report_dict = {
        "day": station['day'],
        "date": station['date'],
        "food_consumed": food_consumed,
        "water_consumed": water_consumed,
        "food_produced": food_produced,
        "water_produced": water_produced,
        "trade_goods_produced": trade_goods_produced,
        "morale": station['stats']['morale'],
        "safety": station['stats']['safety']
    }

    show_day_transition_report(station, report_dict)
