import pytest

from metro_sim.world.factories.world_definition_loader import create_world_from_manifest
from metro_sim.world.services.pathfinding_service import find_station_path


def test_world_slice_is_connected_from_paveletskaya_to_sevastopolskaya():
    world = create_world_from_manifest()

    result = find_station_path(
        world=world,
        from_station_id="paveletskaya_ring",
        to_station_id="sevastopolskaya",
    )

    assert result.success is True

def test_create_world_from_manifest_loads_stations_routes_and_factions():
    world = create_world_from_manifest()

    assert "paveletskaya_ring" in world.stations
    assert "paveletskaya_radial" in world.stations
    assert "sevastopolskaya" in world.stations

    assert len(world.routes) >= 1

    assert "hansa" in world.factions
    assert "independent" in world.factions
    assert "polis" in world.factions
    assert "bandits" in world.factions


def test_paveletskaya_is_split_into_two_nodes():
    world = create_world_from_manifest()

    ring = world.stations["paveletskaya_ring"]
    radial = world.stations["paveletskaya_radial"]

    assert ring.complex_id == "paveletskaya"
    assert radial.complex_id == "paveletskaya"

    assert ring.faction_influence["hansa"] > radial.faction_influence["hansa"]
    assert radial.faction_influence["independent"] > ring.faction_influence["independent"]


def test_routes_reference_existing_stations():
    world = create_world_from_manifest()

    for route in world.routes.values():
        assert route.from_station_id in world.stations
        assert route.to_station_id in world.stations


def test_routes_have_valid_travel_time_ticks():
    world = create_world_from_manifest()

    for route in world.routes.values():
        assert route.travel_time_ticks > 0


def test_all_stations_have_required_pressure_keys():
    world = create_world_from_manifest()

    required_pressure = {
        "danger",
        "sabotage",
        "militia_support",
        "medical_support",
        "smuggling",
        "supply_disruption",
        "security_risk",
        "unrest",
        "faction_tension",
    }

    for station in world.stations.values():
        assert required_pressure <= set(station.pressure.keys())