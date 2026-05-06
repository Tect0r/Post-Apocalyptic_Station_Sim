import metro_sim.utils.file_loader as loader

def upgrade_building(station: dict, building: str, selected_slot: str) -> bool:
    
    slot = station["slots"][selected_slot]

    if slot["building"] is not None and slot["building"] != building:
        return False
    
    building_costs_data = loader.load_buildings_cost_data()
    current_level = slot["level"]
    new_level = current_level + 1

    if new_level > 3:
        return False

    building_costs = building_costs_data[building]["upgrade_cost"][str(new_level)]
    player_ressources = station["ressources"]

    if not can_afford(player_ressources, building_costs):
        return False

    pay_ressources(player_ressources, building_costs)

    station["slots"][selected_slot] = {
        "building": building,
        "level": new_level,
        "production_progress": 0
    }

    return True

def can_afford(ressources: dict, costs: dict) -> bool:
    for resource_name, needed_amount in costs.items():
        available_amount = ressources.get(resource_name, 0)

        if available_amount < needed_amount:
            return False

    return True


def pay_ressources(ressources: dict, costs: dict) -> None:
    for resource_name, amount in costs.items():
        ressources[resource_name] -= amount