import math
import metro_sim.utils.file_loader as loader
import metro_sim.services.report_service as report_service
import metro_sim.utils.utility as utility


def consume_food_by_mix(station: dict, needed_food_units: int, food_weights: dict, food_values: dict, report: dict) -> dict:
    consumed = {}

    while needed_food_units > 0:
        adjusted_weights = get_available_food_weights(
            station["resources"]["food"],
            food_weights
        )

        if not adjusted_weights:
            break  # keine Nahrung mehr vorhanden

        food_consumed_this_round = 0

        for food_name, weight in adjusted_weights.items():
            target_food_units = needed_food_units * weight
            food_value = food_values[food_name]

            needed_amount = math.ceil(target_food_units / food_value)
            available_amount = station["resources"]["food"].get(food_name, 0)

            used_amount = min(needed_amount, available_amount)
            provided_food_units = used_amount * food_value

            station["resources"]["food"][food_name] -= used_amount

            report_service.add_resource_change(report, food_name, -used_amount)

            needed_food_units -= provided_food_units
            food_consumed_this_round += provided_food_units

            consumed[food_name] = consumed.get(food_name, 0) + used_amount

            if needed_food_units <= 0:
                break

        # Sicherheitscheck gegen Endlosschleife
        if food_consumed_this_round == 0:
            break

    return {
        "consumed": consumed,
        "missing_food_units": max(0, needed_food_units)
    }

def calculate_water_consumption_population(station: dict) -> int:
    # Berechnet den Wasserverbrauch basierend auf der Bevölkerung, den zugewiesenen Arbeitern und der Wasserreinigung

    balancing_dict = loader.load_balancing()
    if station['water_system']['infrastructure_status'] == "broken":
        water_consumption = station['population']['total'] * balancing_dict["water_system"]["consumption_per_person_on_failure"]
    else:
        water_consumption = 0
    return water_consumption

def calculate_water_consumption_production(station: dict) -> int:
    # calc water consumption from production each tick if water pipe is broken
    pass

def calculate_bar_consumption(station: dict) -> int:
    # Berechnet den Verbrauch von Handelsgütern basierend auf der Bevölkerung und den zugewiesenen Arbeitern
    balancing_dict = loader.load_balancing()

    # calculate food und wasser verbrauch
    # calc power usage
    # set effect status (genug essen, gutes essen, kein essen)

    return 0

def calculate_consumption_for_tick(station: dict) -> dict:
    balancing_dict = loader.load_balancing()

    report = report_service.create_empty_report()

    is_meal_time = (
        station["time"]["hour"] in balancing_dict["time"]["meal_hours"]
        and station["time"]["minute"] == 0
    )

    if is_meal_time:
        needed_food = math.ceil((station['population']['total'] * balancing_dict["food"]["consumption_per_person_per_day"])/ len(balancing_dict["time"]["meal_hours"]))
        consume_food_by_mix(station, 
                        needed_food, 
                        balancing_dict["food"]["meal_mix_weights"], 
                        balancing_dict["food"]["food_values"], 
                        report)
        
        utility.remove_resource(station, "water", calculate_water_consumption_population(station))

    return report

def get_available_food_weights(resources: dict, food_weights: dict) -> dict:
    available_weights = {}

    for food_name, weight in food_weights.items():
        if resources.get(food_name, 0) > 0:
            available_weights[food_name] = weight

    total_weight = sum(available_weights.values())

    if total_weight == 0:
        return {}

    return {
        food_name: weight / total_weight
        for food_name, weight in available_weights.items()
    }