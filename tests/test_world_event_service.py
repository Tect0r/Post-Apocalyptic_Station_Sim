from metro_sim.world.factories.world_factory import create_initial_world
from metro_sim.world.services.world_event_service import generate_world_events


def test_generate_world_events_creates_event_from_station_pressure():
    world = create_initial_world()
    station = world.stations["paveletskaya"]
    station.pressure["militia_support"] = 25

    events = generate_world_events(world)

    assert len(events) == 1
    assert events[0].station_id == "paveletskaya"
    assert events[0].event_type == "militia_gains_control"
    assert events[0].description_key == "event.militia_gains_control"
    assert len(world.events) == 1


def test_generate_world_events_applies_cooldown():
    world = create_initial_world()
    station = world.stations["paveletskaya"]
    station.pressure["militia_support"] = 25

    first_events = generate_world_events(world)
    second_events = generate_world_events(world)

    assert len(first_events) == 1
    assert second_events == []