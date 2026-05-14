from metro_sim.world.models.tick_result import WorldTickResult
from metro_sim.world.models.world_state import WorldState
from metro_sim.world.services.station_tick_service import simulate_station_tick
from metro_sim.world.services.world_event_service import generate_world_events


def advance_world_tick(world: WorldState) -> WorldTickResult:
    world.current_tick += 1

    station_reports: dict[str, dict] = {}
    world_events: list = []

    for station in world.stations.values():
        station_result = simulate_station_tick(station)

        station_reports[station_result.station_id] = station_result.report
        
        generated_events = generate_world_events(world)
        world_events.extend(generated_events)

    return WorldTickResult(
        tick=world.current_tick,
        station_reports=station_reports,
        events=world_events,
    )
