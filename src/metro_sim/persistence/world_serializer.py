from dataclasses import asdict

from metro_sim.world.models.world_state import WorldState


def serialize_world_state(world: WorldState) -> dict:
    return asdict(world)