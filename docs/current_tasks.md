Phase 1 — CLI von Spiellogik trennen

10. CLI-Menüs dünner machen

In handle_building_employment() sollte am Ende nur noch diese Art Ablauf stehen:

amount_input = input("Wie viele Arbeiter sollen hier arbeiten? > ").strip()

if amount_input == "q":
    return

if not amount_input.isdigit():
    error_message = "Ungültige Zahl."
    continue

result = worker_assignment_service.assign_workers_to_building(
    station=station,
    slot_id=selected_slot_id,
    worker_amount=int(amount_input),
)

if not result.success:
    error_message = result.message
    continue

print("Arbeiter wurden zugewiesen.")
input("Enter zum Fortfahren...")
return

Akzeptanzkriterium:

menu_handlers.py enthält weiterhin input() und print(), aber keine Spiellogik mehr.

11. Services nach UI-Abhängigkeiten durchsuchen

Ausführen:

grep -R "input(" src/metro_sim/services
grep -R "print(" src/metro_sim/services
grep -R "msvcrt" src/metro_sim/services
grep -R "interfaces.cli" src/metro_sim/services
grep -R "metro_sim.ui" src/metro_sim/services

Akzeptanzkriterium:

Alle Befehle liefern nichts zurück.

Das ist dein wichtigster Architektur-Check für Phase 1.

12. core/game_session.py anlegen

Damit später Webserver und CLI dieselbe Spielsession verwenden können, ziehst du die Initialisierung aus der CLI heraus.

Neue Datei:

src/metro_sim/core/game_session.py

Inhalt:

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

Dann in cli_app.py:

from metro_sim.core.game_session import create_game_session, advance_tick

Statt:

station = create_initial_station()
balancing_dict = load_balancing()
last_report = create_empty_report()

nutzt du:

session = create_game_session()

Akzeptanzkriterium:

Die CLI benutzt session.station, session.last_report, session.paused, session.running.

13. Tick-Aufruf aus CLI-Schleife vereinfachen

Vorher in cli_app.py:

new_report = create_empty_report()
calculate_next_tick(station, new_report)
last_report = new_report

Nachher:

advance_tick(session)

Akzeptanzkriterium:

cli_app.py importiert nicht mehr direkt:

calculate_next_tick
create_empty_report
create_initial_station
load_balancing

Diese Dinge gehören jetzt in game_session.py.

14. Tests für die erste echte Trennung schreiben

Lege an:

tests/test_upgrade_service.py

Minimal:

from metro_sim.services.upgrade_service import upgrade_building
from metro_sim.models.state_factory import create_initial_station


def test_upgrade_building_returns_action_result():
    station = create_initial_station()

    result = upgrade_building(
        station=station,
        building="mushroom_farm",
        selected_slot="slot_1",
    )

    assert hasattr(result, "success")
    assert hasattr(result, "message")

Je nachdem, ob slot_1 bei dir passt, musst du den Slot anpassen.

Akzeptanzkriterium:

pytest

läuft.

15. Tests für Worker-Zuweisung schreiben

Lege an:

tests/test_worker_assignment_service.py

Minimal:

from metro_sim.models.state_factory import create_initial_station
from metro_sim.services.worker_assignment_service import assign_workers_to_building


def test_assign_workers_rejects_invalid_slot():
    station = create_initial_station()

    result = assign_workers_to_building(
        station=station,
        slot_id="does_not_exist",
        worker_amount=1,
    )

    assert result.success is False
    assert result.message == "slot_not_found"

Akzeptanzkriterium:

pytest

läuft.

16. Alte ui-Struktur entfernen

Wenn alles läuft:

src/metro_sim/ui/

löschen.

Akzeptanzkriterium:

grep -R "metro_sim.ui" src tests

liefert nichts zurück.

17. Abschluss-Check für Phase 1

Diese Befehle sollten am Ende sauber sein:

python -m compileall src
pytest
grep -R "input(" src/metro_sim/services
grep -R "print(" src/metro_sim/services
grep -R "msvcrt" src/metro_sim/services
grep -R "metro_sim.ui" src tests

Zusätzlich manuell testen:

python -m metro_sim.main

Dann prüfen:

Spiel startet.
Simulation läuft.
Pause funktioniert.
Worker-Zuweisung funktioniert.
Gebäude-Upgrade funktioniert.
Ungültige Eingaben crashen nicht.
Services geben Ergebnisse zurück, aber geben selbst nichts aus.
Sinnvolle Commit-Reihenfolge

Mach nicht einen riesigen Commit. Besser:

git add .
git commit -m "Add interface and core package structure"
git add .
git commit -m "Move CLI files into interfaces package"
git add .
git commit -m "Isolate CLI keyboard input handling"
git add .
git commit -m "Add ActionResult for service responses"
git add .
git commit -m "Refactor upgrade service to return ActionResult"
git add .
git commit -m "Extract worker assignment service"
git add .
git commit -m "Add GameSession wrapper for simulation state"
git add .
git commit -m "Add tests for service-level actions"