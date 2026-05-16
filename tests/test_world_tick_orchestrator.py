from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.simulation.tick_orchestrator import process_world_tick
from metro_sim.world.models.world_event import create_world_event
from metro_sim.world.simulation.snapshot_system import SNAPSHOT_INTERVAL_TICKS
from metro_sim.world.simulation.movement_system import start_world_movement
from metro_sim.world.models.npc_trader import create_npc_trader


def test_world_tick_processes_production_and_consumption_on_interval():
    world = create_world()
    station = world.stations["paveletskaya_ring"]

    station.resources["trade_goods"] = 0
    world.current_tick = 9

    process_world_tick(world)

    assert station.resources["trade_goods"] > 0

def test_world_tick_updates_market_prices():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    station.population = 500
    station.resources["food"] = 20
    station.market["item_prices"] = {
        "food": 10,
        "water": 8,
        "medicine": 30,
        "ammo": 20,
        "trade_goods": 15,
        "parts": 25,
    }

    process_world_tick(world)

    assert station.market["item_prices"]["food"] > 10

def test_world_tick_processes_station_needs():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    station.population = 500
    station.resources["food"] = 50
    station.stats["morale"] = 50

    process_world_tick(world)

    assert station.stats["morale"] < 50

def test_world_tick_processes_npc_traders():
    world = create_world()

    trader = create_npc_trader(
        name="Test Trader",
        current_station_id="paveletskaya_ring",
        home_station_id="paveletskaya_ring",
        data={
            "preferred_targets": ["paveletskaya_radial"]
        },
    )

    world.npc_traders = {
        trader.id: trader
    }

    process_world_tick(world)

    assert trader.status == "traveling"
    assert len(world.movements) == 1
    assert any(
        log.category == "npc_trader_movement_started"
        for log in world.logs
    )

def test_world_tick_processes_completed_movements():
    world = create_world()

    result = start_world_movement(
        world=world,
        actor_type="trader",
        actor_id="trader_001",
        from_station_id="paveletskaya_ring",
        to_station_id="paveletskaya_radial",
    )

    movement = result.movement
    assert movement is not None

    world.current_tick = movement.arrives_at_tick - 1

    process_world_tick(world)

    assert movement.status == "completed"
    assert any(log.category == "movement_completed" for log in world.logs)

def test_world_tick_processes_faction_system():
    world = create_world()
    station = world.stations["paveletskaya_radial"]

    station.faction_influence["bandits"] = 50
    station.pressure["smuggling"] = 0

    process_world_tick(world)

    assert station.pressure["smuggling"] > 0

def test_world_tick_creates_snapshot_on_interval():
    world = create_world()
    world.current_tick = SNAPSHOT_INTERVAL_TICKS - 1

    process_world_tick(world)

    assert len(world.snapshots) == 1
    assert world.snapshots[0].tick == SNAPSHOT_INTERVAL_TICKS

def test_world_tick_turns_route_danger_into_station_event():
    world = create_world()

    route_id = next(iter(world.routes.keys()))
    route = world.routes[route_id]

    route.danger = 100
    route.condition = 100
    route.traffic = 0

    from_station_id = route.from_station_id
    to_station_id = route.to_station_id

    world.stations[from_station_id].pressure["danger"] = 19
    world.stations[to_station_id].pressure["danger"] = 19

    result = process_world_tick(world)

    event_types = [event.event_type for event in result.events]

    assert "mutant_sighting" in event_types

def test_world_tick_processes_routes_and_applies_route_effects():
    world = create_world()

    route_id = next(iter(world.routes.keys()))
    route = world.routes[route_id]

    route.danger = 75
    route.condition = 100
    route.traffic = 0

    from_station_id = route.from_station_id
    to_station_id = route.to_station_id

    world.stations[from_station_id].pressure["danger"] = 0
    world.stations[to_station_id].pressure["danger"] = 0

    process_world_tick(world)

    assert world.stations[from_station_id].pressure["danger"] > 0
    assert world.stations[to_station_id].pressure["danger"] > 0

def test_process_world_tick_advances_current_tick_by_one():
    world = create_world()
    start_tick = world.current_tick

    result = process_world_tick(world)

    assert world.current_tick == start_tick + 1
    assert result.tick == world.current_tick


def test_process_world_tick_returns_station_reports():
    world = create_world()

    result = process_world_tick(world)

    assert result.station_reports
    assert set(result.station_reports.keys()) == set(world.stations.keys())


def test_process_world_tick_stores_logs():
    world = create_world()

    process_world_tick(world)

    assert hasattr(world, "logs")
    assert len(world.logs) > 0


def test_process_world_tick_applies_effects():
    world = create_world()

    station = next(iter(world.stations.values()))
    station.pressure["sabotage"] = 25
    station.stats["security"] = 50

    process_world_tick(world)

    assert station.stats["security"] < 50


def test_world_tick_runs_event_system_and_applies_event_effects():
    world = create_world()
    station = world.stations["paveletskaya_radial"]
    station.pressure["militia_support"] = 25
    start_order = station.stats["order"]

    result = process_world_tick(world)

    assert len(result.events) == 9
    assert result.events[0].event_type == "militia_gains_control"

    assert len(world.events) == 9
    assert station.pressure["militia_support"] == 0
    assert station.stats["order"] > start_order

def test_world_tick_starts_mutant_attack_from_high_danger_pressure():
    world = create_world()
    station = world.stations["paveletskaya_radial"]
    station.pressure["danger"] = 50

    result = process_world_tick(world)

    event_types = [event.event_type for event in result.events]

    assert "mutant_attack" in event_types
    assert any(event.status == "running" for event in result.events)


def test_world_tick_processes_running_events():
    world = create_world()
    station = world.stations["paveletskaya_radial"]
    station.stats["morale"] = 50

    event = create_world_event(
        event_type="mutant_attack",
        target_type="station",
        target_id="paveletskaya_radial",
        started_at_tick=0,
        status="running",
        duration_ticks=1,
        current_phase="approaching",
    )

    world.events.append(event)
    world.current_tick = 0

    process_world_tick(world)

    assert event.status == "completed"
    assert station.stats["morale"] < 50