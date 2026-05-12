from time import sleep

from metro_sim.utils.file_loader import load_balancing
from metro_sim.models.state_factory import create_initial_station
from metro_sim.services.tick_service import calculate_next_tick
from metro_sim.services.report_service import create_empty_report
from metro_sim.interfaces.cli.cli import clear_console, show_station_overview
import metro_sim.interfaces.cli.input_reader as input_reader
import metro_sim.interfaces.cli.menu_handlers as menu_handler

def wait_with_pause_check(seconds: int | float) -> str | None:
    step = 0.1
    elapsed = 0.0

    while elapsed < seconds:
        key = input_reader.key_pressed()

        if key is not None:
            return key

        sleep(step)
        elapsed += step

    return None

def run_cli() -> None:
    station = create_initial_station()
    balancing_dict = load_balancing()

    running = True
    paused = False
    last_report = create_empty_report()

    while running:
        clear_console()
        show_station_overview(station, last_report)

        if paused:
            user_input = menu_handler.show_pause_menu()

            match user_input:
                case "\r":
                    paused = False

                case "q":
                    running = False

                case "1":
                    menu_handler.handle_employment_menu(station)
                case "2":
                    menu_handler.handle_upgrade_overview_menu(station)
                
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

            new_report = create_empty_report()

            calculate_next_tick(station, new_report)
            last_report = new_report