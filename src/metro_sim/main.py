#pytest -v <- run tests

#$env:PYTHONPATH="src"
# python -m metro_sim.main <- run the main function to see the initial state

from time import sleep

from metro_sim.services.state_factory import create_initial_station
from metro_sim.ui.cli import clear_console, show_station_status

def main() -> None:
    clear_console()
    station = create_initial_station()
    show_station_status(station)


if __name__ == "__main__":
    while True:
        main()
        sleep(1)