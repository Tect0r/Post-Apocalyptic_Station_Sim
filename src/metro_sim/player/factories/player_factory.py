from metro_sim.player.models.crew_state import CrewState
from metro_sim.player.models.inventory_state import InventoryState
from metro_sim.player.models.player_state import PlayerState
from metro_sim.player.models.reputation_state import ReputationState


def create_initial_player(
    player_id: str = "player_001",
    name: str = "Test Player",
) -> PlayerState:
    return PlayerState(
        id=player_id,
        name=name,
        crew=CrewState(
            members=6,
            health=80,
            morale=55,
            fatigue=10,
            specialization="stalker",
            current_location_id="paveletskaya",
            destination_location_id=None,
            is_traveling=False
        ),
        inventory=InventoryState(
            items={
                "ammo": 80,
                "food": 40,
                "water": 40,
                "medicine": 8,
                "parts": 10,
            }
        ),
        reputation=ReputationState(
            values={
                "paveletskaya": 0,
                "polis": 0,
                "hansa_ring": 0,
                "hansa": 0,
                "bandits": 0,
                "independent": 0,
            }
        ),
        assets=[],
        active_actions=[],
        completed_actions=[],
    )