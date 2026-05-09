import metro_sim.ui.cli as cli
import metro_sim.utils.utility as util
import metro_sim.ui.upgrade_menu as upgrade_menu
import metro_sim.ui.employment_menu as employment_menu
import metro_sim.services.upgrade_service as upgrade_service
import metro_sim.services.station_service as station_service
import msvcrt


def read_valid_key(valid_keys: set[str]) -> str:
    while True:
        key = msvcrt.getwch().lower()

        if key in valid_keys:
            return key

def show_pause_menu() -> str:
    print()
    print("Simulation pausiert")
    print("[Enter] Fortsetzen")
    print("")
    print("[1]: Bewohner zuweisen")
    print("[2]: Station verbessern")
    print("[3]: Handel")
    print("")
    print("[q] Beenden")

    return read_valid_key(["1", "2", "3", "q", "\r"])

def handle_employment_menu(station: dict) -> None:
    menu_lines, menu_actions = employment_menu.create_employment_menu(station)

    cli.clear_console()

    station_map = cli.build_station_map_lines(station=station)
    cli.print_side_by_side(menu_lines, station_map)

    user_input = input(">")

    if user_input == "q":
        return

    selected_slot_id = menu_actions.get(user_input)

    if selected_slot_id is None:
        print("Ungültige Eingabe")
        input("Enter zum Fortfahren...")
        return

    selected_slot = station["slots"][selected_slot_id]
    building = selected_slot.get("building")
    current_workers = selected_slot.get("assigned_workers", 0)

    print()
    print(f"Ausgewählter Slot: {selected_slot_id}")
    print(f"Gebäude: {building}")
    print(f"Aktuelle Arbeiter: {current_workers}")
    print(f"Verfügbare Arbeiter: {station['population']['worker_available']}")
    print()

    amount_input = input("Wie viele Arbeiter sollen hier arbeiten? > ").strip()

    if not amount_input.isdigit():
        print("Ungültige Zahl")
        input("Enter zum Fortfahren...")
        return

    new_amount = int(amount_input)

    if new_amount < 0:
        print("Ungültige Anzahl")
        input("Enter zum Fortfahren...")
        return

    worker_difference = new_amount - current_workers

    if worker_difference > station["population"]["worker_available"]:
        print("Nicht genug freie Arbeiter verfügbar.")
        input("Enter zum Fortfahren...")
        return

    station_service.assign_workers_to_slot(
        station=station,
        slot_id=selected_slot_id,
        worker_amount=new_amount
    )

    print(f"Die Anzahl der Arbeiter wurde in {selected_slot_id} auf {new_amount} gesetzt.")
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