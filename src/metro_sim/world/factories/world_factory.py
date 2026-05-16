from metro_sim.world.factories.world_definition_loader import create_world_from_manifest
from metro_sim.world.models.world_state import WorldState


def create_world() -> WorldState:
    return create_world_from_manifest()