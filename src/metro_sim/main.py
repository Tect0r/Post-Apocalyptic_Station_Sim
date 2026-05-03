#pytest -v <- run tests

#$env:PYTHONPATH="src"
# python -m metro_sim.main <- run the main function to see the initial state

from time import sleep

from metro_sim.services.state_factory import create_initial_station
from metro_sim.ui.cli import clear_console, show_station_status, show_input_options, show_upgrade_options, slot_upgrade_options
from metro_sim.services.simulation_service import simulate_next_day



def main() -> None:
    station = create_initial_station()

    while True:
        clear_console()
        show_station_status(station)
        show_input_options()
        user_input = input("")

        match user_input:
            case "1":
                print("Ressourcen zuweisen")
            case "2":
                print("Bewohner zuweisen")
            case "3":
                upgrade_station(station)
            case "4":
                print("Nächster Tag")
                simulate_next_day(station)
                input("Drücke Enter, um fortzufahren...")
            case _:
                print("Ungültige Eingabe")

def upgrade_station(station: dict) -> None:
    #Verbessert die Station basierend auf der Slot-Auswahl und aktualisiert den Stationsstatus entsprechend
    clear_console()
    show_upgrade_options()
    user_input = input("")
    match user_input:
        case "1":
            upgrade_slots(1, station)
        case "2":
            upgrade_slots(2, station)
        case "3":
            upgrade_slots(3, station)
        case "4":
            upgrade_slots(4, station)
        case "Esc":
            show_station_status(station)
            show_input_options()
        case _:
            print("Ungültige Eingabe")

def upgrade_slots(slot_number: int, station: dict) -> None:
    #Verbessert die ausgewählte Slot basierend auf der Upgrade-Auswahl und aktualisiert den Stationsstatus entsprechend
    clear_console()
    upgrade_dict = slot_upgrade_options(slot_number, station)
    user_input = input("")

    match user_input:
        case "1":
            print("Upgrade 1 ausgewählt")
        case "2":
            print("Upgrade 2 ausgewählt")
        case "3":
            print("Upgrade 3 ausgewählt")
        case "4":
            print("Upgrade 4 ausgewählt")
        case "Esc":
            upgrade_station(station)
        case _:
            print("Ungültige Eingabe")

if __name__ == "__main__":
        main()