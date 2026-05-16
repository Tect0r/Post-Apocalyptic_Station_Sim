import json
from pathlib import Path
from typing import Any

from metro_sim.world.models.route_state import RouteState
from metro_sim.world.models.station_state import StationState
from metro_sim.world.models.world_state import WorldState
from metro_sim.world.factories.npc_trader_factory import create_initial_npc_traders


DEFINITIONS_ROOT = Path("data/definitions")


def create_world_from_manifest(
    manifest_path: str | Path = DEFINITIONS_ROOT / "world_slice.json",
) -> WorldState:
    manifest_path = Path(manifest_path)

    manifest = read_json(manifest_path)
    base_dir = manifest_path.parent

    stations = load_station_definitions(
        base_dir=base_dir,
        station_files=manifest["station_files"],
    )

    routes = load_route_definitions(
        base_dir=base_dir,
        route_files=manifest["route_files"],
    )

    factions = load_faction_definitions(
        base_dir=base_dir,
        faction_file=manifest["faction_file"],
    )

    contracts = load_contract_definitions(
        base_dir=base_dir,
        contract_file=manifest.get("contract_file"),
    )

    validate_world_definitions(
        stations=stations,
        routes=routes,
        factions=factions,
    )

    return WorldState(
        current_tick=0,
        stations=stations,
        routes=routes,
        factions=factions,
        contracts=contracts,
        npc_traders=create_initial_npc_traders(),
    )


def load_station_definitions(
    *,
    base_dir: Path,
    station_files: list[str],
) -> dict[str, StationState]:
    stations: dict[str, StationState] = {}

    for station_file in station_files:
        data = read_json(base_dir / station_file)
        nodes = data.get("nodes", {})

        for node_id, node_data in nodes.items():
            if node_id in stations:
                raise ValueError(f"Duplicate station node id: {node_id}")

            node_data = dict(node_data)
            node_data.setdefault("id", node_id)
            node_data.setdefault("complex_id", data.get("complex_id"))

            station = StationState(**node_data)
            stations[node_id] = station

    return stations


def load_route_definitions(
    *,
    base_dir: Path,
    route_files: list[str],
) -> dict[str, RouteState]:
    routes: dict[str, RouteState] = {}

    for route_file in route_files:
        data = read_json(base_dir / route_file)
        route_data_by_id = data.get("routes", {})

        for route_id, route_data in route_data_by_id.items():
            if route_id in routes:
                raise ValueError(f"Duplicate route id: {route_id}")

            route_data = dict(route_data)
            route_data.setdefault("id", route_id)

            route = RouteState(**route_data)
            routes[route_id] = route

    return routes


def load_faction_definitions(
    *,
    base_dir: Path,
    faction_file: str,
) -> dict[str, Any]:
    data = read_json(base_dir / faction_file)
    return data.get("factions", {})


def validate_world_definitions(
    *,
    stations: dict[str, StationState],
    routes: dict[str, RouteState],
    factions: dict[str, Any],
) -> None:
    validate_required_station_fields(stations)
    validate_required_route_fields(stations=stations, routes=routes)
    validate_faction_references(
        stations=stations,
        routes=routes,
        factions=factions,
    )


def validate_required_station_fields(
    stations: dict[str, StationState],
) -> None:
    required_stats = {
        "morale",
        "order",
        "security",
        "health",
        "comfort",
    }

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

    for station_id, station in stations.items():
        missing_stats = required_stats - set(station.stats.keys())
        if missing_stats:
            raise ValueError(
                f"Station {station_id} is missing stats: {sorted(missing_stats)}"
            )

        missing_pressure = required_pressure - set(station.pressure.keys())
        if missing_pressure:
            raise ValueError(
                f"Station {station_id} is missing pressure keys: {sorted(missing_pressure)}"
            )


def validate_required_route_fields(
    *,
    stations: dict[str, StationState],
    routes: dict[str, RouteState],
) -> None:
    for route_id, route in routes.items():
        if route.from_station_id not in stations:
            raise ValueError(
                f"Route {route_id} references unknown from_station_id: {route.from_station_id}"
            )

        if route.to_station_id not in stations:
            raise ValueError(
                f"Route {route_id} references unknown to_station_id: {route.to_station_id}"
            )

        if route.travel_time_ticks <= 0:
            raise ValueError(
                f"Route {route_id} must have travel_time_ticks > 0"
            )

        if not 0 <= route.danger <= 100:
            raise ValueError(
                f"Route {route_id} danger must be between 0 and 100"
            )

        if not 0 <= route.condition <= 100:
            raise ValueError(
                f"Route {route_id} condition must be between 0 and 100"
            )


def validate_faction_references(
    *,
    stations: dict[str, StationState],
    routes: dict[str, RouteState],
    factions: dict[str, Any],
) -> None:
    faction_ids = set(factions.keys())

    for station_id, station in stations.items():
        unknown_factions = set(station.faction_influence.keys()) - faction_ids
        if unknown_factions:
            raise ValueError(
                f"Station {station_id} references unknown factions: {sorted(unknown_factions)}"
            )

    for route_id, route in routes.items():
        unknown_factions = set(route.control.keys()) - faction_ids
        if unknown_factions:
            raise ValueError(
                f"Route {route_id} references unknown factions: {sorted(unknown_factions)}"
            )


def read_json(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Definition file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)
    
def load_contract_definitions(
    *,
    base_dir: Path,
    contract_file: str | None,
) -> dict[str, Any]:
    if contract_file is None:
        return {}

    data = read_json(base_dir / contract_file)
    return data.get("contracts", {})