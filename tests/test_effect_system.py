from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.models.world_effect import WorldEffect
from metro_sim.world.simulation.effect_system import apply_world_effects


def test_effect_system_adds_value_to_station_stat():
    world = create_world()
    station = world.stations["paveletskaya_radial"]
    station.stats["morale"] = 50

    effect = WorldEffect(
        target_type="station",
        target_id="paveletskaya_radial",
        field_path=["stats", "morale"],
        operation="add",
        value=5,
        reason="test_effect",
    )

    logs = apply_world_effects(world=world, effects=[effect])

    assert station.stats["morale"] == 55
    assert len(logs) == 1
    assert logs[0].category == "effect_applied"


def test_effect_system_subtracts_value_from_station_stat():
    world = create_world()
    station = world.stations["paveletskaya_radial"]
    station.stats["morale"] = 50

    effect = WorldEffect(
        target_type="station",
        target_id="paveletskaya_radial",
        field_path=["stats", "morale"],
        operation="subtract",
        value=5,
        reason="test_effect",
    )

    apply_world_effects(world=world, effects=[effect])

    assert station.stats["morale"] == 45


def test_effect_system_sets_value_on_station_stat():
    world = create_world()
    station = world.stations["paveletskaya_radial"]
    station.stats["morale"] = 50

    effect = WorldEffect(
        target_type="station",
        target_id="paveletskaya_radial",
        field_path=["stats", "morale"],
        operation="set",
        value=75,
        reason="test_effect",
    )

    apply_world_effects(world=world, effects=[effect])

    assert station.stats["morale"] == 75


def test_effect_system_clamps_station_stat_to_maximum():
    world = create_world()
    station = world.stations["paveletskaya_radial"]
    station.stats["morale"] = 98

    effect = WorldEffect(
        target_type="station",
        target_id="paveletskaya_radial",
        field_path=["stats", "morale"],
        operation="add",
        value=20,
        reason="test_effect",
    )

    apply_world_effects(world=world, effects=[effect])

    assert station.stats["morale"] == 100


def test_effect_system_clamps_station_stat_to_minimum():
    world = create_world()
    station = world.stations["paveletskaya_radial"]
    station.stats["morale"] = 2

    effect = WorldEffect(
        target_type="station",
        target_id="paveletskaya_radial",
        field_path=["stats", "morale"],
        operation="subtract",
        value=20,
        reason="test_effect",
    )

    apply_world_effects(world=world, effects=[effect])

    assert station.stats["morale"] == 0


def test_effect_system_logs_failure_for_unknown_station():
    world = create_world()

    effect = WorldEffect(
        target_type="station",
        target_id="unknown_station",
        field_path=["stats", "morale"],
        operation="add",
        value=5,
        reason="test_effect",
    )

    logs = apply_world_effects(world=world, effects=[effect])

    assert len(logs) == 1
    assert logs[0].category == "effect_failed"
    assert "target not found" in logs[0].message


def test_effect_system_logs_failure_for_unknown_field():
    world = create_world()

    effect = WorldEffect(
        target_type="station",
        target_id="paveletskaya_radial",
        field_path=["stats", "unknown_stat"],
        operation="add",
        value=5,
        reason="test_effect",
    )

    logs = apply_world_effects(world=world, effects=[effect])

    assert len(logs) == 1
    assert logs[0].category == "effect_failed"
    assert "Field path not found" in logs[0].message


def test_effect_system_logs_failure_for_unknown_operation():
    world = create_world()
    station = world.stations["paveletskaya_radial"]
    station.stats["morale"] = 50

    effect = WorldEffect(
        target_type="station",
        target_id="paveletskaya_radial",
        field_path=["stats", "morale"],
        operation="multiply",
        value=2,
        reason="test_effect",
    )

    logs = apply_world_effects(world=world, effects=[effect])

    assert station.stats["morale"] == 50
    assert len(logs) == 1
    assert logs[0].category == "effect_failed"
    assert "Unsupported effect operation" in logs[0].message