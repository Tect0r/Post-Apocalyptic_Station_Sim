import metro_sim.utils.file_loader as loader
from metro_sim.core.action_result import ActionResult

def upgrade_building(station: dict, building: str, selected_slot: str) -> ActionResult:
    
    slot = station["slots"][selected_slot]

    if slot["building"] is not None and slot["building"] != building:
        return ActionResult(False, "slot_has_different_building")
    
    building_costs_data = loader.load_buildings_cost_data()
    current_level = slot["level"]
    new_level = current_level + 1

    if new_level > 3:
        return ActionResult(False, "slot_is_max_level")

    building_costs = building_costs_data[building]["upgrade_cost"][str(new_level)]
    player_resources = station["resources"]["mechanical"]
    
    can_afford_ActionResult = can_afford(player_resources, building_costs)
    
    if not can_afford_ActionResult.success:
        return ActionResult(False, can_afford_ActionResult["msg"])

    pay_resources(player_resources, building_costs)

    station["slots"][selected_slot] = {
        "building": building,
        "level": new_level,
        "production_progress": 0
    }

    return ActionResult(True, "slot_upgraded")

def demolish_building(station: dict, building: str, selected_slot: str) -> ActionResult:
    #ausgewältes gebäude wird zerstört
    # ressourcen werden anteilhaft vom letzten upgrade zurück gegeben (50% oder so)
    pass

def can_afford(resources: dict, costs: dict) -> ActionResult:
    for resource_name, needed_amount in costs.items():
        available_amount = resources.get(resource_name, 0)

        if available_amount < needed_amount:
            return ActionResult(False, f"missing_{resource_name}")

    return ActionResult(True, "can_pay_resources")


def pay_resources(resources: dict, costs: dict) -> None:
    for resource_name, amount in costs.items():
        resources[resource_name] -= amount

def salvage_resources(resources: dict, costs: dict) -> None:
    balancing_dict = loader.load_balancing()
    for resource_name, amount in costs.items():
        resources[resource_name] += amount * balancing_dict["building_demolishing"]["salvaged_resource_percentage"]