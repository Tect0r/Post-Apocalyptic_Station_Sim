Phase 2 — Aus station wird WorldState

Ziel: Die alte Simulation soll weiter funktionieren, aber der Spielzustand liegt nicht mehr direkt in station, sondern in world.stations["paveletskaya"]. Aktuell erzeugt create_initial_station() noch direkt ein Stations-Dict, und calculate_next_tick(station, report) arbeitet direkt auf dieser Station.

Wichtig: In Phase 2 baust du erstmal eine Hülle um die Station. Du ersetzt nicht sofort alle Dicts durch Dataclasses. Sonst wird der Umbau zu groß.

Aufgabe 1: Branch erstellen
git checkout -b refactor/world-state

Akzeptanzkriterium:

git status

zeigt:

On branch refactor/world-state
Aufgabe 2: Neue Ordnerstruktur anlegen

Lege an:

src/metro_sim/world/
src/metro_sim/world/models/
src/metro_sim/world/factories/
src/metro_sim/world/services/

Dazu jeweils:

src/metro_sim/world/__init__.py
src/metro_sim/world/models/__init__.py
src/metro_sim/world/factories/__init__.py
src/metro_sim/world/services/__init__.py

Akzeptanzkriterium:

python -m compileall src

läuft durch.

Aufgabe 3: StationState anlegen

Datei:

src/metro_sim/world/models/station_state.py

Inhalt:

from dataclasses import dataclass, field


@dataclass
class StationState:
    id: str
    name: str
    resources: dict
    population: dict
    stats: dict
    buildings: dict
    time: dict
    power: dict = field(default_factory=dict)
    water_system: dict = field(default_factory=dict)
    maintenance: dict = field(default_factory=dict)
    pressure: dict = field(default_factory=dict)
    faction_influence: dict = field(default_factory=dict)

Wichtig: Ich würde hier erstmal time, power, water_system und maintenance ergänzen, weil deine aktuelle Station diese Daten bereits hat. Wenn du sie nicht mitnimmst, verlierst du direkt Kompatibilität mit bestehenden Services.

Akzeptanzkriterium:

python -m compileall src

läuft durch.

Aufgabe 4: WorldState anlegen

Datei:

src/metro_sim/world/models/world_state.py

Inhalt:

from dataclasses import dataclass, field

from metro_sim.world.models.station_state import StationState


@dataclass
class WorldState:
    current_tick: int
    stations: dict[str, StationState]
    factions: dict = field(default_factory=dict)
    routes: dict = field(default_factory=dict)
    events: list = field(default_factory=list)

Akzeptanzkriterium:

Du kannst importieren:

from metro_sim.world.models.world_state import WorldState
Aufgabe 5: Platzhaltermodelle für Fraktionen und Routen anlegen

Datei:

src/metro_sim/world/models/faction_state.py

Inhalt:

from dataclasses import dataclass, field


@dataclass
class FactionState:
    id: str
    name: str
    resources: dict = field(default_factory=dict)
    relations: dict = field(default_factory=dict)
    controlled_stations: list[str] = field(default_factory=list)

Datei:

src/metro_sim/world/models/route_state.py

Inhalt:

from dataclasses import dataclass, field


@dataclass
class RouteState:
    id: str
    from_station_id: str
    to_station_id: str
    distance: int
    danger_level: int
    status: str = "open"
    modifiers: dict = field(default_factory=dict)

Akzeptanzkriterium:

python -m compileall src

läuft durch.

Aufgabe 6: Adapter von altem Station-Dict zu StationState bauen

Du hast aktuell viele Services, die ein Dict erwarten. Deshalb brauchst du einen Adapter.

Datei:

src/metro_sim/world/factories/station_factory.py

Inhalt:

from metro_sim.models.state_factory import create_initial_station
from metro_sim.world.models.station_state import StationState


def create_initial_station_state(station_id: str = "paveletskaya") -> StationState:
    station_dict = create_initial_station()

    return StationState(
        id=station_id,
        name=station_dict["name"],
        resources=station_dict["resources"],
        population=station_dict["population"],
        stats=station_dict["stats"],
        buildings=station_dict["slots"],
        time=station_dict["time"],
        power=station_dict["power"],
        water_system=station_dict["water_system"],
        maintenance=station_dict["maintenance"],
    )

Akzeptanzkriterium:

station = create_initial_station_state()
assert station.id == "paveletskaya"
assert station.name is not None
Aufgabe 7: Kompatibilitätsfunktion für alte Services bauen

Deine alten Services erwarten aktuell noch sowas:

station["resources"]
station["population"]
station["slots"]
station["time"]

StationState hat aber Attribute:

station.resources
station.population
station.buildings
station.time

Damit du nicht sofort alle Services umbauen musst, baust du erstmal eine Funktion zurück ins alte Dict-Format.

Datei erweitern:

src/metro_sim/world/factories/station_factory.py

Ergänzen:

def station_state_to_legacy_dict(station: StationState) -> dict:
    return {
        "name": station.name,
        "time": station.time,
        "population": station.population,
        "resources": station.resources,
        "power": station.power,
        "water_system": station.water_system,
        "stats": station.stats,
        "maintenance": station.maintenance,
        "slots": station.buildings,
    }

Akzeptanzkriterium:

station_state = create_initial_station_state()
legacy_station = station_state_to_legacy_dict(station_state)

assert "slots" in legacy_station
assert "resources" in legacy_station
assert "time" in legacy_station

Das ist nicht “schön”, aber strategisch richtig. Es erlaubt dir, WorldState einzuführen, ohne alle alten Services sofort zu zerstören.

Aufgabe 8: create_initial_world() bauen

Datei:

src/metro_sim/world/factories/world_factory.py

Inhalt:

from metro_sim.world.factories.station_factory import create_initial_station_state
from metro_sim.world.models.world_state import WorldState


def create_initial_world() -> WorldState:
    station = create_initial_station_state("paveletskaya")

    return WorldState(
        current_tick=0,
        stations={
            station.id: station,
        },
        factions={},
        routes={},
        events=[],
    )

Akzeptanzkriterium:

world = create_initial_world()

assert world.current_tick == 0
assert "paveletskaya" in world.stations
Aufgabe 9: advance_world_tick() bauen

Datei:

src/metro_sim/world/services/world_tick_service.py

Inhalt:

from metro_sim.services.report_service import create_empty_report
from metro_sim.services.tick_service import calculate_next_tick
from metro_sim.world.factories.station_factory import station_state_to_legacy_dict
from metro_sim.world.models.world_state import WorldState


def advance_world_tick(world: WorldState) -> dict:
    world.current_tick += 1

    world_report = {
        "tick": world.current_tick,
        "station_reports": {},
        "events": [],
    }

    for station_id, station in world.stations.items():
        station_report = create_empty_report()

        legacy_station = station_state_to_legacy_dict(station)
        calculate_next_tick(legacy_station, station_report)

        world_report["station_reports"][station_id] = station_report

    return world_report

Akzeptanzkriterium:

world = create_initial_world()
report = advance_world_tick(world)

assert world.current_tick == 1
assert "paveletskaya" in report["station_reports"]

Wichtig: Weil station_state_to_legacy_dict() dieselben verschachtelten Dicts verwendet, ändern die alten Services weiterhin die echte Station. Das funktioniert, weil resources, population, buildings, time usw. als Referenzen weitergegeben werden.

Aufgabe 10: GameSession auf WorldState umstellen

Falls du aus Phase 1 schon GameSession hast, ändere sie von:

@dataclass
class GameSession:
    station: dict
    balancing: dict
    last_report: dict

zu:

from dataclasses import dataclass

from metro_sim.world.models.world_state import WorldState


@dataclass
class GameSession:
    world: WorldState
    last_report: dict
    running: bool = True
    paused: bool = False

Dann:

from metro_sim.world.factories.world_factory import create_initial_world


def create_game_session() -> GameSession:
    return GameSession(
        world=create_initial_world(),
        last_report={},
    )

Und:

from metro_sim.world.services.world_tick_service import advance_world_tick


def advance_tick(session: GameSession) -> None:
    session.last_report = advance_world_tick(session.world)

Akzeptanzkriterium:

In GameSession gibt es nicht mehr:

station: dict

sondern:

world: WorldState
Aufgabe 11: CLI an neue Session-Struktur anpassen

Überall, wo die CLI aktuell sowas nutzt:

session.station

änderst du erstmal auf:

station = session.world.stations["paveletskaya"]

Aber Achtung: Deine alten CLI-Funktionen erwarten wahrscheinlich noch ein Dict. Deshalb gibst du dort erstmal das Legacy-Dict weiter.

In der CLI:

from metro_sim.world.factories.station_factory import station_state_to_legacy_dict

Dann:

station_state = session.world.stations["paveletskaya"]
station = station_state_to_legacy_dict(station_state)

Danach kannst du bestehende Funktionen weiter so aufrufen:

render_station(station, session.last_report)
handle_menu(station)

Akzeptanzkriterium:

Die CLI läuft weiterhin, obwohl intern jetzt session.world existiert.

Aufgabe 12: Direkte create_initial_station()-Nutzung reduzieren

Suche:

grep -R "create_initial_station" src/metro_sim

Erwartung:

Erlaubt ist es erstmal nur noch in:

src/metro_sim/world/factories/station_factory.py

Nicht mehr direkt in:

cli_app.py
game_session.py
main.py

Akzeptanzkriterium:

Die Initialisierung läuft über:

create_initial_world()

nicht mehr über:

create_initial_station()
Aufgabe 13: Direkte Tick-Nutzung reduzieren

Suche:

grep -R "calculate_next_tick" src/metro_sim

Erwartung:

Erlaubt ist es erstmal nur noch in:

src/metro_sim/world/services/world_tick_service.py

Nicht mehr direkt in der CLI.

Akzeptanzkriterium:

Die CLI ruft nicht mehr auf:

calculate_next_tick(station, report)

sondern nur noch indirekt:

advance_tick(session)

oder:

advance_world_tick(world)
Aufgabe 14: Test für create_initial_world()

Datei:

tests/test_world_factory.py

Inhalt:

from metro_sim.world.factories.world_factory import create_initial_world


def test_create_initial_world_contains_paveletskaya():
    world = create_initial_world()

    assert world.current_tick == 0
    assert "paveletskaya" in world.stations

    station = world.stations["paveletskaya"]

    assert station.id == "paveletskaya"
    assert station.name is not None
    assert station.resources is not None
    assert station.population is not None
    assert station.buildings is not None

Akzeptanzkriterium:

pytest tests/test_world_factory.py

läuft.

Aufgabe 15: Test für advance_world_tick()

Datei:

tests/test_world_tick_service.py

Inhalt:

from metro_sim.world.factories.world_factory import create_initial_world
from metro_sim.world.services.world_tick_service import advance_world_tick


def test_advance_world_tick_increases_current_tick():
    world = create_initial_world()

    advance_world_tick(world)

    assert world.current_tick == 1


def test_advance_world_tick_returns_station_report():
    world = create_initial_world()

    report = advance_world_tick(world)

    assert "station_reports" in report
    assert "paveletskaya" in report["station_reports"]

Akzeptanzkriterium:

pytest tests/test_world_tick_service.py

läuft.

Aufgabe 16: Test für alte Station-Kompatibilität

Datei:

tests/test_station_state_adapter.py

Inhalt:

from metro_sim.world.factories.station_factory import (
    create_initial_station_state,
    station_state_to_legacy_dict,
)


def test_station_state_can_be_converted_to_legacy_dict():
    station_state = create_initial_station_state()

    legacy_station = station_state_to_legacy_dict(station_state)

    assert legacy_station["name"] == station_state.name
    assert legacy_station["resources"] is station_state.resources
    assert legacy_station["population"] is station_state.population
    assert legacy_station["slots"] is station_state.buildings
    assert legacy_station["time"] is station_state.time

Der is-Check ist hier absichtlich. Er prüft, dass keine Kopie erzeugt wird. Wenn du eine Kopie erzeugst, ändern alte Services nicht mehr den echten StationState.

Akzeptanzkriterium:

pytest tests/test_station_state_adapter.py

läuft.

Aufgabe 17: Gesamttest

Ausführen:

python -m compileall src
pytest
python -m metro_sim.main

Manuell prüfen:

Spiel startet.
Zeit läuft weiter.
Produktion läuft weiter.
Konsolenanzeige funktioniert.
Worker-Zuweisung funktioniert noch.
Upgrade funktioniert noch.
world.current_tick steigt bei jedem Tick.
Die Station liegt unter world.stations["paveletskaya"].
Aufgabe 18: Saubere Commit-Reihenfolge

Nicht alles in einen Commit werfen.

Empfohlene Reihenfolge:

git add .
git commit -m "Add world state model structure"
git add .
git commit -m "Add station state adapter for legacy simulation"
git add .
git commit -m "Add initial world factory"
git add .
git commit -m "Add world tick service"
git add .
git commit -m "Refactor game session to use world state"
git add .
git commit -m "Add tests for world state initialization"
Ergebnis nach Phase 2

Vorher:

station = create_initial_station()
calculate_next_tick(station, report)

Nachher:

session = create_game_session()
advance_tick(session)

Intern:

session.world.stations["paveletskaya"]

Oder direkter:

world = create_initial_world()
advance_world_tick(world)