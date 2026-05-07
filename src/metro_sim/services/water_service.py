import metro_sim.utils.file_loader as loader

def calculate_water_production(station: dict, effects: dict) -> int:
    # Berechnet die Wasserproduktion basierend auf den zugewiesenen Arbeitern und der Wasserreinigung
    balancing_dict = loader.load_balancing()
    if station['infrastructure_status']['water_system'] > 0:
        water_production = station['work_assignment']['water_system'] * (effects["water_per_worker_by_level"][str(station['infrastructure_levels']['water_system'])])
    else:            
        water_production = 0
    return water_production