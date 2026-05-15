from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.models.world_event import create_world_event
from metro_sim.world.simulation.active_event_system import process_active_events
from metro_sim.world.simulation.effect_system import apply_world_effects


def test_active_mutant_attack_completes_after_duration():
    world = create_world()
    station = world.stations["paveletskaya"]
    station.stats["morale"] = 50
    station.stats["security"] = 50

    event = create_world_event(
        event_type="mutant_attack",
        target_type="station",
        target_id="paveletskaya",
        started_at_tick=0,
        status="running",
        duration_ticks=3,
        current_phase="approaching",
    )

    world.events.append(event)

    world.current_tick = 3

    effects, logs = process_active_events(world)
    apply_world_effects(world=world, effects=effects)

    assert event.status == "completed"
    assert station.stats["morale"] == 45
    assert station.stats["security"] == 47
    assert any(log.category == "event_completed" for log in logs)


def test_active_mutant_attack_changes_phase():
    world = create_world()

    event = create_world_event(
        event_type="mutant_attack",
        target_type="station",
        target_id="paveletskaya",
        started_at_tick=0,
        status="running",
        duration_ticks=40,
        current_phase="approaching",
    )

    world.events.append(event)
    world.current_tick = 20

    effects, logs = process_active_events(world)

    assert event.current_phase == "breach_attempt"
    assert effects == []
    assert any(log.category == "event_phase_changed" for log in logs)