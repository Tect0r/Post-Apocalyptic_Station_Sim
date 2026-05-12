import metro_sim.utils.file_loader as loader
import math

def calculate_building_wear(slot: dict, balancing_dict: dict, is_nighttime: bool) -> float:
    if slot.get("building") is None or slot.get("level", 0) <= 0:
        return 0
    
    if is_nighttime:
        return balancing_dict["maintenance"]["night_wear_per_tick"]

    workers = slot.get("assigned_workers", 0)

    if workers <= 0:
        return balancing_dict["maintenance"]["idle_wear_per_tick"]

    return (
        balancing_dict["maintenance"]["active_wear_base_value"]
        + workers * balancing_dict["maintenance"]["assigned_workers_value"]
    )

def apply_infrastructure_wear(station: dict, balancing_dict: dict) -> None:
    new_water_condition = station["water_system"]["maintenance_condition"] - balancing_dict["maintenance"]["water_system_wear"]
    station["water_system"]["maintenance_condition"] = max(0,  round(new_water_condition, 2))

    new_power_condition = station["power"]["maintenance_condition"] - balancing_dict["maintenance"]["power_line_wear"]
    station["power"]["maintenance_condition"] = max(0, round(new_power_condition, 2))

def calc_and_apply_building_maintenance(
    maintenance_targets: dict,
    worker_amount: int,
    balancing_dict: dict,
    report: dict | None = None
) -> None:
    
    if maintenance_targets is None:
        return

    max_workers_per_target = balancing_dict["maintenance"]["max_worker_per_building"]
    repair_per_worker_per_tick = balancing_dict["maintenance"]["repair_per_worker_per_tick"]

    remaining_workers = worker_amount

    for target_id, target_data in maintenance_targets.items():
        if remaining_workers <= 0:
            break

        target = target_data["target"]

        workers_for_target = min(remaining_workers, max_workers_per_target)
        amount_repaired = workers_for_target * repair_per_worker_per_tick

        old_condition = target.get("maintenance_condition", 100)
        new_condition = min(100, old_condition + amount_repaired)
        actual_repair = new_condition - old_condition

        target["maintenance_condition"] = new_condition

        #TODO: add report

        remaining_workers -= workers_for_target

def find_buildings_for_maintenance(station: dict, worker_amount: int, balancing_dict: dict) -> dict:
    if worker_amount <= 0:
        return {}

    maintenance_candidates = {}

    # Infrastruktur zuerst prüfen
    if station["water_system"]["maintenance_condition"] <= balancing_dict["maintenance"]["water_system_threshold"]:
        maintenance_candidates["water_system"] = {
            "type": "infrastructure",
            "target": station["water_system"],
            "condition": station["water_system"]["maintenance_condition"],
            "priority": 0
        }

    if station["power"]["maintenance_condition"] <= balancing_dict["maintenance"]["power_line_threshold"]:
        maintenance_candidates["power"] = {
            "type": "infrastructure",
            "target": station["power"],
            "condition": station["power"]["maintenance_condition"],
            "priority": 0
        }

    # Gebäude sammeln
    for slot_id, slot in station.get("slots", {}).items():
        if slot.get("building") is None:
            continue

        if slot.get("level", 0) <= 0:
            continue

        if slot.get("maintenance_condition", 100) >= 100:
            continue

        maintenance_candidates[slot_id] = {
            "type": "building",
            "target": slot,
            "condition": slot.get("maintenance_condition", 100),
            "priority": 1
        }

    max_workers_per_target = balancing_dict["maintenance"]["max_worker_per_building"]
    amount_to_choose = math.ceil(worker_amount / max_workers_per_target)

    sorted_candidates = dict(
        sorted(
            maintenance_candidates.items(),
            key=lambda item: (item[1]["priority"], item[1]["condition"])
        )
    )

    chosen_targets = {}

    for target_id, target_data in sorted_candidates.items():
        if len(chosen_targets) >= amount_to_choose:
            break

        chosen_targets[target_id] = target_data

    return chosen_targets

def apply_maintenance_worker(station: dict, balancing_dict: dict, buildings_for_maintenance: dict, report: dict) -> None:
    worker_amount = get_maintenance_worker_amount(station)

    calc_and_apply_building_maintenance(buildings_for_maintenance, worker_amount, balancing_dict, report)

def maintenance_per_tick(station: dict, is_nighttime: bool) -> None:
    balancing_dict = loader.load_balancing()    

    report = {} #TODO: put report in method header

    for slot_id, slot in station.get("slots").items():
        calced_wear = calculate_building_wear(slot, balancing_dict, is_nighttime)
        new_condition = slot.get("maintenance_condition", 100) - calced_wear
        slot["maintenance_condition"] = max(0, round(new_condition, 2))
    
    apply_infrastructure_wear(station, balancing_dict)
    apply_maintenance_worker(station, balancing_dict, station["maintenance"]["daily_targets"], report)

def assign_daily_maintenance_targets(station: dict) -> None:
    balancing_dict = loader.load_balancing() 
    worker_amount = get_maintenance_worker_amount(station)

    station["maintenance"]["daily_targets"] = find_buildings_for_maintenance(
        station,
        worker_amount,
        balancing_dict
    )

def get_maintenance_worker_amount(station: dict) -> int:
    worker_amount = 0

    for slot_id, slot in station["slots"].items():
        if slot["building"] == "maintenance":
            worker_amount += slot["assigned_workers"]
    
    return worker_amount


def calculate_building_failure() -> bool:
    #randomize, je nach condition
    #75–100: normal
    #50–74: erhöhtes Ausfallrisiko
    #25–49: hohes Ausfallrisiko
    #1–24: kritisch, starke Ausfallgefahr
    #0: broken
    pass

def get_condition_status(condition: float) -> str:
    if condition <= 0:
        return "Ausgefallen"
    if condition <= 24:
        return "Kritisch"
    if condition <= 49:
        return "Stark beschädigt"
    if condition <= 74:
        return "Angeschlagen"
    return "Stabil"