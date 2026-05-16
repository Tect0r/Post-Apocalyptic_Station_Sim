from collections import deque
from dataclasses import dataclass
from typing import Any

from metro_sim.world.models.route_state import RouteState
from metro_sim.world.models.world_state import WorldState


@dataclass
class StationPathResult:
    success: bool
    station_ids: list[str]
    route_ids: list[str]
    total_travel_time_ticks: int
    error: str | None = None


def find_station_path(
    *,
    world: WorldState,
    from_station_id: str,
    to_station_id: str,
) -> StationPathResult:
    if from_station_id not in world.stations:
        return StationPathResult(
            success=False,
            station_ids=[],
            route_ids=[],
            total_travel_time_ticks=0,
            error="from_station_not_found",
        )

    if to_station_id not in world.stations:
        return StationPathResult(
            success=False,
            station_ids=[],
            route_ids=[],
            total_travel_time_ticks=0,
            error="to_station_not_found",
        )

    if from_station_id == to_station_id:
        return StationPathResult(
            success=True,
            station_ids=[from_station_id],
            route_ids=[],
            total_travel_time_ticks=0,
        )

    adjacency = build_station_adjacency(world)

    queue = deque()
    queue.append((from_station_id, [from_station_id], []))

    visited = {from_station_id}

    while queue:
        current_station_id, station_path, route_path = queue.popleft()

        for next_station_id, route_id in adjacency.get(current_station_id, []):
            if next_station_id in visited:
                continue

            next_station_path = station_path + [next_station_id]
            next_route_path = route_path + [route_id]

            if next_station_id == to_station_id:
                return StationPathResult(
                    success=True,
                    station_ids=next_station_path,
                    route_ids=next_route_path,
                    total_travel_time_ticks=calculate_total_travel_time(
                        world=world,
                        route_ids=next_route_path,
                    ),
                )

            visited.add(next_station_id)
            queue.append((next_station_id, next_station_path, next_route_path))

    return StationPathResult(
        success=False,
        station_ids=[],
        route_ids=[],
        total_travel_time_ticks=0,
        error="path_not_found",
    )


def build_station_adjacency(
    world: WorldState,
) -> dict[str, list[tuple[str, str]]]:
    adjacency: dict[str, list[tuple[str, str]]] = {}

    for route_id, route in world.routes.items():
        from_station_id = get_route_value(route, "from_station_id")
        to_station_id = get_route_value(route, "to_station_id")

        if not isinstance(from_station_id, str) or not from_station_id:
            continue

        if not isinstance(to_station_id, str) or not to_station_id:
            continue

        if from_station_id not in world.stations:
            continue

        if to_station_id not in world.stations:
            continue

        if is_route_blocked(route):
            continue

        adjacency.setdefault(from_station_id, [])

        if (to_station_id, route_id) not in adjacency[from_station_id]:
            adjacency[from_station_id].append((to_station_id, route_id))

        if is_route_bidirectional(route):
            adjacency.setdefault(to_station_id, [])

            if (from_station_id, route_id) not in adjacency[to_station_id]:
                adjacency[to_station_id].append((from_station_id, route_id))

    return adjacency


def get_route_value(route: Any, key: str, default: Any = None) -> Any:
    if isinstance(route, dict):
        return route.get(key, default)

    return getattr(route, key, default)


def is_route_blocked(route: Any) -> bool:
    status = get_route_value(route, "status", "open")

    if status in {"blocked", "closed", "destroyed"}:
        return True

    tags = get_route_value(route, "tags", []) or []

    if "blocked" in tags or "closed" in tags:
        return True

    condition = get_route_value(route, "condition", 100)

    if isinstance(condition, int | float) and condition <= 0:
        return True

    return False


def is_route_bidirectional(route: Any) -> bool:
    return bool(get_route_value(route, "bidirectional", True))

def calculate_total_travel_time(
    *,
    world: WorldState,
    route_ids: list[str],
) -> int:
    total = 0

    for route_id in route_ids:
        route: RouteState = world.routes[route_id]
        total += route.travel_time_ticks

    return total