from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.models.world_log_entry import create_world_log_entry
from metro_sim.world.simulation.log_system import (
    append_world_logs,
    get_debug_world_logs,
    get_logs_by_category,
    get_logs_for_target,
    get_visible_world_logs,
)


def test_append_world_logs_stores_logs():
    world = create_world()

    log = create_world_log_entry(
        tick=1,
        category="world_event",
        message="Test event",
        importance="normal",
    )

    append_world_logs(world=world, logs=[log])

    assert len(world.logs) == 1
    assert world.logs[0].message == "Test event"


def test_get_visible_world_logs_filters_debug_logs():
    world = create_world()

    debug_log = create_world_log_entry(
        tick=1,
        category="station_processed",
        message="Debug",
        importance="debug",
    )

    visible_log = create_world_log_entry(
        tick=1,
        category="world_event",
        message="Visible",
        importance="normal",
    )

    append_world_logs(world=world, logs=[debug_log, visible_log])

    visible_logs = get_visible_world_logs(world=world)

    assert len(visible_logs) == 1
    assert visible_logs[0].message == "Visible"


def test_get_debug_world_logs_returns_all_recent_logs():
    world = create_world()

    debug_log = create_world_log_entry(
        tick=1,
        category="station_processed",
        message="Debug",
        importance="debug",
    )

    visible_log = create_world_log_entry(
        tick=1,
        category="world_event",
        message="Visible",
        importance="normal",
    )

    append_world_logs(world=world, logs=[debug_log, visible_log])

    logs = get_debug_world_logs(world=world)

    assert len(logs) == 2


def test_get_logs_by_category():
    world = create_world()

    log_a = create_world_log_entry(
        tick=1,
        category="world_event",
        message="Event",
        importance="normal",
    )

    log_b = create_world_log_entry(
        tick=1,
        category="effect_applied",
        message="Effect",
        importance="normal",
    )

    append_world_logs(world=world, logs=[log_a, log_b])

    logs = get_logs_by_category(
        world=world,
        category="world_event",
    )

    assert len(logs) == 1
    assert logs[0].message == "Event"


def test_get_logs_for_target():
    world = create_world()

    log_a = create_world_log_entry(
        tick=1,
        category="world_event",
        message="Paveletskaya event",
        target_type="station",
        target_id="paveletskaya",
        importance="normal",
    )

    log_b = create_world_log_entry(
        tick=1,
        category="world_event",
        message="Polis event",
        target_type="station",
        target_id="polis",
        importance="normal",
    )

    append_world_logs(world=world, logs=[log_a, log_b])

    logs = get_logs_for_target(
        world=world,
        target_type="station",
        target_id="paveletskaya",
    )

    assert len(logs) == 1
    assert logs[0].message == "Paveletskaya event"


def test_append_world_logs_limits_log_count():
    world = create_world()

    logs = [
        create_world_log_entry(
            tick=i,
            category="debug_tick",
            message=f"Log {i}",
            importance="debug",
        )
        for i in range(1100)
    ]

    append_world_logs(world=world, logs=logs)

    assert len(world.logs) == 1000
    assert world.logs[0].message == "Log 100"