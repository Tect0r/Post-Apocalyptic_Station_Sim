


from metro_sim.ui.cli import show_day_transition_report
from metro_sim.utils.file_loader import load_balancing
import metro_sim.services.time_service as time_service


def simulate_tick(station: dict) -> None:
    # Simuliert die Ereignisse eines einzelnen Ticks und aktualisiert den Stationsstatus entsprechend
    time_service.advance_time(station, 1)

        

def simulate_next_day(station: dict) -> None:
    ## Simuliert die Ereignisse des nächsten Tages und aktualisiert den Stationsstatus entsprechend
    #balancing_dict = load_balancing()
#
    ##Datum
#
#
    ##Produktion
    #food_produced = calcs.calculate_food_production(station)
    #water_produced = calcs.calculate_water_production(station)
    #station['ressources']['food'] += food_produced
    #station['ressources']['water'] += water_produced
#
    #food_consumed = calcs.calculate_food_consumption(station)
    #water_consumed = calcs.calculate_water_consumption(station)
    #station['ressources']['food'] = max(0, station['ressources']['food'] - food_consumed)
    #station['ressources']['water'] = max(0, station['ressources']['water'] - water_consumed)
#
    ##Trade
    #trade_goods_produced = calcs.calculate_trade_goods_production(station)
    #station['ressources']['trade_goods'] += trade_goods_produced
#
    #trade_goods_consumed, ammo_gained = calcs.calculate_trade_goods_consumption(station)
    #station['ressources']['trade_goods'] = max(0, station['ressources']['trade_goods'] - trade_goods_consumed)
    #station['ressources']['ammo'] += ammo_gained
#
    ##Stromverbrauch
    #station['ressources']['power_consumption'] = calcs.calculate_power_consumption(station)
#
    #if(station['ressources']['food'] == 0 or station['ressources']['water'] == 0):
    #    station['stats']['morale'] = max(0, station['stats']['morale'] - 10)
    #    station['stats']['safety'] = max(0, station['stats']['safety'] - 10)
#
    ##Events
#
    #report_dict = {
    #    "day": station['day'],
    #    "date": station['date'],
    #    "food_consumed": food_consumed,
    #    "water_consumed": water_consumed,
    #    "food_produced": food_produced,
    #    "water_produced": water_produced,
    #    "trade_goods_produced": trade_goods_produced,
    #    "morale": station['stats']['morale'],
    #    "safety": station['stats']['safety']
    #}
#
    #show_day_transition_report(station, report_dict)
    pass
