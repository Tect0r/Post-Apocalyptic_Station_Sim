from dataclasses import dataclass

from metro_sim.models.state_factory import create_initial_station
from metro_sim.services.report_service import create_empty_report
from metro_sim.services.tick_service import calculate_next_tick
from metro_sim.utils.file_loader import load_balancing

@dataclass
class GameSession:
    station: dict
    balancing: dict
    last_report: dict
    running: bool = True
    paused: bool = False

def create_game_session() -> GameSession:
    return GameSession(
        station=create_initial_station(),
        balancing=load_balancing(),
        last_report=create_empty_report(),
    )

def advance_tick(session: GameSession) -> None:
    new_report = create_empty_report()
    calculate_next_tick(session.station, new_report)
    session.last_report = new_report
