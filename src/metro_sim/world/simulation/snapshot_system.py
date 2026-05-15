from dataclasses import asdict, is_dataclass
from typing import Any

from metro_sim.world.models.world_snapshot import WorldSnapshot, create_world_snapshot
from metro_sim.world.models.world_state import WorldState


SNAPSHOT_INTERVAL_TICKS = 60
MAX_STORED_SNAPSHOTS = 100


def maybe_create_world_snapshot(world: WorldState) -> WorldSnapshot | None:
    if world.current_tick <= 0:
        return None

    if world.current_tick % SNAPSHOT_INTERVAL_TICKS != 0:
        return None

    snapshot = build_world_snapshot(world)
    world.snapshots.append(snapshot)

    if len(world.snapshots) > MAX_STORED_SNAPSHOTS:
        world.snapshots = world.snapshots[-MAX_STORED_SNAPSHOTS:]

    return snapshot


def build_world_snapshot(world: WorldState) -> WorldSnapshot:
    return create_world_snapshot(
        tick=world.current_tick,
        stations={
            station_id: serialize_for_snapshot(station)
            for station_id, station in world.stations.items()
        },
        routes={
            route_id: serialize_for_snapshot(route)
            for route_id, route in world.routes.items()
        },
        factions={
            faction_id: serialize_for_snapshot(faction)
            for faction_id, faction in world.factions.items()
        },
        events=[
            serialize_for_snapshot(event)
            for event in world.events
        ],
    )


def serialize_for_snapshot(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)

    if isinstance(value, dict):
        return {
            key: serialize_for_snapshot(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            serialize_for_snapshot(item)
            for item in value
        ]

    return value