
import os

from metro_sim.utils.file_loader import load_balancing


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
    map_lines = build_station_map_lines()

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

def build_station_map_lines() -> list[str]:
    return [
        "╔╦═══════╦═════╦════════════════╦═════╦═══════╦╗",
        "║║ GLEIS ╬═════╬║ ZUGANG NORD  ║╬═════╬ GLEIS ║║",
        "║║   v   ║     ║║              ║║     ║   ^   ║║",
        "║║   v   ║     ║║              ║║     ║   ^   ║║",
        "║║   v   ║     ╚═╦════════════╦═╝     ║   ^   ║║",
        "║║   v   ║     |o|            |o|     ║   ^   ║║",
        "║║   v   ║     | |            | |     ║   ^   ║║",
        "║║   v   ║     |o|            |o|     ║   ^   ║║",
        "║║   v   ║     | |            | |     ║   ^   ║║",
        "║║   v   ║     |o|            |o|     ║   ^   ║║",
        "║║   v   ║     | |            | |     ║   ^   ║║",
        "║║   v   ║     |o|            |o|     ║   ^   ║║",
        "║║   v   ║     | |            | |     ║   ^   ║║",
        "║║   v   ║     |o|            |o|     ║   ^   ║║",
        "║║   v   ║     | |            | |     ║   ^   ║║",
        "║║   v   ║     |o|            |o|     ║   ^   ║║",
        "║║   v   ║     | |            | |     ║   ^   ║║",
        "║║   v   ║     |o|            |o|     ║   ^   ║║",
        "║║   v   ║     | |            | |     ║   ^   ║║",
        "║║   v   ║     |o|            |o|     ║   ^   ║║",
        "║║   v   ║     | |            | |     ║   ^   ║║",
        "║║   v   ║     |o|            |o|     ║   ^   ║║",
        "║║   v   ║     | |            | |     ║   ^   ║║",
        "║║   v   ║     |o|            |o|     ║   ^   ║║",
        "║║   v   ║     | |            | |     ║   ^   ║║",
        "║║   v   ║     |o|            |o|     ║   ^   ║║",
        "║║   v   ║     | |            | |     ║   ^   ║║",
        "║║   v   ║     |o|            |o|     ║   ^   ║║",
        "║║   v   ║     | |            | |     ║   ^   ║║",
        "║║   v   ║     |o|            |o|     ║   ^   ║║",
        "║║   v   ║     ╔═╩════════════╩═╗     ║   ^   ║║",
        "║║   v   ║     ║║              ║║     ║   ^   ║║",
        "║║   v   ║     ║║              ║║     ║   ^   ║║",
        "║║ GLEIS ╬═════╬║  ZUGANG SÜD  ║╬═════╬ GLEIS ║║",
        "╚╩═══════╩═════╩════════════════╩═════╩═══════╩╝",
    ]

def build_station_status_lines(station: dict) -> list[str]:
    balancing_dict = load_balancing()
    return [
        f"Station: {station['name']}",
        f"Tag: {station['day']}",
        f"Datum: {station['date']}",
        "",
        "Bevölkerung",
            f"  Arbeitsfähig: {station['population']['employed']}",
            f"  Kinder: {station['population']['children']}",
            f"  Alte: {station['population']['elderly']}",
        "",
        "Ressourcen",
            f"  Nahrung: {station['resources']['food']}",
            f"  Wasser: {station['resources']['water']}",
            f"  Munition: {station['resources']['ammo']}",
            f"  Medikamente: {station['resources']['medicine']}",
            f"  Handelsressourcen: {station['resources']['trade_goods']}",
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