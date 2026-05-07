from metro_sim.utils.file_loader import load_buildings_cost_data, load_buildings_effects_data, load_map_data
import metro_sim.ui.cli as cli

def show_upgrade_overview_menu(station: dict) -> list[str]:
    cli.clear_console()

    menu = create_upgrade_menu(station)
    station_map = cli.build_station_map_lines(station=station)

    cli.print_side_by_side(menu, station_map)

    return menu

def show_upgrade_detail_menu(station: dict) -> list[str]:
    cli.clear_console()

    menu = create_building_upgrade_menu(station)
    station_map = cli.build_station_map_lines(station=station)

    cli.print_side_by_side(menu, station_map)

    return menu

def create_upgrade_menu(station: dict) -> tuple[list[str], dict[str, str]]:
    menu_lines = ["Slots:"]
    menu_actions = {}
    building_slots = station.get("slots")
    id = 1
    for slot in building_slots.values():
        menu_lines.append(f"[{id}]. {slot.get("building")} - lvl {slot.get("level")}")
        menu_actions[id] = slot.get("building")
        id += 1
    
    menu_lines.append("")
    menu_lines.append("[q] Zurück")

    return menu_lines, menu_actions

def create_possible_buildings_menu(station: dict, selected_slot: str) -> tuple[list[str], dict[str, str]]:
    menu_lines = ["Mögliche Gebäude:"]
    menu_actions = {}
    map_data = load_map_data()
    map_data = map_data.get("slots")
    allowed_building_types = map_data.get(selected_slot)["allowed_building_types"]
    id = 1
    for building_type in allowed_building_types:
        menu_lines.append(f"[{id}]. {building_type}")
        menu_actions[id] = building_type
        id += 1

    menu_lines.append("")
    menu_lines.append("[q] Zurück")

    return menu_lines, menu_actions

def create_building_upgrade_menu(station: dict, building: str, selected_slot: str) -> list[str]:
    menu_lines = [f"{building}",
                    "",
                    "Upgradekosten:"]

    building_upgrade_costs = load_buildings_cost_data()
    building_effects_data = load_buildings_effects_data()
    slots = station.get("slots")

    current_level = slots.get(selected_slot)["level"]
    building_costs = building_upgrade_costs.get(building)["upgrade_cost"][str(current_level+1)]        

    for resource_name, cost in building_costs.items():
        menu_lines.append(f"    {resource_name}: {cost}")
    menu_lines.append("")
    menu_lines.append("Upgrade-Effekt:")
    building_effects = building_effects_data[building]["effects_by_level"]

    effects_current_level = {}
    if current_level > 0:
        building_effects[str(current_level)]

    effects_new_level = building_effects[str(current_level+1)]
    effect_diff = build_upgrade_diff_lines(effects_current_level, effects_new_level)
    for line in effect_diff:
        menu_lines.append(f"    {line}")

    menu_lines.append("")
    menu_lines.append("")
    menu_lines.append("Upgraden? [y]/[n]")
    menu_lines.append("")
    menu_lines.append("[q] Zurück")

    return menu_lines

def build_upgrade_diff_lines(current_effects: dict, new_effects: dict) -> list[str]:
    lines = []

    for effect_name, new_value in new_effects.items():
        current_value = current_effects.get(effect_name)

        if current_value is None:
            lines.append(f"{effect_name}: neu {new_value}")
            continue

        difference = new_value - current_value

        if difference > 0:
            lines.append(f"{effect_name}: +{difference}")
        elif difference < 0:
            lines.append(f"{effect_name}: {difference}")
        else:
            lines.append(f"{effect_name}: unverändert")

    return lines