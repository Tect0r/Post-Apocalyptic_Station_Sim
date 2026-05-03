
from datetime import datetime, timedelta

from metro_sim.ui.cli import show_day_transition_report
from metro_sim.utils.file_loader import load_balancing

def calculate_power_consumption(station: dict) -> int:
    # Berechnet den Stromverbrauch basierend auf der Infrastruktur und den zugewiesenen Arbeitern
    balancing_dict = load_balancing()
    power_consumption = 0
    power_consumption += balancing_dict["food"]["power_consumption_per_farm_level"][str(station['infrastructure_levels']['food_production'])]
    power_consumption += balancing_dict["water"]["power_consumption_per_water_level"][str(station['infrastructure_levels']['water_purification'])]
    power_consumption += balancing_dict["trade_goods"]["power_consumption_per_trade_level"][str(station['infrastructure_levels']['trade_goods_production'])]
    power_consumption += balancing_dict["living_quarters"]["power_consumption_per_level"][str(station['infrastructure_levels']['living_quarters'])]

    return power_consumption

def simulate_next_day(station: dict) -> None:
    # Simuliert die Ereignisse des nächsten Tages und aktualisiert den Stationsstatus entsprechend
    balancing_dict = load_balancing()

    #Datum
    station['day'] += 1
    date_format = "%d.%m.%Y"
    new_date = datetime.strptime(station['date'], date_format) + timedelta(days=1)
    station['date'] = new_date.strftime(date_format)

    #Produktion
    if station['infrastructure_status']['power_generation'] > 0:
        if station['infrastructure_status']['food_production'] > 0:
            food_produced = station['work_assignment']['food_production'] * (balancing_dict["food"]["production_per_worker_by_farm_level"][str(station['infrastructure_levels']['food_production'])])
            station['resources']['food'] += food_produced
        else:
            food_produced = 0

        if station['infrastructure_status']['water_purification'] > 0:
            water_produced = balancing_dict["water"]["refill_per_day"][str(station['infrastructure_levels']['water_purification'])]
            station['resources']['water'] += water_produced
        else:            
            water_produced = 0

        trade_goods_produced = station['work_assignment']['trading_goods_production'] * (balancing_dict["trade_goods"]["production_per_worker_by_level"][str(station['infrastructure_levels']['trade_goods_production'])])
        station['resources']['trade_goods'] += trade_goods_produced
    else:
        food_produced = 0
        water_produced = 0
        trade_goods_produced = 0

    #Trade

    #Ressourcenverbrauch
    food_consumed = station['population']['total'] * balancing_dict["food"]["consumption_per_person"]

    if station['infrastructure_status']['water_purification'] == 0:
        water_consumed = station['population']['total'] * balancing_dict["water"]["consumption_per_person"]
    else:
        water_consumed = 0

    station['resources']['food'] = max(0, station['resources']['food'] - food_consumed)
    station['resources']['water'] = max(0, station['resources']['water'] - water_consumed)

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
