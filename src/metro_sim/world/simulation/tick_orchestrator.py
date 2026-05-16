from metro_sim.world.models.tick_result import WorldTickResult
from metro_sim.world.models.world_state import WorldState
from metro_sim.world.simulation.effect_system import apply_world_effects
from metro_sim.world.simulation.event_system import process_world_events
from metro_sim.world.simulation.log_system import append_world_logs
from metro_sim.world.simulation.route_system import process_routes_tick
from metro_sim.world.simulation.station_system import process_station_tick
from metro_sim.world.simulation.active_event_system import process_active_events
from metro_sim.world.simulation.snapshot_system import maybe_create_world_snapshot
from metro_sim.world.simulation.faction_system import process_factions_tick
from metro_sim.world.simulation.movement_system import process_world_movements
from metro_sim.world.simulation.npc_trader_system import process_npc_traders_tick
from metro_sim.world.simulation.market_system import process_markets_tick


def process_world_tick(world: WorldState) -> WorldTickResult:
    world.current_tick += 1

    station_reports: dict[str, dict] = {}
    all_effects = []
    all_logs = []

    movement_logs = process_world_movements(world)
    all_logs.extend(movement_logs)

    npc_trader_logs = process_npc_traders_tick(world)
    all_logs.extend(npc_trader_logs)

    # 1. Station systems generate pre-event effects.
    for station_id, station in world.stations.items():
        station.id = station_id

        station_result = process_station_tick(
            station=station,
            current_tick=world.current_tick,
        )

        report = station_result.report
        report["station_id"] = station_id
        station_reports[station_id] = report

        all_effects.extend(station_result.effects)
        all_logs.extend(station_result.logs)

    # 2. Route system generates pre-event effects.
    route_effects, route_logs = process_routes_tick(world)
    all_effects.extend(route_effects)
    all_logs.extend(route_logs)

    # Faction system
    faction_effects, faction_logs = process_factions_tick(world)

    all_effects.extend(faction_effects)
    all_logs.extend(faction_logs)

    # 3. Apply pre-event effects so EventSystem sees updated pressure/state.
    pre_event_effect_logs = apply_world_effects(
        world=world,
        effects=all_effects,
    )
    all_logs.extend(pre_event_effect_logs)

    pre_event_effect_logs = apply_world_effects(
        world=world,
        effects=all_effects,
    )
    all_logs.extend(pre_event_effect_logs)

    market_effects, market_logs = process_markets_tick(world)

    all_effects.extend(market_effects)
    all_logs.extend(market_logs)

    market_effect_logs = apply_world_effects(
        world=world,
        effects=market_effects,
    )
    all_logs.extend(market_effect_logs)

    active_event_effects, active_event_logs = process_active_events(world)

    all_effects.extend(active_event_effects)
    all_logs.extend(active_event_logs)

    active_event_effect_logs = apply_world_effects(
        world=world,
        effects=active_event_effects,
    )
    all_logs.extend(active_event_effect_logs)

    # 4. Generate events based on updated world state.
    generated_events, event_effects, event_logs = process_world_events(world)

    all_effects.extend(event_effects)
    all_logs.extend(event_logs)

    # 5. Apply event effects.
    event_effect_logs = apply_world_effects(
        world=world,
        effects=event_effects,
    )
    all_logs.extend(event_effect_logs)

    # 6. Store logs.
    append_world_logs(
        world=world,
        logs=all_logs,
    )

    maybe_create_world_snapshot(world)

    return WorldTickResult(
        tick=world.current_tick,
        station_reports=station_reports,
        effects=all_effects,
        logs=all_logs,
        events=generated_events,
    )


def process_world_ticks(
    *,
    world: WorldState,
    amount: int,
) -> WorldTickResult | None:
    last_result: WorldTickResult | None = None

    for _ in range(amount):
        last_result = process_world_tick(world)

    return last_result