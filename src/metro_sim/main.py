#pytest -v <- run tests

#$env:PYTHONPATH="src"
# python -m metro_sim.main <- run the main function to see the initial state

import msvcrt
from time import sleep

from metro_sim.utils.file_loader import load_balancing
from metro_sim.utils.utility import ask_until_valid
from metro_sim.services.state_factory import create_initial_station
from metro_sim.services.tick_service import calculate_next_tick
from metro_sim.services.station_service import assign_workers
from metro_sim.services.upgrade_service import upgrade_building
from metro_sim.ui.production_menu import create_employment_menu
from metro_sim.ui.upgrade_menu import create_building_upgrade_menu, create_upgrade_menu, create_possible_buildings_menu
from metro_sim.ui.cli import clear_console, show_station_overview, build_station_map_lines, print_side_by_side


def key_pressed() -> str | None:
    if msvcrt.kbhit():
        return msvcrt.getwch().lower()
    return None


def wait_with_pause_check(seconds: int | float) -> str | None:
    step = 0.1
    elapsed = 0.0

    while elapsed < seconds:
        key = key_pressed()

        if key is not None:
            return key

        sleep(step)
        elapsed += step

    return None


def show_pause_menu() -> str:
    print()
    print("Simulation pausiert")
    print("[Enter] Fortsetzen")
    print("")
    print("[1] Bewohner zuweisen")
    print("[2] Station verbessern")
    print("[3] Handel")
    print("")
    print("[q] Beenden")
    return input("> ").lower()

def handle_employment_menu(station: dict) -> None:
    menu_lines, menu_actions = create_employment_menu(station)

    clear_console()

    station_map = build_station_map_lines(station=station)
    print_side_by_side(menu_lines, station_map)

    user_input = input("> ")

    if user_input == "0":
        return

    selected_job = menu_actions.get(user_input)

    if selected_job is None:
        print("Ungültige Eingabe")
        input("Enter zum Fortfahren...")
        return

    amount_input = input("Wie viele Bewohner zuweisen? > ")

    if not amount_input.isdigit():
        print("Ungültige Zahl")
        input("Enter zum Fortfahren...")
        return

    amount = int(amount_input)

    if amount < 0 or amount > station["population"]["unemployed"]:
        print("Ungültige Anzahl")
        input("Enter zum Fortfahren...")
        return
    
    assign_workers(station, selected_job, amount)

    print(f"{amount} Bewohner wurden zugewiesen: {selected_job}")
    input("Enter zum Fortfahren...")

def handle_upgrade_overview_menu(station: dict) -> None:
    clear_console()

    menu_lines, menu_actions = create_upgrade_menu(station)
    station_map = build_station_map_lines(station=station, upgrade_mode=True)
    print_side_by_side(menu_lines, station_map)

    user_input = input("Wähle einen Slot zum upgraden. ")

    if user_input == "q":
        return

    selected_building = menu_actions.get(int(user_input))
    
    if selected_building is not None:
        handle_upgrade_detail_menu(station, selected_building, f"slot_{str(user_input)}")
    else:
        handle_build_new_building_menu(station, f"slot_{str(user_input)}")

def handle_build_new_building_menu(station: dict, selected_slot: str) -> None:
    menu_lines, menu_actions = create_possible_buildings_menu(station, selected_slot)

    clear_console()

    station_map = build_station_map_lines(station=station, upgrade_mode=True, selected_slot=selected_slot)
    print_side_by_side(menu_lines, station_map)

    user_input = input("Wähle einen Gebäude zum bauen.")

    if user_input == "q":
        return
    
    selected_building = menu_actions.get(int(user_input))
    handle_upgrade_detail_menu(station, selected_building, selected_slot)

def handle_upgrade_detail_menu(station: dict, selected_building: dict, selected_slot: str) -> None:
    menu_lines = create_building_upgrade_menu(station, selected_building, selected_slot)

    clear_console()

    station_map = build_station_map_lines(station=station, upgrade_mode=True, selected_slot=selected_slot)
    print_side_by_side(menu_lines, station_map)
    

    user_input = ask_until_valid(["q", "y", "n"] ,"Möchtest du das Gebäude upgraden?")

    if user_input == "q" or user_input == "n":
        return
    elif user_input == "y":
        upgrade_building(station, selected_building, selected_slot)
        return


def main() -> None:
    station = create_initial_station()
    balancing_dict = load_balancing()

    running = True
    paused = False
    last_report = {
        "resource_changes": {},
        "stat_changes": {},
        "messages": []
    }

    while running:
        clear_console()
        show_station_overview(station, last_report)

        if paused:
            user_input = show_pause_menu()

            match user_input:
                case "":
                    paused = False

                case "q":
                    running = False

                case "1":
                    handle_employment_menu(station)
                case "2":
                    handle_upgrade_overview_menu(station)
                
                case "3":
                    input("Enter zum Fortfahren...")
                case _:
                    print("Ungültige Eingabe")
                    input("Enter zum Fortfahren...")

        else:
            print()
            print("Simulation läuft... Taste drücken zum Pausieren.")

            pressed_key = wait_with_pause_check(
                balancing_dict["time"]["real_seconds_per_tick"]
            )

            if pressed_key is not None:
                paused = True
                continue

            new_report = {
                "resource_changes": {},
                "stat_changes": {},
                "messages": []
            }

            calculate_next_tick(station, new_report)
            last_report = new_report


if __name__ == "__main__":
    main()