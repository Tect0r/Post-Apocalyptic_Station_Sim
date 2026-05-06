import metro_sim.utils.file_loader as loader

def calculate_power_consumption(station: dict) -> float:
    """Berechnet den täglichen Stromverbrauch der Station in kWh."""

    building_costs = loader.load_buildings_cost_data()
    balancing = loader.load_balancing()

    worker_power = balancing["power"]["worker_consumption_kwh_per_day"]

    power_consumption = 0.0

    # Gebäude-Verbrauch
    for slot in station.get("slots", {}).values():
        building = slot.get("building")
        level = slot.get("level", 0)

        if building is None or level <= 0:
            continue

        power_consumption += building_costs[building]["kwh_per_day_by_level"][str(level)]

    # Grundverbrauch pro Bewohner
    population_total = station["population"]["total"]
    power_consumption += population_total * worker_power["base_per_person"]

    # Verbrauch durch zugewiesene Arbeiter
    employment = station.get("employment", {})

    employment_to_power_key = {
        "mushroom_production": "food_worker",
        "pig_production": "food_worker",
        "kitchen_work": "food_worker",
        "maintenance": "maintenance_worker",
        "trade_goods_production": "trade_goods_worker",
        "trading": "trader",
        "guards": "guard",
        "medical": "medical_worker",

        # aktuell keine eigenen Werte in balancing.json:
        "machine_shop": "maintenance_worker",
        "stalker_expedition": "guard",
        "service_work": "trader",
    }

    for job_name, worker_count in employment.items():
        power_key = employment_to_power_key.get(job_name)

        if power_key is None:
            continue

        power_consumption += worker_count * worker_power[power_key]

    return round(power_consumption, 2)