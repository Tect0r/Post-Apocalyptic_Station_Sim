import metro_sim.utils.file_loader as loader

def calculate_ammo_consumption(station: dict) -> int:
    # Berechnet den Munitionsverbrauch basierend auf der Bevölkerung, den zugewiesenen Arbeitern und der Sicherheit
    balancing_dict = loader.load_balancing()
    ammo_consumption = station['work_assignment']['guards'] * balancing_dict["guards"]["ammo_consumption_per_guard_by_level"][str(station['infrastructure_levels']['guard_post'])]
    return ammo_consumption