import metro_sim.ui.cli as cli
import metro_sim.utils.utility as util
import metro_sim.ui.upgrade_menu as upgrade_menu
import metro_sim.ui.employment_menu as employment_menu
import metro_sim.services.upgrade_service as upgrade_service
import metro_sim.services.station_service as station_service


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
    menu_lines, menu_actions = employment_menu.create_employment_menu(station)

    cli.clear_console()

    station_map = cli.build_station_map_lines(station=station)
    cli.print_side_by_side(menu_lines, station_map)

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
    
    station_service.assign_workers(station, selected_job, amount)

    print(f"{amount} Bewohner wurden zugewiesen: {selected_job}")
    input("Enter zum Fortfahren...")

def handle_upgrade_overview_menu(station: dict) -> None:
    cli.clear_console()

    menu_lines, menu_actions = upgrade_menu.create_upgrade_menu(station)
    station_map = cli.build_station_map_lines(station=station, upgrade_mode=True)
    cli.print_side_by_side(menu_lines, station_map)

    user_input = input("Wähle einen Slot zum upgraden. ")

    if user_input == "q":
        return

    selected_building = menu_actions.get(int(user_input))
    
    if selected_building is not None:
        handle_upgrade_detail_menu(station, selected_building, f"slot_{str(user_input)}")
    else:
        handle_build_new_building_menu(station, f"slot_{str(user_input)}")

def handle_build_new_building_menu(station: dict, selected_slot: str) -> None:
    menu_lines, menu_actions = upgrade_menu.create_possible_buildings_menu(station, selected_slot)

    cli.clear_console()

    station_map =cli. build_station_map_lines(station=station, upgrade_mode=True, selected_slot=selected_slot)
    cli.print_side_by_side(menu_lines, station_map)

    user_input = input("Wähle einen Gebäude zum bauen.")

    if user_input == "q":
        return
    
    selected_building = menu_actions.get(int(user_input))
    handle_upgrade_detail_menu(station, selected_building, selected_slot)

def handle_upgrade_detail_menu(station: dict, selected_building: dict, selected_slot: str) -> None:
    menu_lines = upgrade_menu.create_building_upgrade_menu(station, selected_building, selected_slot)

    cli.clear_console()

    station_map = cli.build_station_map_lines(station=station, upgrade_mode=True, selected_slot=selected_slot)
    cli.print_side_by_side(menu_lines, station_map)
    

    user_input = util.ask_until_valid(["q", "y", "n"] ,"Möchtest du das Gebäude upgraden?")

    if user_input == "q" or user_input == "n":
        return
    elif user_input == "y":
        upgrade_service.upgrade_building(station, selected_building, selected_slot)
        return