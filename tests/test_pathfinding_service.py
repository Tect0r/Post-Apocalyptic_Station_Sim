from metro_sim.world.factories.world_factory import create_world
from metro_sim.world.services.pathfinding_service import find_station_path


def test_pathfinding_finds_path_from_paveletskaya_ring_to_sevastopolskaya():
    world = create_world()

    result = find_station_path(
        world=world,
        from_station_id="paveletskaya_ring",
        to_station_id="sevastopolskaya",
    )

    assert result.success is True
    assert result.station_ids == [
        "paveletskaya_ring",
        "paveletskaya_radial",
        "dobryninskaya_serpukhovskaya",
        "tulskaya",
        "nagatinskaya",
        "nagornaya",
        "nakhimovsky_prospekt",
        "sevastopolskaya",
    ]

    assert result.route_ids == [
        "route_paveletskaya_ring_radial",
        "route_paveletskaya_radial_dobryninskaya_serpukhovskaya",
        "route_dobryninskaya_serpukhovskaya_tulskaya",
        "route_tulskaya_nagatinskaya",
        "route_nagatinskaya_nagornaya",
        "route_nagornaya_nakhimovsky_prospekt",
        "route_nakhimovsky_prospekt_sevastopolskaya",
    ]

    assert result.total_travel_time_ticks > 0


def test_pathfinding_finds_reverse_path():
    world = create_world()

    result = find_station_path(
        world=world,
        from_station_id="sevastopolskaya",
        to_station_id="paveletskaya_ring",
    )

    assert result.success is True
    assert result.station_ids[0] == "sevastopolskaya"
    assert result.station_ids[-1] == "paveletskaya_ring"


def test_pathfinding_returns_error_for_unknown_start_station():
    world = create_world()

    result = find_station_path(
        world=world,
        from_station_id="unknown",
        to_station_id="sevastopolskaya",
    )

    assert result.success is False
    assert result.error == "from_station_not_found"


def test_pathfinding_returns_error_for_unknown_target_station():
    world = create_world()

    result = find_station_path(
        world=world,
        from_station_id="paveletskaya_ring",
        to_station_id="unknown",
    )

    assert result.success is False
    assert result.error == "to_station_not_found"


def test_pathfinding_returns_zero_length_path_for_same_station():
    world = create_world()

    result = find_station_path(
        world=world,
        from_station_id="paveletskaya_ring",
        to_station_id="paveletskaya_ring",
    )

    assert result.success is True
    assert result.station_ids == ["paveletskaya_ring"]
    assert result.route_ids == []
    assert result.total_travel_time_ticks == 0