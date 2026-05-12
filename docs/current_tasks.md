Phase 1 — CLI von Spiellogik trennen

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