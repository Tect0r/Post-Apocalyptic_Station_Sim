Phase 2: Aus station wird WorldState
Ziel

Dein aktueller Spielzustand soll nicht mehr direkt eine Station sein, sondern eine Welt mit mindestens einer Station.

Aktueller Denkfehler

Der alte Code denkt ungefähr so:

station = create_initial_station()
calculate_next_tick(station, report)

Das ist für Singleplayer okay, aber für Multiplayer falsch.

Neuer Denkrahmen
game_state = create_initial_game_state()
advance_world_tick(game_state.world)
Neue Modelle

Erstelle:

src/metro_sim/world/models/world_state.py
src/metro_sim/world/models/station_state.py
src/metro_sim/world/models/faction_state.py
src/metro_sim/world/models/route_state.py

Minimal:

from dataclasses import dataclass, field

@dataclass
class StationState:
    id: str
    name: str
    resources: dict
    population: dict
    stats: dict
    buildings: dict
    pressure: dict = field(default_factory=dict)
    faction_influence: dict = field(default_factory=dict)

@dataclass
class WorldState:
    current_tick: int
    stations: dict[str, StationState]
    factions: dict
    routes: dict
    events: list
Factory umbauen

Aus:

create_initial_station()

wird zusätzlich:

create_initial_world()

Erstmal darf create_initial_world() nur eine Station enthalten:

world = WorldState(
    current_tick=0,
    stations={
        "paveletskaya": create_initial_station()
    },
    factions={},
    routes={},
    events=[]
)
Zwischenziel

Die alte Simulation funktioniert noch, aber technisch liegt die Station jetzt innerhalb einer Welt.

Das ist der erste echte Schritt Richtung Multiplayer.

--------------------------------------------------------------------------------------------------------

Phase 3: Stationstick von Worldtick trennen
Ziel

Dein vorhandener Tick-Service soll weiter genutzt werden, aber er darf nicht mehr “das ganze Spiel” ticken. Er tickt nur noch eine Station. Dein Repo hat bereits einen tick_service.py, der zentrale Simulationsschritte ausführt.

Neue Trennung
core/services/station_tick_service.py
world/services/world_tick_service.py
Prinzip
def simulate_station_tick(station: StationState) -> StationTickResult:
    ...

def simulate_world_tick(world: WorldState) -> WorldTickResult:
    for station in world.stations.values():
        simulate_station_tick(station)
Warum wichtig

Später brauchst du:

- 1 Welt
- viele Stationen
- viele Spieler
- ein globaler Server-Tick

Dann darf nicht jeder Spieler seine “eigene Simulation” lokal laufen lassen.

Zwischenziel

Mehrere Stationen können im selben Weltzustand existieren und gemeinsam pro Tick aktualisiert werden.

--------------------------------------------------------------------------------------------------------

Phase 4: Spieler als Crew einführen
Ziel

Der Spieler ist nicht mehr Stationsverwalter, sondern Crew-/Organisationsführer.

Neue Modelle
src/metro_sim/player/models/player_state.py
src/metro_sim/player/models/crew_state.py
src/metro_sim/player/models/player_asset.py
src/metro_sim/player/models/reputation_state.py
src/metro_sim/player/models/inventory_state.py

Minimal:

@dataclass
class CrewState:
    members: int
    health: int
    morale: int
    fatigue: int
    specialization: str

@dataclass
class PlayerState:
    id: str
    name: str
    crew: CrewState
    inventory: dict
    reputation: dict
    assets: list
    active_actions: list
Startzustand

Beispiel:

player = PlayerState(
    id="player_001",
    name="Testspieler",
    crew=CrewState(
        members=6,
        health=80,
        morale=55,
        fatigue=10,
        specialization="stalker"
    ),
    inventory={
        "ammo": 40,
        "food": 12,
        "water": 18,
        "medicine": 2
    },
    reputation={
        "paveletskaya": 0,
        "hansa": 0,
        "bandits": 0
    },
    assets=[],
    active_actions=[]
)
Wichtig

Baue nicht direkt zehn Crew-Typen. Erst ein Spieler, eine Crew, wenige Werte.

Zwischenziel

Das Spiel kann einen Spieler mit Crew speichern und anzeigen, ohne dass der Spieler eine Station kontrolliert.

--------------------------------------------------------------------------------------------------------

Phase 5: Alte Stationsaktionen abschneiden oder umdeuten
Ziel

Alle alten Aktionen prüfen: Gehören sie noch zum Spieler oder zur Station?

Alte Aktionen

Vermutlich aktuell relevant:

- Bewohner zuweisen
- Gebäude bauen
- Gebäude upgraden
- Produktion verändern
- Wartung beeinflussen

Diese Aktionen passen nicht mehr direkt zum Multiplayer-Crew-Spiel.

Neue Einordnung
Stationsintern / NPC / Welt
- Wasserfilter betreiben
- Generatoren verwalten
- Wohnquartiere ausbauen
- Krankenstation betreiben
- Wachen einteilen

Das gehört zur Station, nicht direkt dem Spieler.

Spieleraktionen
- Crew auf Patrouille schicken
- Handelsroute sichern
- Lagerraum mieten
- Werkstatt betreiben
- Miliz finanzieren
- Schmuggelware verstecken
- Reparaturteam unterstützen
- Expedition starten
- Auftrag annehmen
Kritischer Punkt

Du darfst nicht einfach “Gebäude bauen” durch “Crew baut Gebäude” ersetzen. Dann bist du wieder beim Stationsmanagement.

Besser:

Spieler besitzt Assets.
Station besitzt Infrastruktur.
Zwischenziel

Es gibt eine klare Grenze zwischen Stationssystemen und Spielerbesitz.

--------------------------------------------------------------------------------------------------------

Phase 6: Action-System bauen
Ziel

Spieler beeinflussen die Welt über Aktionen. Das ist der Kern deines neuen Spiels.

Neue Struktur
src/metro_sim/player/services/player_action_service.py
src/metro_sim/world/services/action_resolution_service.py
data/player_actions.json
Action-Modell
@dataclass
class PlayerAction:
    id: str
    player_id: str
    action_type: str
    target_type: str
    target_id: str
    started_tick: int
    duration_ticks: int
    status: str
Beispielaktionen
1. Tunnel erkunden
2. Handelsroute sichern
3. Miliz unterstützen
4. Wasserfilter reparieren helfen
5. Schmuggelware verstecken
6. Marktstand betreiben
7. Lagerraum mieten
8. Stalker-Expedition starten
9. Verwundete versorgen
10. Fraktionskontakt pflegen
Beispiel player_actions.json
{
  "support_militia": {
    "label": "Miliz unterstützen",
    "target": "station",
    "duration_ticks": 6,
    "cost": {
      "ammo": 10,
      "food": 3
    },
    "effects": {
      "station_pressure": {
        "militia_support": 8
      },
      "player_reputation": {
        "station": 3,
        "bandits": -2
      },
      "crew": {
        "fatigue": 5
      }
    }
  }
}
Ablauf
1. Spieler wählt Aktion
2. Kosten werden geprüft
3. Aktion wird gestartet
4. Aktion läuft X Ticks
5. Ergebnis wird berechnet
6. Station/Spieler/Welt werden verändert
Zwischenziel

Der Spieler kann über seine Crew konkrete Aktionen ausführen, die Stationen beeinflussen.

--------------------------------------------------------------------------------------------------------

Phase 7: Pressure- und Influence-System einführen
Ziel

Viele Spieler sollen später dieselbe Station beeinflussen können, ohne dass jeder Klick direkt harte Änderungen auslöst.

Pressure-Werte

Pro Station:

pressure = {
    "sabotage": 0,
    "supply_support": 0,
    "militia_support": 0,
    "smuggling": 0,
    "medical_support": 0,
    "trade_activity": 0
}
Influence-Werte

Pro Station:

faction_influence = {
    "hansa": 48,
    "independent": 32,
    "bandits": 9,
    "red_line": 7,
    "polis": 4
}
Warum wichtig

Im Multiplayer darf nicht passieren:

100 Spieler klicken Sabotage
=> Station sofort kaputt

Besser:

100 Aktionen erzeugen Sabotagedruck
=> daraus entsteht eventuell ein Event
Zwischenziel

Spieleraktionen verändern Druck, Ruf und Einfluss. Die Welt entscheidet daraus über konkrete Ereignisse.

--------------------------------------------------------------------------------------------------------

Phase 8: Ereignissystem bauen
Ziel

Aus Weltzustand und Pressure-Werten entstehen Ereignisse.

Beispiele
- Wasserfilter beschädigt
- Marktpreise steigen
- Tunnelroute unsicher
- Miliz gewinnt Kontrolle zurück
- Banditenaktivität steigt
- Medizinmangel führt zu Krankheitswelle
- Hansa schickt Sicherheitskräfte
Event-Modell
@dataclass
class WorldEvent:
    id: str
    tick: int
    station_id: str
    event_type: str
    severity: int
    description_key: str
    effects: dict
Zwischenziel

Die Welt reagiert sichtbar auf Spieleraktionen, aber nicht chaotisch oder sofort.

--------------------------------------------------------------------------------------------------------

Phase 9: Minimalen Crew-Spiel-Prototyp bauen
Ziel

Jetzt erst sollte der neue Spielkern spielbar werden.

Inhalt
1 Welt
3 Stationen
2–3 Fraktionen
1 Spielercrew
10 Aktionen
Pressure-System
Influence-System
Ereignisse
ein einfacher Welt-Tick
Beispielstationen
- Paveletskaya
- Polis
- Hansa-Ringstation
Beispiel-Fraktionen
- Hansa
- Banditen
- Unabhängige
Spielerloop
1. Crewstatus prüfen
2. Station/Route/Auftrag wählen
3. Aktion starten
4. Ticks laufen lassen
5. Ergebnis erhalten
6. Ruf/Ressourcen/Crewstatus prüfen
7. neue Möglichkeiten freischalten
Zwischenziel

Das Spiel ist kein Stationsmanager mehr. Es ist ein Crew-Spiel mit Stationen als Weltobjekten.

Das ist der wichtigste Meilenstein der gesamten Roadmap.

--------------------------------------------------------------------------------------------------------

Phase 10: Persistenz vorbereiten
Ziel

Der Spielzustand darf nicht nur im RAM existieren. Für Web/Login/Multiplayer brauchst du Speicherung.

Erst simpel

Am Anfang reicht JSON-Speicherung:

saves/
  world_state.json
  players/
    player_001.json
Danach Datenbank

Für Web und Multiplayer später:

PostgreSQL

Nicht SQLite als langfristige Multiplayer-Basis. SQLite ist für lokal okay, aber bei parallelen Webzugriffen schnell unpraktisch.

Datenbanktabellen grob
users
players
crews
player_inventory
player_assets
stations
station_resources
station_stats
station_pressure
factions
station_faction_influence
routes
actions
events
market_orders
Zwischenziel

Welt und Spieler können gespeichert und geladen werden.

--------------------------------------------------------------------------------------------------------

Phase 11: Backend-API einführen
Ziel

Die Simulation bekommt eine HTTP-Schnittstelle. Die Web-UI spricht nicht direkt mit Python-Objekten, sondern mit einer API.

Empfehlung

Für Python:

FastAPI

Warum: modern, gut dokumentiert, automatische OpenAPI-Doku, gut für JSON-APIs.

Neue Struktur
src/metro_sim/interfaces/api/
  app.py
  routes/
    auth_routes.py
    player_routes.py
    world_routes.py
    station_routes.py
    action_routes.py
  schemas/
    player_schema.py
    station_schema.py
    action_schema.py
Erste Endpoints
GET  /health
GET  /world
GET  /stations
GET  /stations/{station_id}
GET  /player/me
GET  /player/me/crew
GET  /player/me/actions
POST /player/me/actions
Noch ohne Login

Erstmal kannst du mit einem festen Testspieler arbeiten.

Zwischenziel

Du kannst den Spielzustand über Browser/Postman/API-Client abfragen und Aktionen per HTTP starten.

--------------------------------------------------------------------------------------------------------

Phase 12: Web-UI als erste Version
Ziel

Eine einfache Oberfläche, die den neuen Spielkern sichtbar macht.

Empfehlung

Für dich realistisch:

Frontend: React + TypeScript
Backend: FastAPI

Alternativ, wenn du weniger Frontend-Komplexität willst:

HTMX + FastAPI Templates

Aber langfristig für ein Browsergame ist React + TypeScript sinnvoller.

Erste Seiten
/login              später
/dashboard
/crew
/stations
/stations/:id
/actions
/events
Erste UI-Funktionen
Dashboard:
- Crewstatus
- Ressourcen
- aktuelle Aktionen
- letzte Ereignisse

Stationsansicht:
- Sicherheit
- Moral
- Versorgung
- Fraktionseinfluss
- Pressure-Werte
- verfügbare Aktionen

Aktionsansicht:
- Aktion auswählen
- Kosten sehen
- Risiko sehen
- starten
Zwischenziel

Du kannst dein Crew-Spiel im Browser spielen, noch ohne echten Multiplayer.

--------------------------------------------------------------------------------------------------------

Phase 13: Login und User-System
Ziel

Spieler bekommen Accounts und besitzen jeweils einen PlayerState.

Nicht selbst unsicher basteln

Du brauchst:

- Passwort-Hashing
- Sessions oder JWT
- geschützte Endpoints
- User -> Player-Zuordnung
Tabellen
users
- id
- email
- username
- password_hash
- created_at

players
- id
- user_id
- name
- created_at
Auth-Flows
POST /auth/register
POST /auth/login
POST /auth/logout
GET  /player/me
Wichtig

Login kommt erst, wenn der Spielkern über API funktioniert. Sonst baust du Login um ein Spiel herum, das noch nicht klar ist.

Zwischenziel

Mehrere Accounts können sich anmelden und jeweils ihre eigene Crew sehen.

--------------------------------------------------------------------------------------------------------

Phase 14: Multiplayer-Grundlage
Ziel

Mehrere Spieler existieren in derselben Welt.

Wichtiges Prinzip

Nicht jeder Spieler hat eine eigene Welt.

Falsch:
User A -> eigene Welt
User B -> eigene Welt

Richtig:
Serverwelt -> viele Spielercrews
Datenmodell
world
  stations
  routes
  factions
  events

players
  crew
  inventory
  assets
  reputation
  actions
Erste Multiplayer-Version

Noch kein PvP.

Nur:

- Spieler sehen dieselben Stationen
- Spieleraktionen beeinflussen dieselben Pressure-Werte
- Events betreffen alle
- Spieler haben eigene Crews und Ressourcen
Zwischenziel

Wenn Spieler A Miliz unterstützt und Spieler B Schmuggel stärkt, sieht man beides im Zustand derselben Station.

--------------------------------------------------------------------------------------------------------

Phase 15: Server-Tick statt lokaler Tick
Ziel

Die Welt läuft serverseitig. Nicht der Client entscheidet, wann die Simulation fortschreitet.

Varianten
Variante A: Tick bei Request

Einfacher:

Wenn jemand eine Aktion ausführt oder Welt abfragt:
- prüfe vergangene Zeit
- simuliere nötige Ticks nach

Gut für frühen Prototyp.

Variante B: Hintergrundprozess

Später besser:

Alle X Sekunden:
- lade Welt
- simuliere Tick
- speichere Welt
Für den Anfang

Nimm Variante A oder einen simplen manuellen Admin-Tick.

Nicht direkt Celery, Redis, Worker, Scheduler, Deployment-Komplexität.

Zwischenziel

Die Weltentwicklung hängt nicht mehr an einem lokalen Konsolenloop.

--------------------------------------------------------------------------------------------------------

Phase 16: Aktionen asynchron machen
Ziel

Spieleraktionen dauern Zeit.

Nicht:

Klick -> Ergebnis sofort

Sondern:

Aktion starten -> läuft 2 Stunden / 6 Ticks -> Ergebnis
Action-Status
planned
active
completed
failed
cancelled
Beispiel
Stalker-Expedition:
- Dauer: 8 Ticks
- Risiko: mittel
- Kosten: Nahrung, Munition
- Ergebnis: Loot, Verletzungen, Informationen, Ruf
Zwischenziel

Das Spiel bekommt Browsergame-Struktur: planen, warten, reagieren.

--------------------------------------------------------------------------------------------------------

Phase 17: Auftragssystem
Ziel

Der Spieler braucht konkrete Ziele, nicht nur abstrakte Aktionen.

Auftragstypen
- Lieferauftrag
- Eskorte
- Reparaturhilfe
- Spionage
- Sabotage
- Patrouille
- Expedition
- Rettung
- Schmuggel
Auftrag hat
- Auftraggeber
- Zielstation
- Route
- Kosten
- Dauer
- Risiko
- Belohnung
- Rufauswirkung
- Weltwirkung
Zwischenziel

Crew-Management bekommt Richtung. Der Spieler fragt nicht mehr “welchen Wert erhöhe ich?”, sondern “welchen Auftrag nehme ich an?”

--------------------------------------------------------------------------------------------------------

Phase 18: Routen- und Bewegungssystem
Ziel

Die Metro-Welt wird räumlich.

RouteState
@dataclass
class RouteState:
    id: str
    from_station_id: str
    to_station_id: str
    danger: int
    control: dict
    travel_time_ticks: int
    trade_value: int
    blocked: bool
Warum wichtig

Crew-Spiel lebt von Bewegung:

- Wo ist meine Crew?
- Wie gefährlich ist die Route?
- Lohnt sich der Weg?
- Wer kontrolliert den Tunnel?
Zwischenziel

Spieleraktionen sind nicht mehr nur stationär, sondern hängen an Stationen und Routen.

--------------------------------------------------------------------------------------------------------

Phase 19: Spielerbesitz / Assets
Ziel

Spieler bauen keine Stationen, aber sie besitzen kleine Infrastruktur.

Asset-Typen
- Lagerraum
- Marktstand
- Werkbank
- Schlafquartier
- Schmuggelversteck
- Kontaktperson
- Eskorte
- Handelsroute
Asset-Modell
@dataclass
class PlayerAsset:
    id: str
    owner_player_id: str
    asset_type: str
    station_id: str | None
    route_id: str | None
    level: int
    condition: int
Zwischenziel

Spielerprogression entsteht durch Crew, Ruf, Besitz und Netzwerke — nicht durch Stationsbau.

--------------------------------------------------------------------------------------------------------

Phase 20: Markt und Handel
Ziel

Spieler brauchen wirtschaftliche Entscheidungen.

Erste Version
NPC-Marktpreise pro Station
Spieler kann kaufen/verkaufen
Preise hängen von Versorgung und Sicherheit ab
Spätere Version
Spielerangebote
Handelsrouten
Transportzeit
Risiko
Knappheit
Fraktionseinfluss
Nicht zu früh

Ein echter Spieler-zu-Spieler-Markt ist komplex. Erst NPC-Markt bauen.

Zwischenziel

Ressourcen werden strategisch relevant: Munition, Nahrung, Wasser, Medizin, Ersatzteile.

--------------------------------------------------------------------------------------------------------

Phase 21: Indirektes PvP
Ziel

PvP soll über Weltwirkung laufen, nicht über permanentes Direktangreifen.

Erste indirekte PvP-Systeme
- Spieler konkurrieren um Aufträge
- Spieler beeinflussen Fraktionseinfluss
- Spieler verändern Marktpreise
- Spieler stärken/schwächen Stationen
- Spieler erhöhen/ senken Pressure-Werte
Später
- Karawanenüberfall
- Sabotage gegen Assets
- Fraktionskriegszonen
- riskante Tunnelabschnitte
Schutzmechanismen
- keine komplette Account-Zerstörung
- Assets können beschädigt, aber nicht permanent gelöscht werden
- direkte Angriffe nur in bestimmten Zonen
- Reputation-Kosten für Aggression
- Cooldowns
- Beweis-/Entdeckungsmechanik
Zwischenziel

Spieler können gegeneinander arbeiten, ohne dass das Spiel toxisch wird.

--------------------------------------------------------------------------------------------------------

Phase 22: Rechte, Admin-Tools und Debug-Ansichten
Ziel

Du brauchst Werkzeuge, um deine Welt zu verstehen.

Admin-Ansichten
- alle Spieler
- alle Stationen
- alle laufenden Aktionen
- Pressure-Werte
- Fraktionseinfluss
- Events
- Tick-Logs
Debug-Funktionen
- Welt um 1 Tick vorspulen
- Aktion erzwingen
- Station zurücksetzen
- Spielerressourcen ändern
- Event auslösen
Zwischenziel

Du kannst Balancing und Fehler untersuchen, ohne in JSON/DB manuell herumzupfuschen.

--------------------------------------------------------------------------------------------------------

Phase 23: Tests
Ziel

Jetzt wird Testbarkeit wichtig.

Testbereiche
Unit Tests:
- Ressourcenverbrauch
- Aktion starten
- Aktion abschließen
- Pressure-Anstieg
- Influence-Normalisierung
- Rufänderung

Integration Tests:
- Spieler startet Aktion
- Ticks laufen
- Aktion verändert Station
- Event entsteht

API Tests:
- Login
- Spieler abrufen
- Aktion starten
- Stationszustand abrufen
Wichtig

Tests zuerst für Kernregeln, nicht für UI.

Zwischenziel

Du kannst refactoren, ohne ständig Angst zu haben, dass alles kaputtgeht.

--------------------------------------------------------------------------------------------------------

Phase 24: Deployment-Grundlage
Ziel

Spiel lokal und später online betreiben können.

Lokales Setup
backend/
frontend/
database/
docker-compose.yml
Komponenten
Backend: FastAPI
Frontend: React/TypeScript
DB: PostgreSQL
Reverse Proxy später: Nginx/Caddy
Zwischenziel

Du kannst das Spiel lokal mit einem Befehl starten.

Beispiel:

docker compose up

--------------------------------------------------------------------------------------------------------

Phase 25: MVP-Multiplayer
Ziel

Eine erste echte Multiplayer-Version.

MVP-Inhalt
Login:
- Registrierung
- Login
- eigener Spieler

Welt:
- 3 Stationen
- 3 Fraktionen
- 5 Routen
- globale Ticks

Crew:
- Mitglieder
- Gesundheit
- Moral
- Müdigkeit
- Inventar

Aktionen:
- 10 Aktionen
- Dauer
- Kosten
- Risiko
- Ergebnis

Stationen:
- Stats
- Pressure
- Fraktionseinfluss
- Events

UI:
- Dashboard
- Crew
- Station
- Aktionen
- Events
Nicht im MVP
- KI-Fraktionsagenten
- komplexer Spielerhandel
- direktes PvP
- große Metro-Karte
- viele Crewklassen
- Chat
- Gilden
- Echtzeit-Kampf
Zwischenziel

Das Spiel ist online spielbar, mit mehreren Spielern in derselben Welt.

--------------------------------------------------------------------------------------------------------

Phase 26: Danach erst KI-Fraktionen
Ziel

Erst wenn der MVP stabil läuft, lohnt sich KI.

Dann hast du:

- Weltzustand
- Fraktionszustand
- Aktionskatalog
- Regelvalidierung
- Logs
- Events

Erst dann kann ein KI-Agent sinnvoll sagen:

Hansa will Route X sichern.
Banditen wollen Station Y destabilisieren.
Polis will Krise Z entschärfen.

Vorher wäre KI nur Nebel über einem noch instabilen System.

--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------
