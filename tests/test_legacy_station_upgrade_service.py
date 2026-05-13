# tests/test_upgrade_service.py

import pytest

from metro_sim.services.upgrade_service import (
    upgrade_building,
    can_afford,
    pay_resources,
    salvage_resources,
)


# ------------------------------------------------------------
# Testdaten / Fixtures
# ------------------------------------------------------------

@pytest.fixture
def station():
    """
    Fixture = wiederverwendbare Testdaten.

    Diese Station wird in mehreren Tests benutzt.
    Vorteil:
    - weniger Duplikate
    - Tests bleiben lesbarer
    - Änderungen an der Grundstruktur nur an einer Stelle
    """
    return {
        "resources": {
            "mechanical": {
                "scrap": 100,
                "parts": 50,
            }
        },
        "slots": {
            "slot_1": {
                "building": None,
                "level": 0,
                "production_progress": 0,
            },
            "slot_2": {
                "building": "mushroom_farm",
                "level": 1,
                "production_progress": 20,
            },
            "slot_3": {
                "building": "water_filter",
                "level": 3,
                "production_progress": 80,
            },
        },
    }


@pytest.fixture
def building_costs():
    """
    Fake-Kostendaten für Gebäude-Upgrades.

    Im echten Code kommen diese Daten aus JSON über:
    loader.load_buildings_cost_data()

    Im Test wollen wir aber keine echte Datei laden.
    Deshalb mocken/patchen wir diese Funktion später.
    """
    return {
        "mushroom_farm": {
            "upgrade_cost": {
                "1": {"scrap": 10, "parts": 5},
                "2": {"scrap": 20, "parts": 10},
                "3": {"scrap": 30, "parts": 15},
            }
        },
        "water_filter": {
            "upgrade_cost": {
                "1": {"scrap": 15, "parts": 5},
                "2": {"scrap": 25, "parts": 10},
                "3": {"scrap": 40, "parts": 20},
            }
        },
    }


# ------------------------------------------------------------
# Tests für can_afford()
# ------------------------------------------------------------

def test_can_afford_returns_success_when_resources_are_enough():
    """
    Ziel:
    Prüfen, ob can_afford True zurückgibt,
    wenn alle benötigten Ressourcen vorhanden sind.

    Struktur:
    Arrange = Testdaten vorbereiten
    Act     = Funktion ausführen
    Assert  = Ergebnis prüfen
    """

    # Arrange
    resources = {
        "scrap": 100,
        "parts": 50,
    }

    costs = {
        "scrap": 10,
        "parts": 5,
    }

    # Act
    result = can_afford(resources, costs)

    # Assert
    assert result.success is True
    assert result.message == "can_pay_resources"


def test_can_afford_returns_missing_resource_when_resource_is_too_low():
    """
    Ziel:
    Prüfen, ob can_afford False zurückgibt,
    wenn eine Ressource nicht reicht.

    Hier fehlt scrap:
    gebraucht: 120
    vorhanden: 100
    """

    # Arrange
    resources = {
        "scrap": 100,
        "parts": 50,
    }

    costs = {
        "scrap": 120,
        "parts": 5,
    }

    # Act
    result = can_afford(resources, costs)

    # Assert
    assert result.success is False
    assert result.message == "missing_scrap"


def test_can_afford_treats_missing_resource_as_zero():
    """
    Ziel:
    Prüfen, ob eine nicht vorhandene Ressource als 0 behandelt wird.

    In deinem Code:
    available_amount = resources.get(resource_name, 0)

    Wenn "parts" nicht existiert, wird also 0 angenommen.
    """

    # Arrange
    resources = {
        "scrap": 100,
    }

    costs = {
        "parts": 5,
    }

    # Act
    result = can_afford(resources, costs)

    # Assert
    assert result.success is False
    assert result.message == "missing_parts"


# ------------------------------------------------------------
# Tests für pay_resources()
# ------------------------------------------------------------

def test_pay_resources_subtracts_costs_from_resources():
    """
    Ziel:
    Prüfen, ob pay_resources die Kosten korrekt abzieht.

    Wichtig:
    pay_resources verändert das übergebene Dictionary direkt.
    Es gibt nichts zurück.
    """

    # Arrange
    resources = {
        "scrap": 100,
        "parts": 50,
    }

    costs = {
        "scrap": 10,
        "parts": 5,
    }

    # Act
    pay_resources(resources, costs)

    # Assert
    assert resources["scrap"] == 90
    assert resources["parts"] == 45


# ------------------------------------------------------------
# Tests für upgrade_building()
# ------------------------------------------------------------

def test_upgrade_building_places_new_building_in_empty_slot(
    station,
    building_costs,
    monkeypatch,
):
    """
    Ziel:
    Ein leeres Slot soll mit einem Gebäude belegt und auf Level 1 gesetzt werden.

    Warum monkeypatch?
    upgrade_building lädt intern JSON-Daten über:
    loader.load_buildings_cost_data()

    Im Test ersetzen wir diese Funktion durch Fake-Daten.
    Dadurch ist der Test unabhängig von echten Dateien.
    """

    # Arrange
    monkeypatch.setattr(
        "metro_sim.services.upgrade_service.loader.load_buildings_cost_data",
        lambda: building_costs,
    )

    # Act
    result = upgrade_building(
        station=station,
        building="mushroom_farm",
        selected_slot="slot_1",
    )

    # Assert: Rückgabe prüfen
    assert result.success is True
    assert result.message == "slot_upgraded"

    # Assert: Slot wurde korrekt gesetzt
    assert station["slots"]["slot_1"]["building"] == "mushroom_farm"
    assert station["slots"]["slot_1"]["level"] == 1
    assert station["slots"]["slot_1"]["production_progress"] == 0

    # Assert: Ressourcen wurden bezahlt
    assert station["resources"]["mechanical"]["scrap"] == 90
    assert station["resources"]["mechanical"]["parts"] == 45


def test_upgrade_building_upgrades_existing_same_building(
    station,
    building_costs,
    monkeypatch,
):
    """
    Ziel:
    Wenn im Slot bereits dasselbe Gebäude steht,
    soll es um 1 Level erhöht werden.

    slot_2 startet mit:
    building = mushroom_farm
    level = 1

    Danach sollte es level = 2 sein.
    """

    # Arrange
    monkeypatch.setattr(
        "metro_sim.services.upgrade_service.loader.load_buildings_cost_data",
        lambda: building_costs,
    )

    # Act
    result = upgrade_building(
        station=station,
        building="mushroom_farm",
        selected_slot="slot_2",
    )

    # Assert
    assert result.success is True
    assert result.message == "slot_upgraded"

    assert station["slots"]["slot_2"]["building"] == "mushroom_farm"
    assert station["slots"]["slot_2"]["level"] == 2
    assert station["slots"]["slot_2"]["production_progress"] == 0

    # Level 2 kostet bei mushroom_farm:
    # scrap: 20
    # parts: 10
    assert station["resources"]["mechanical"]["scrap"] == 80
    assert station["resources"]["mechanical"]["parts"] == 40


def test_upgrade_building_fails_when_slot_has_different_building(
    station,
    building_costs,
    monkeypatch,
):
    """
    Ziel:
    Wenn im Slot schon ein anderes Gebäude steht,
    darf das Upgrade nicht durchgeführt werden.

    slot_2 enthält mushroom_farm.
    Wir versuchen aber water_filter zu bauen.
    Das muss fehlschlagen.
    """

    # Arrange
    monkeypatch.setattr(
        "metro_sim.services.upgrade_service.loader.load_buildings_cost_data",
        lambda: building_costs,
    )

    # Act
    result = upgrade_building(
        station=station,
        building="water_filter",
        selected_slot="slot_2",
    )

    # Assert: Ergebnis ist Fehler
    assert result.success is False
    assert result.message == "slot_has_different_building"

    # Assert: Slot bleibt unverändert
    assert station["slots"]["slot_2"]["building"] == "mushroom_farm"
    assert station["slots"]["slot_2"]["level"] == 1

    # Assert: Ressourcen bleiben unverändert
    assert station["resources"]["mechanical"]["scrap"] == 100
    assert station["resources"]["mechanical"]["parts"] == 50


def test_upgrade_building_fails_when_slot_is_already_max_level(
    station,
    building_costs,
    monkeypatch,
):
    """
    Ziel:
    Ein Gebäude auf Level 3 darf nicht weiter verbessert werden.

    In deinem Code:
    new_level = current_level + 1

    Wenn current_level 3 ist, wäre new_level 4.
    Dann kommt:
    ActionResult(False, "slot_is_max_level")
    """

    # Arrange
    monkeypatch.setattr(
        "metro_sim.services.upgrade_service.loader.load_buildings_cost_data",
        lambda: building_costs,
    )

    # Act
    result = upgrade_building(
        station=station,
        building="water_filter",
        selected_slot="slot_3",
    )

    # Assert
    assert result.success is False
    assert result.message == "slot_is_max_level"

    # Assert: nichts verändert
    assert station["slots"]["slot_3"]["building"] == "water_filter"
    assert station["slots"]["slot_3"]["level"] == 3

    assert station["resources"]["mechanical"]["scrap"] == 100
    assert station["resources"]["mechanical"]["parts"] == 50


def test_upgrade_building_fails_when_player_cannot_afford_upgrade(
    station,
    building_costs,
    monkeypatch,
):
    """
    Ziel:
    Wenn Ressourcen fehlen, darf nicht gebaut werden.

    Achtung:
    In deiner aktuellen upgrade_service.py ist wahrscheinlich ein Bug:

        return ActionResult(False, can_afford_ActionResult["msg"])

    Wenn ActionResult kein Dictionary ist, müsste es vermutlich heißen:

        return ActionResult(False, can_afford_Actionresult.message)

    Falls dieser Test mit
    TypeError: 'ActionResult' object is not subscriptable
    fehlschlägt, liegt es genau daran.
    """

    # Arrange
    monkeypatch.setattr(
        "metro_sim.services.upgrade_service.loader.load_buildings_cost_data",
        lambda: building_costs,
    )

    # Ressourcen absichtlich zu niedrig setzen
    station["resources"]["mechanical"]["scrap"] = 5
    station["resources"]["mechanical"]["parts"] = 50

    # Act
    result = upgrade_building(
        station=station,
        building="mushroom_farm",
        selected_slot="slot_1",
    )

    # Assert
    assert result.success is False
    assert result.message == "missing_scrap"

    # Assert: Slot wurde nicht verändert
    assert station["slots"]["slot_1"]["building"] is None
    assert station["slots"]["slot_1"]["level"] == 0

    # Assert: Ressourcen wurden nicht abgezogen
    assert station["resources"]["mechanical"]["scrap"] == 5
    assert station["resources"]["mechanical"]["parts"] == 50


# ------------------------------------------------------------
# Tests für salvage_resources()
# ------------------------------------------------------------

def test_salvage_resources_adds_percentage_of_costs(monkeypatch):
    """
    Ziel:
    Prüfen, ob beim Abriss ein prozentualer Anteil der Kosten
    zurückgegeben wird.

    Die Funktion lädt intern:
    loader.load_balancing()

    Deshalb patchen wir auch diese Funktion.
    """

    # Arrange
    fake_balancing = {
        "building_demolishing": {
            "salvaged_resource_percentage": 0.5,
        }
    }

    monkeypatch.setattr(
        "metro_sim.services.upgrade_service.loader.load_balancing",
        lambda: fake_balancing,
    )

    resources = {
        "scrap": 10,
        "parts": 5,
    }

    costs = {
        "scrap": 20,
        "parts": 10,
    }

    # Act
    salvage_resources(resources, costs)

    # Assert
    # 50% von 20 scrap = 10
    # 50% von 10 parts = 5
    assert resources["scrap"] == 20
    assert resources["parts"] == 10