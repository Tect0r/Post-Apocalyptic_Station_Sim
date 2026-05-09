import metro_sim.utils.file_loader as loader

def upgrade_building(station: dict, building: str, selected_slot: str) -> {bool, str}:
    
    slot = station["slots"][selected_slot]

    if slot["building"] is not None and slot["building"] != building:
        return {"success" : False, "msg" : "Slots ist bereits belegt."}
    
    building_costs_data = loader.load_buildings_cost_data()
    current_level = slot["level"]
    new_level = current_level + 1

    if new_level > 3:
        return {"success" : False, "msg" : "Slot ist bereits auf dem maixmalen Level."}

    building_costs = building_costs_data[building]["upgrade_cost"][str(new_level)]
    player_resources = station["resources"]
    
    can_afford_dict = can_afford(player_resources, building_costs)
    
    if not can_afford_dict["success"]:
        return {"success" : False, "msg" : can_afford_dict["msg"]}

    pay_resources(player_resources, building_costs)

    station["slots"][selected_slot] = {
        "building": building,
        "level": new_level,
        "production_progress": 0
    }

    return {"success" : True, "msg" : "Gebäude erfolgreich geupgraded."}

def demolish_building(station: dict, building: str, selected_slot: str) -> {bool, str}:
    #ausgewältes gebäude wird zerstört
    # ressourcen werden anteilhaft vom letzten upgrade zurück gegeben (50% oder so)
    pass

def can_afford(resources: dict, costs: dict) -> {bool, str}:
    for resource_name, needed_amount in costs.items():
        available_amount = resources.get(resource_name, 0)

        if available_amount < needed_amount:
            return {"success" : False, "msg" : f"Es fehlt: {resource_name}"}

    return {"success" : True, "msg" : f"Alle Ressource sind vorrätig."}


def pay_resources(resources: dict, costs: dict) -> None:
    for resource_name, amount in costs.items():
        resources[resource_name] -= amount

def salvage_resources(resources: dict, costs: dict) -> None:
    balancing_dict = loader.load_balancing()
    for resource_name, amount in costs.items():
        resources[resource_name] += amount * balancing_dict["building_demolishing"]["salvaged_resource_percentage"]