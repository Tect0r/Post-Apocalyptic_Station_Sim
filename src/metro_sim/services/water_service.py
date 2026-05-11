import metro_sim.utils.file_loader as loader

def calculate_water_consumption_population(station: dict) -> int:
    # Berechnet den Wasserverbrauch basierend auf der Bevölkerung, den zugewiesenen Arbeitern und der Wasserreinigung

    balancing_dict = loader.load_balancing()
    if station['water_system']['infrastructure_status'] == "broken":
        water_consumption = station['population']['total'] * balancing_dict["water_system"]["consumption_per_person_on_failure"]
    else:
        water_consumption = 0
    return water_consumption


def calculate_consumption_by_progress(
    previous_progress: int,
    new_progress: int,
    work_required: int,
    total_needed: int
) -> int:
    if total_needed <= 0:
        return 0

    work_per_unit = work_required / total_needed

    previous_units = int(previous_progress // work_per_unit)
    new_units = int(new_progress // work_per_unit)

    return new_units - previous_units