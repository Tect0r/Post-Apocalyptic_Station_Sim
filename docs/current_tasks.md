Phase 1 — CLI von Spiellogik trennen

9. Worker-Zuweisung aus Menülogik herauslösen

Aktuell prüft handle_building_employment() sehr viel direkt im CLI-Menü: Zahl prüfen, maximale Arbeiter prüfen, verfügbare Arbeiter prüfen, dann station_service.assign_workers_to_slot(...) aufrufen.

Ziel: Die CLI fragt nur Eingabe ab. Die fachliche Prüfung gehört in den Service.

Lege oder erweitere:

src/metro_sim/services/worker_assignment_service.py

Funktion:

from metro_sim.core.action_result import ActionResult
import metro_sim.utils.file_loader as loader


def assign_workers_to_building(
    station: dict,
    slot_id: str,
    worker_amount: int,
) -> ActionResult:
    if slot_id not in station["slots"]:
        return ActionResult(False, "slot_not_found")

    if worker_amount < 0:
        return ActionResult(False, "invalid_worker_amount")

    slot = station["slots"][slot_id]
    building = slot.get("building")

    if building is None:
        return ActionResult(False, "slot_has_no_building")

    current_level = str(slot.get("level"))
    building_data = loader.load_production_data()[building]["levels"][current_level]

    max_workers = building_data["max_workers"]
    current_workers = slot.get("assigned_workers", 0)

    if worker_amount > max_workers:
        return ActionResult(False, "too_many_workers_for_building")

    worker_difference = worker_amount - current_workers

    if worker_difference > station["population"]["worker_available"]:
        return ActionResult(False, "not_enough_available_workers")

    station["population"]["worker_available"] -= worker_difference
    slot["assigned_workers"] = worker_amount

    return ActionResult(
        True,
        "workers_assigned",
        {
            "slot_id": slot_id,
            "worker_amount": worker_amount,
        },
    )

Akzeptanzkriterium:

In menu_handlers.py steht keine Fachlogik mehr wie:

if new_amount > building_data["max_workers"]:

oder:

if worker_difference > station["population"]["worker_available"]:

Die CLI darf nur noch prüfen:

if not amount_input.isdigit():

Alles andere macht der Service.

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