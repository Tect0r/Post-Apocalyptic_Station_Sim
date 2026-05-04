
import os

from metro_sim.utils.file_loader import load_balancing, load_map_data, load_buildings_data


def clear_console() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def print_side_by_side(left_lines: list[str], right_lines: list[str], left_width: int = 45) -> None:
    max_lines = max(len(left_lines), len(right_lines))

    for index in range(max_lines):
        left = left_lines[index] if index < len(left_lines) else ""
        right = right_lines[index] if index < len(right_lines) else ""

        print(f"{left:<{left_width}} {right}")

def show_station_overview(station: dict) -> None:
    left_lines = build_station_status_lines(station)
    left_lines += [""]
    left_lines += build_input_option_lines()
    map_lines = build_station_map_lines(station=station)

    print_side_by_side(left_lines, map_lines)

def build_input_option_lines() -> list[str]:
    return [
        "Optionen:",
        "1. Ressourcen zuweisen",
        "2. Bewohner zuweisen",
        "3. Station verbessern",
        "4. Nächster Tag"
    ]

def show_upgrade_options() -> None:
    print("Station (Wähle einen Slot zum verbessern):")
    print("Slot 1: Leer")
    print("Slot 2: Leer")
    print("Slot 3: Leer")
    print("Slot 4: Leer")
    print("")
    print("Esc: Zurück zum Hauptmenü")

def slot_upgrade_options(slot_number: int, station: dict) -> None:
    clear_console()
    print(f"Upgrade-Optionen für Slot {slot_number}:")
    print("1. Upgrade 1")
    print("2. Upgrade 2")
    print("3. Upgrade 3")
    print("4. Upgrade 4")
    print("")
    print("Esc: Zurück zum Stationsmenü")

    upgrade_dict = {}

    return upgrade_dict

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

def build_station_map_lines(station: dict | None = None) -> list[str]:
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

            if current_building is None:
                template = slot_data.get("empty_template")

                if template is None:
                    raise ValueError(f"Slot '{slot_id}' hat kein empty_template.")

            else:
                if building_slots is None:
                    template = slot_data.get("upgrade_template")

                    if template is None:
                        raise ValueError(f"Slot '{slot_id}' hat kein upgrade_template.")
                else:
                    orientation = slot_data["orientation"]

                    try:
                        template = building_slots["buildings"][current_building][orientation]
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

def build_station_status_lines(station: dict) -> list[str]:
    balancing_dict = load_balancing()
    return [
        f"Station: {station['name']}",
        f"Tag: {station['day']}",
        f"Datum: {station['date']}",
        "",
        "Bevölkerung",
            f"  Arbeitsfähig: {station['population']['employed']}",
            f"  Unbeschäftigt: {station['population']['unemployed']}",
            f"  Kinder: {station['population']['children']}",
            f"  Alte: {station['population']['elderly']}",
        "",
        "Ressourcen",
            f"  Nahrung:",
            f"    Pilze: {station['resources']['mushrooms']}",
            f"    Schweine: {station['resources']['pigs']}",
            f"  Wasser: {station['resources']['water']}",
            f"  Munition: {station['resources']['ammo']}",
            f"  Medikamente: {station['resources']['medicine']}",
            f"  Handelsressourcen: {station['resources']['trade_goods']}",
            f"  Ersatzteile: {station['resources']['spare_parts']}",
            f"  Stromverbrauch: {station['resources']['power_consumption']} kWh / {balancing_dict['power']['contracts'][station['stats']['power_contract']]["kwh_per_day"]} kWh",
        "",
        "Stationswerte",
            f"  Moral: {station['stats']['morale']}",
            f"  Komfort: {station['stats']['comfort']}",
            f"  Sicherheit: {station['stats']['safety']}",
            f"  Stromstabilität: {station['stats']['power_stability']}",
            f"  Stromstufe: {station['stats']['power_contract']}",
        "",
    ]