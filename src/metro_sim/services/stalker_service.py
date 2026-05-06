import metro_sim.utils.file_loader as loader

def calculate_stalker_expedition_production(station: dict, effects: dict) -> int:
    # Berechnet die Produktion von Handelsgütern basierend auf den zugewiesenen Arbeitern und der Infrastruktur

    return 0

def calculate_stalker_den_consumption(station: dict) -> int:
    # Berechnet den Verbrauch von Handelsgütern basierend auf der Bevölkerung und den zugewiesenen Arbeitern
    balancing_dict = loader.load_balancing()
    stalker_den_consumption = station['work_assignment']['stalker_expedition'] * balancing_dict["stalker_den"]["trade_goods_consumption_per_worker_by_level"][str(station['infrastructure_levels']['stalker_den'])]
    return stalker_den_consumption