import metro_sim.utils.file_loader as loader

def assign_workers_to_slot(station: dict, slot_id: str, worker_amount: int) -> None:
    slot = station["slots"][slot_id]

    current_workers = slot.get("assigned_workers", 0)
    worker_difference = worker_amount - current_workers

    station["population"]["worker_unavailable"] += worker_difference
    station["population"]["worker_available"] -= worker_difference

    slot["assigned_workers"] = worker_amount

def calculate_leadership_effects(station: dict, effects: dict) -> int:
    # moral/sicherheits bonus
    # effizienz bonus auf bestimmte gebäude? oder alle? mal gucken?
    # vllt so, das man sich entscheiden muss oder so?
    return 0

def calculate_maintenance_work(station: dict, effects: dict) -> int:
    # maintenance arbeit an allem (gebäude, power_line, water_system)
    return 0

def calculate_living_quarters_capacity(station: dict) -> int:
    # Berechnet die Kapazität der Unterkünfte basierend auf der Infrastruktur
    building_effects = loader.load_buildings_effects_data()
    station_slots = station.get("slots", {}).values()
    living_quarters_capacity = 0

    for slot in station_slots:
        if slot.get("building") == "living_quarters":
            living_quarters_capacity = building_effects["living_quarters"]["effects_by_level"][str(slot.get("level", {}))]["population_capacity"]

    return living_quarters_capacity