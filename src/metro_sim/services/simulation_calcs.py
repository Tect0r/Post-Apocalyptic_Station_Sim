from metro_sim.utils.file_loader import load_balancing

def calculate_power_consumption(station: dict) -> int:
    # Berechnet den Stromverbrauch basierend auf der Infrastruktur und den zugewiesenen Arbeitern
    balancing_dict = load_balancing()
    power_consumption = 0
    # Slots von Station durchgehen
    # dict bauen mit buildings : level, assigned_workers
    # für jedes building: power_consumption += balancing_dict["power_consumption"]["power_consumption_per_worker_by_level"][building][level] * assigned_workers

    return power_consumption

def calculate_food_consumption(station: dict) -> int:
    # Berechnet den Nahrungsverbrauch basierend auf der Bevölkerung und den zugewiesenen Arbeitern
    # Nahrungsverbrauch gucken wegen pigs und mushrooms + kitchen
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

#calulation fehlen für medical, machine_shop, stalker_expedition, service_work