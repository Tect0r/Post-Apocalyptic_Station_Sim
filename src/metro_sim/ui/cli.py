
import os


def clear_console() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def show_station_status(station: dict) -> None:
    print(f"Station: {station['name']}")
    print(f"Tag: {station['day']}")
    print(f"Tag: {station['date']}")
    print()

    print("Bevölkerung")
    print(f"  Gesamt: {station['population']['total']}")
    print(f"  Arbeitsfähig: {station['population']['employed']}")
    print(f"  Nicht arbeitsfähig: {station['population']['unemployed']}")
    print()

    print("Ressourcen")
    print(f"  Nahrung: {station['resources']['food']}")
    print(f"  Wasser: {station['resources']['water']}")
    print(f"  Munition: {station['resources']['ammo']}")
    print(f"  Medikamente: {station['resources']['medicine']}")
    print(f"  Handelsressourcen: {station['resources']['trade_goods']}")
    print(f"  Stromverbrauch: {station['resources']['power_consumption']} %")
    print()

    print("Stationswerte")
    print(f"  Moral: {station['stats']['morale']}")
    print(f"  Komfort: {station['stats']['comfort']}")
    print(f"  Sicherheit: {station['stats']['safety']}")
    print(f"  Stromstabilität: {station['stats']['power_stability']}")
    print(f"  Stromstufe: {station['stats']['power_level']}")
    print()

def show_input_options() -> None:
    print("Optionen:")
    print("1. Ressourcen zuweisen")
    print("2. Bewohner zuweisen")
    print("3. Station verbessern")
    print("4. Nächster Tag")

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