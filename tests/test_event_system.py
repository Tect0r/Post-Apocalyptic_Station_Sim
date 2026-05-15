from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.simulation.event_system import process_world_events


def test_event_system_creates_militia_control_event_from_pressure():
    world = create_world()
    station = world.stations["paveletskaya"]
    station.pressure["militia_support"] = 25

    events, effects, logs = process_world_events(world)

    assert len(events) == 1
    assert events[0].event_type == "militia_gains_control"
    assert events[0].target_type == "station"
    assert events[0].target_id == "paveletskaya"

    assert any(effect.reason == "militia_gains_control" for effect in effects)
    assert len(logs) >= 1


def test_event_system_creates_sabotage_event_from_pressure():
    world = create_world()
    station = world.stations["paveletskaya"]
    station.pressure["sabotage"] = 25

    events, effects, logs = process_world_events(world)

    assert len(events) == 1
    assert events[0].event_type == "sabotage_incident"

    assert any(effect.reason == "sabotage_incident" for effect in effects)
    assert len(logs) >= 1


def test_event_system_creates_medical_event_from_pressure():
    world = create_world()
    station = world.stations["paveletskaya"]
    station.pressure["medical_support"] = 25

    events, effects, logs = process_world_events(world)

    assert len(events) == 1
    assert events[0].event_type == "medical_campaign_success"

    assert any(effect.reason == "medical_campaign_success" for effect in effects)
    assert len(logs) >= 1


def test_event_system_creates_black_market_event_from_pressure():
    world = create_world()
    station = world.stations["paveletskaya"]
    station.pressure["smuggling"] = 25

    events, effects, logs = process_world_events(world)

    assert len(events) == 1
    assert events[0].event_type == "black_market_expands"

    assert any(effect.reason == "black_market_expands" for effect in effects)
    assert len(logs) >= 1