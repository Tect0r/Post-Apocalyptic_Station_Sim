import metro_sim.utils.file_loader as loader
import metro_sim.services.report_service as report_service
import random
import metro_sim.utils.utility as utility

def calculate_production_for_tick(station: dict) -> dict:
    """
    Berechnet die Produktion für einen einzelnen Tick.

    Für jeden belegten und funktionierenden Gebäudeslot wird der
    Produktionsfortschritt erhöht. Die Höhe des Fortschritts hängt von
    den zugewiesenen Arbeitern und dem Gebäudewert
    `work_per_worker_per_tick` ab.

    Sobald `production_progress` den Wert `work_required` erreicht,
    wird ein Produktionszyklus abgeschlossen. Dann werden benötigte
    Ressourcen verbraucht, erzeugte Ressourcen hinzugefügt und die
    Änderungen in einem Report gespeichert.
    """

    building_slots = station.get("slots", {})
    production_data = loader.load_production_data()
    balancing_dict = loader.load_balancing()
    report = report_service.create_empty_report()

    for slot_id, slot in building_slots.items():
        building = slot.get("building")
        level = slot.get("level", 0)
        building_status = slot.get("building_status", "working")
        assigned_workers = slot.get("assigned_workers", 0)

        if building is None or level <= 0:
            continue

        if building_status == "broken":
            continue

        if assigned_workers <= 0:
            continue

        level_key = str(level)
        prod_per_building_level = production_data[building]["levels"][level_key]

        work_required = prod_per_building_level["work_required"]
        work_per_worker = prod_per_building_level["work_per_worker_per_tick"]

        slot["production_progress"] += assigned_workers * work_per_worker

        if slot["production_progress"] < work_required:
            continue

        needs = prod_per_building_level["base"]["needs"]
        gives = prod_per_building_level["base"]["gives"]

        if not check_needs_for_production(station, needs):
            continue
        
        while slot["production_progress"] > work_required:
            slot["production_progress"] -= work_required

            consume_resources_for_production(station, needs, report)

            if building == "tunnel_scavenging":
                if random.randint(1, 100) <= balancing_dict["tunnel_scavenging"]["chance_to_loot"]:
                    loot_chances = balancing_dict["tunnel_scavenging"]["resource_ratio"]
                    given_resource = choose_weighted_resource(loot_chances)

                    amount = gives.get(given_resource, 0)
                    gives = {given_resource: amount}
                else:
                    gives = {}

            add_resources_from_production(station, gives, report)

            # TODO: Boosts berechnen und anwenden
            # TODO: Effekte wie morale_points, comfort_points usw. getrennt behandeln

    return report

def choose_weighted_resource(resource_chances: dict[str, float]) -> str:
    resources = list(resource_chances.keys())
    weights = list(resource_chances.values())

    return random.choices(resources, weights=weights, k=1)[0]

def check_needs_for_production(station: dict, needs_for_level: dict) -> bool:
    for resource_name, required_amount in needs_for_level.items():
        available_amount = utility.get_resource_amount(station, resource_name)

        if available_amount < required_amount:
            return False

    return True

def consume_resources_for_production(station: dict, costs: dict, report: dict) -> None:
    for resource_name, amount in costs.items():
        remove_resource(station, resource_name, amount)
        report_service.add_resource_change(report, resource_name, -amount)

def add_resources_from_production(station: dict, gains: dict, report: dict) -> None:
    for resource_name, amount in gains.items():
        utility.add_resource(station, resource_name, amount)
        report_service.add_resource_change(report, resource_name, amount)

def remove_resource(station: dict, resource_name: str, amount: int | float) -> None:
    category = utility.get_resource_category(resource_name)

    station["resources"][category][resource_name] = max(
        0,
        station["resources"][category].get(resource_name, 0) - amount
    )
