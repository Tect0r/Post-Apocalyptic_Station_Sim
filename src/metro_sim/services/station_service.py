import metro_sim.utils.file_loader as loader

def assign_workers(
    station: dict,
    building: str,
    workers: int
) -> None:
    """
    Weist eine bestimmte Anzahl von Arbeitern einem Gebäude zu, um die Produktion zu steigern.
    """

    station["employment"][building] += workers
    
    station["population"]["employed"] += workers
    station["population"]["unemployed"] -= workers

def calculate_leadership_production(station: dict, effects: dict) -> int:
    # Berechnet die Produktion von Handelsgütern basierend auf den zugewiesenen Arbeitern und der Infrastruktur
    balancing_dict = loader.load_balancing()
    if station['infrastructure_status']['station_leadership'] > 0:
        leadership_production = station['work_assignment']['station_leadership'] * (effects["production_per_worker_by_level"][str(station['infrastructure_levels']['station_leadership'])])
    else:
        leadership_production = 0
    return leadership_production

def calculate_service_work_production(station: dict, effects: dict) -> int:
    # Berechnet die Produktion von Handelsgütern basierend auf den zugewiesenen Arbeitern und der Infrastruktur
    balancing_dict = loader.load_balancing()
    if station['infrastructure_status']['bar'] > 0:
        service_work_production = station['work_assignment']['service_work'] * (effects["production_per_worker_by_level"][str(station['infrastructure_levels']['bar'])])
    else:
        service_work_production = 0
    return service_work_production

def calculate_living_quarters_capacity(station: dict) -> int:
    # Berechnet die Kapazität der Unterkünfte basierend auf der Infrastruktur
    building_effects = loader.load_buildings_effects_data()
    station_slots = station.get("slots", {}).values()
    for slot in station_slots:
        if slot.get("building") == "living_quarters":
            living_quarters_capacity = building_effects["living_quarters"]["effects_by_level"][str(slot.get("level", {}))]["population_capacity"]

    return living_quarters_capacity