from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.simulation.snapshot_system import (
    SNAPSHOT_INTERVAL_TICKS,
    build_world_snapshot,
    maybe_create_world_snapshot,
)


def test_build_world_snapshot_captures_world_state():
    world = create_world()
    world.current_tick = 42

    snapshot = build_world_snapshot(world)

    assert snapshot.tick == 42
    assert snapshot.stations
    assert snapshot.routes
    assert snapshot.factions is not None
    assert isinstance(snapshot.events, list)


def test_maybe_create_world_snapshot_skips_non_interval_tick():
    world = create_world()
    world.current_tick = SNAPSHOT_INTERVAL_TICKS - 1

    snapshot = maybe_create_world_snapshot(world)

    assert snapshot is None
    assert len(world.snapshots) == 0


def test_maybe_create_world_snapshot_creates_on_interval_tick():
    world = create_world()
    world.current_tick = SNAPSHOT_INTERVAL_TICKS

    snapshot = maybe_create_world_snapshot(world)

    assert snapshot is not None
    assert len(world.snapshots) == 1
    assert world.snapshots[0].tick == SNAPSHOT_INTERVAL_TICKS