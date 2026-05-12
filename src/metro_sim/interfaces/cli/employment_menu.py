import metro_sim.interfaces.cli.cli as cli
import metro_sim.utils.file_loader as loader

def show_employment_menu(station: dict) -> list[str]:
    cli.clear_console()

    menu = create_employment_menu(station)
    station_map = cli.build_station_map_lines(station=station)

    cli.print_side_by_side(menu, station_map)

    return menu

def create_employment_detail_menu(station: dict, selected_slot_id: str) -> str:
    selected_slot = station["slots"][selected_slot_id]
    building = selected_slot.get("building")
    current_workers = selected_slot.get("assigned_workers", 0)
    current_level = str(selected_slot.get("level"))
    building_data = loader.load_production_data()[building]["levels"][current_level]
    
    return [
        "",
        f"Ausgewählter Slot: {selected_slot_id}",
        f"Gebäude: {building}",
        f"Aktuelle Arbeiter: {current_workers} / {building_data["max_workers"]}",
        f"Verfügbare Arbeiter: {station['population']['worker_available']}",
        "",
        "[q] Zurück"
    ]

def create_employment_menu(station: dict) -> tuple[list[str], dict[str, str]]:
    station_slots = station.get("slots", {})

    building_to_label = {
        "tunnel_scavenging": "Tunnel scavenging",
        "mushroom_farm": "Pilzfarm",
        "pig_farm": "Schweinefarm",
        "kitchen": "Küche",
        "maintenance": "Wartung",
        "trading_goods": "Handelswarenproduktion",
        "trading_post": "Handelsposten",
        "guard_post": "Wachposten",
        "medical": "Medizin",
        "machine_shop": "Werkstatt",
        "stalker_den": "Stalker-Quartier",
        "bar": "Bar",
        "market": "Markt",
        "generator": "Generator",
        "station_leadership": "Stationsleitung",
        "weapon_chamber": "Waffenkammer",
        "storage": "Lager",
        "living_quarters": "Unterkünfte",
    }

    worker_buildings = {
        "tunnel_scavenging",
        "mushroom_farm",
        "pig_farm",
        "kitchen",
        "maintenance",
        "trading_goods",
        "trading_post",
        "guard_post",
        "medical",
        "machine_shop",
        "stalker_den",
        "bar",
        "market",
        "generator",
        "station_leadership",
        "weapon_chamber",
    }

    menu_lines = ["Bewohner zuweisen:"]
    menu_actions = {}

    menu_index = 0

    for slot_id, slot in station_slots.items():
        building = slot.get("building")
        level = slot.get("level", 0)
        assigned_workers = slot.get("assigned_workers", 0)

        if building is None or level <= 0:
            continue

        if building not in worker_buildings:
            continue

        label = building_to_label.get(building, building)

        key = str(menu_index)
        menu_lines.append(
            f"[{key}]. {slot_id} - {label} L{level} - Arbeiter: {assigned_workers}"
        )
        menu_actions[key] = slot_id

        menu_index += 1

    menu_lines.append("")
    menu_lines.append("[q] Zurück")

    return menu_lines, menu_actions