from metro_sim.world.models.tick_result import WorldTickResult
from metro_sim.world.models.world_state import WorldState
from metro_sim.world.simulation.effect_system import apply_world_effects
from metro_sim.world.simulation.event_system import process_world_events
from metro_sim.world.simulation.log_system import append_world_logs
from metro_sim.world.simulation.route_system import process_routes_tick
from metro_sim.world.simulation.station_system import process_station_tick


def process_world_tick(world: WorldState) -> WorldTickResult:
    world.current_tick += 1

    station_reports: dict[str, dict] = {}
    all_effects = []
    all_logs = []

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

    # 3. Apply pre-event effects so EventSystem sees updated pressure/state.
    pre_event_effect_logs = apply_world_effects(
        world=world,
        effects=all_effects,
    )
    all_logs.extend(pre_event_effect_logs)

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