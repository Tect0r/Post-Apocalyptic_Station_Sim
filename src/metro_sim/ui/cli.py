import os
from metro_sim.utils.file_loader import load_balancing, load_map_data, load_buildings_data
import metro_sim.services.station_service as station_service
import re

ANSI_PATTERN = re.compile(r"\033\[[0-9;]*m")

def visible_len(text: str) -> int:
    return len(ANSI_PATTERN.sub("", text))

def pad_ansi(text: str, width: int) -> str:
    padding = max(0, width - visible_len(text))
    return text + " " * padding

def clear_console() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def print_side_by_side(left_lines: list[str], right_lines: list[str], left_width: int = 45) -> None:
    max_lines = max(len(left_lines), len(right_lines))

    for index in range(max_lines):
        left = left_lines[index] if index < len(left_lines) else ""
        right = right_lines[index] if index < len(right_lines) else ""

        print(f"{pad_ansi(left, left_width)} {right}")

def show_station_overview(station: dict, last_report: dict | None = None) -> None:
    left_lines = build_station_status_lines(station, last_report)
    map_lines = build_station_map_lines(station=station)

    print_side_by_side(left_lines, map_lines)

def show_day_transition_report(station: dict, report_dict : dict) -> None:
    clear_console()
    print("Der nächste Tag bricht an...")
    print(f"Tag: {report_dict['day']} - Datum: {report_dict['date']}")
    print(f"Ressourcenverbrauch: Nahrung: {report_dict['food_produced']-report_dict['food_consumed']}, Wasser: {report_dict['water_produced']-report_dict['water_consumed']}")
    print(f"Produktion: Handelsressourcen: {report_dict['trade_goods_produced']}")
    print(f"Handel: tbd")

    if station['stats']['morale'] < 30 and station['stats']['morale'] > 0:
        print("Die Moral der Bewohner ist kritisch niedrig! Versuche, die Moral zu verbessern, um Unruhen zu vermeiden.")

    if station['stats']['morale'] == 0:
        print("Die Moral der Bewohner ist auf 0 gesunken! Es kommt zu Unruhen und Plünderungen in der Station!")

    print("")

def color_lines(lines: list[str], color: str) -> list[str]:
    GREEN = "\033[32m"
    RESET = "\033[0m"
    return [f"{color}{line}{GREEN}" for line in lines]

def build_station_map_lines(station: dict | None = None, 
                            upgrade_mode : bool = False, 
                            selected_slot : str | None = None) -> list[str]:
    result_map = []

    map_data = load_map_data()
    buildings_data = load_buildings_data()

    if station is None:
        station = {"slots": {}}

    station_slots = station.get("slots", {})
    map_slots = map_data.get("slots", {})
    building_slots = buildings_data.get("buildings", {})

    slot_ids = list(map_slots.keys())
    slots_per_row = 3

    for i in range(0, len(slot_ids), slots_per_row):
        row_slot_ids = slot_ids[i:i + slots_per_row]
        templates = []

        for slot_id in row_slot_ids:
            slot_data = map_slots[slot_id]
            current_slot = station_slots.get(slot_id)
            current_building = current_slot.get("building") if current_slot else None

            if current_building is None and not upgrade_mode:
                template = slot_data.get("empty_template")

                if template is None:
                    raise ValueError(f"Slot '{slot_id}' hat kein empty_template.")
            
            elif current_building is None and upgrade_mode:
                template = slot_data.get("upgrade_template")

                if selected_slot is not None and selected_slot == slot_id:
                    template = [f"\033[32m{line}\033[0m" for line in template]

                if template is None:
                    raise ValueError(f"Slot '{slot_id}' hat kein upgrade_template.")
            else:
                if building_slots is None:
                    template = slot_data.get("upgrade_template")

                    if template is None:
                        raise ValueError(f"Slot '{slot_id}' hat kein upgrade_template.")
                else:
                    orientation = slot_data["orientation"]

                    try:
                        template = building_slots[current_building]["templates"][orientation]
                    except KeyError:
                        raise ValueError(
                            f"Kein Template für building='{current_building}' "
                            f"mit orientation='{orientation}' in Slot '{slot_id}'."
                        )

            templates.append(template)

        if not templates:
            continue

        height = len(templates[0])

        for template in templates:
            if len(template) != height:
                raise ValueError("Alle Templates in einer Slot-Reihe müssen dieselbe Höhe haben.")

        for line_index in range(height):
            combined_line = ""

            for template in templates:
                combined_line += template[line_index]

            result_map.append(combined_line)

    return result_map

def format_resource_change(report: dict | None, resource_name: str) -> str:
    if report is None:
        return ""

    change = report.get("resource_changes", {}).get(resource_name, 0)

    if change > 0:
        return f" \033[32m+{change}\033[0m"
    if change < 0:
        return f" \033[31m{change}\033[0m"

    return ""

def build_station_status_lines(station: dict, report: dict | None) -> list[str]:
    balancing_dict = load_balancing()
    power_contract = station["stats"]["power_contract"]
    available_power = balancing_dict["power"]["contracts"][power_contract]["kwh_per_day"]
    return [
        f"Station: {station['name']}",
        f"Tag: {station['time']['day']}",
        f"Datum: {station['time']['date']}",
        f"Uhrzeit: {station['time']['hour']:02d}:{station['time']['minute']:02d}",
        "",
        f"Unterkünfte:",
            f"Bewohner: {station['population']['total']}",
            f"Obdachlos: {max(0, station['population']['total'] - station_service.calculate_living_quarters_capacity(station))}",
        "",
        "Bevölkerung",
            f"  Arbeitsfähig: {station['population']['employed']}",
            f"  Unbeschäftigt: {station['population']['unemployed']}",
            f"  Kinder: {station['population']['children']}",
            f"  Alte: {station['population']['elderly']}",
        "",
        "Ressourcen",
        f"  Nahrung:",
        f"    Pilze: {station['ressources']['mushrooms']}{format_resource_change(report, 'mushrooms')}",
        f"    Schweine: {station['ressources']['pigs']}{format_resource_change(report, 'pigs')}",
        f"  Wasser: {station['ressources']['water']}{format_resource_change(report, 'water')}",
        f"  Munition: {station['ressources']['ammo']}{format_resource_change(report, 'ammo')}",
        f"  Medikamente: {station['ressources']['medicine']}{format_resource_change(report, 'medicine')}",
        f"  Handelsressourcen: {station['ressources']['trade_goods']}{format_resource_change(report, 'trade_goods')}",
        f"  Ersatzteile: {station['ressources']['spare_parts']}{format_resource_change(report, 'spare_parts')}",
        f"  Stromverbrauch: {station['ressources']['power_consumption']} kWh / {available_power} kWh",
        "",
        "Stationswerte",
            f"  Moral: {station['stats']['morale']}",
            f"  Komfort: {station['stats']['comfort']}",
            f"  Sicherheit: {station['stats']['safety']}",
            f"  Stromstabilität: {station['stats']['power_stability']}",
            f"  Stromstufe: {power_contract}",
        "",
    ]