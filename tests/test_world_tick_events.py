from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.services.world_tick_service import advance_world_tick


def test_world_tick_generates_events_from_pressure():
    world = create_world()
    station = world.stations["paveletskaya_radial"]
    station.pressure["militia_support"] = 25
    start_order = station.stats["order"]

    result = advance_world_tick(world)

    assert len(result.events) >= 1
    assert result.events[0].event_type == "militia_gains_control"

    assert len(world.events) >= 1
    assert world.events[0].event_type == "militia_gains_control"

    assert station.pressure["militia_support"] == 0
    assert station.stats["order"] > start_order