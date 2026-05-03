
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
    print(f"  Stromverbrauch: {station['resources']['power_usage']}")
    print()

    print("Stationswerte")
    print(f"  Moral: {station['stats']['morale']}")
    print(f"  Komfort: {station['stats']['comfort']}")
    print(f"  Sicherheit: {station['stats']['safety']}")
    print(f"  Stromstabilität: {station['stats']['power_stability']}")
    print(f"  Stromstufe: {station['stats']['power_level']}")

    print("", flush=True)