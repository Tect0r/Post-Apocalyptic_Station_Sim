from time import sleep

from metro_sim.interfaces.cli.cli import clear_console, show_station_overview
import metro_sim.interfaces.cli.input_reader as input_reader
import metro_sim.interfaces.cli.menu_handlers as menu_handler

from metro_sim.core.game_session import create_game_session, advance_tick

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
    session = create_game_session()

    while session.running:
        clear_console()
        show_station_overview(session.station, session.last_report)

        if session.paused:
            user_input = menu_handler.show_pause_menu()

            match user_input:
                case "\r":
                    session.paused = False

                case "q":
                    session.running = False

                case "1":
                    menu_handler.handle_employment_menu(session.station)
                case "2":
                    menu_handler.handle_upgrade_overview_menu(session.station)
                
                case "3":
                    input("Enter zum Fortfahren...")
                case _:
                    print("Ungültige Eingabe")
                    input("Enter zum Fortfahren...")

        else:
            print()
            print("Simulation läuft... Taste drücken zum Pausieren.")

            pressed_key = wait_with_pause_check(
                session.balancing["time"]["real_seconds_per_tick"]
            )

            if pressed_key is not None:
                session.paused = True
                continue

            advance_tick(session)