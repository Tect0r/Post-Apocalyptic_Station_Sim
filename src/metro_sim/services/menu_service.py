from metro_sim.ui.production_menu import create_employment_menu
from metro_sim.ui.cli import build_station_map_lines, clear_console, print_side_by_side

def show_employment_menu(station: dict) -> list[str]:
    clear_console()

    menu = create_employment_menu(station)
    station_map = build_station_map_lines(station=station)

    print_side_by_side(menu, station_map)

    return menu