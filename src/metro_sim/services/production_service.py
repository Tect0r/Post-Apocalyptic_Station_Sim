from metro_sim.utils.file_loader import load_balancing, load_buildings_cost_data, load_buildings_effects_data

def calculate_mushroom_production(station: dict, effects: dict) -> int:
    # Berechnet die Pilzproduktion basierend auf den zugewiesenen Arbeitern und der Infrastruktur
    workers = station["employment"]["mushroom_production"]
    amount = workers * effects["food_per_worker"]
    return amount

def calculate_pig_production(station: dict, effects: dict) -> int:
    # Berechnet die Schweineproduktion basierend auf den zugewiesenen Arbeitern und der Infrastruktur
    workers = station["employment"]["pig_production"]
    amount = workers * effects["food_per_worker"]
    return amount

def calculate_kitchen_production(station: dict, effects: dict) -> int:
    # Berechnet die Nahrungsproduktion basierend auf den zugewiesenen Arbeitern und der Infrastruktur

    return 0

def calculate_water_production(station: dict, effects: dict) -> int:
    # Berechnet die Wasserproduktion basierend auf den zugewiesenen Arbeitern und der Wasserreinigung
    balancing_dict = load_balancing()
    if station['infrastructure_status']['water_system'] > 0:
        water_production = station['work_assignment']['water_system'] * (effects["water_per_worker_by_level"][str(station['infrastructure_levels']['water_system'])])
    else:            
        water_production = 0
    return water_production

def calculate_trade_goods_production(station: dict, effects: dict) -> int:
    # Berechnet die Produktion von Handelsgütern basierend auf den zugewiesenen Arbeitern und der Infrastruktur
    workers = station["employment"]["trade_goods_production"]
    amount = workers * effects["trade_goods_per_worker"]
    return amount

def calculate_machine_shop_production(station: dict, effects: dict) -> int:
    # Berechnet die Produktion von Ersatzteilen basierend auf den zugewiesenen Arbeitern und der Infrastruktur
    workers = station["employment"]["machine_shop"]
    amount = workers * effects["spare_parts_per_worker"]
    return amount

def calculate_medical_production(station: dict, effects: dict) -> int:
    # Berechnet die medizinische Produktion basierend auf den zugewiesenen Arbeitern und der Infrastruktur
    workers = station["employment"]["medical"]
    amount = workers * effects["medicine_per_worker"]
    return amount

def calculate_stalker_expedition_production(station: dict, effects: dict) -> int:
    # Berechnet die Produktion von Handelsgütern basierend auf den zugewiesenen Arbeitern und der Infrastruktur

    return 0

def calculate_service_work_production(station: dict, effects: dict) -> int:
    # Berechnet die Produktion von Handelsgütern basierend auf den zugewiesenen Arbeitern und der Infrastruktur
    balancing_dict = load_balancing()
    if station['infrastructure_status']['bar'] > 0:
        service_work_production = station['work_assignment']['service_work'] * (effects["production_per_worker_by_level"][str(station['infrastructure_levels']['bar'])])
    else:
        service_work_production = 0
    return service_work_production

def calculate_leadership_production(station: dict, effects: dict) -> int:
    # Berechnet die Produktion von Handelsgütern basierend auf den zugewiesenen Arbeitern und der Infrastruktur
    balancing_dict = load_balancing()
    if station['infrastructure_status']['station_leadership'] > 0:
        leadership_production = station['work_assignment']['station_leadership'] * (effects["production_per_worker_by_level"][str(station['infrastructure_levels']['station_leadership'])])
    else:
        leadership_production = 0
    return leadership_production

def calculate_generator_production(station: dict, effects: dict) -> int:
    # Berechnet die Stromproduktion basierend auf den zugewiesenen Arbeitern und der Infrastruktur
    balancing_dict = load_balancing()
    if station['infrastructure_status']['power_generation'] > 0:
        generator_production = station['work_assignment']['generator'] * (effects["production_per_worker_by_level"][str(station['infrastructure_levels']['generator'])])
    else:
        generator_production = 0
    return generator_production

def assign_workers(
    station: dict,
    building: str,
    workers: int
) -> None:
    """
    Weist eine bestimmte Anzahl von Arbeitern einem Gebäude zu, um die Produktion zu steigern.
    """

    station["employment"][building] += workers