from metro_sim.player.models.crew_state import CrewState
from metro_sim.player.models.inventory_state import InventoryState
from metro_sim.player.models.player_state import PlayerState
from metro_sim.player.models.reputation_state import ReputationState


def create_initial_player(
    player_id: str = "player_001",
    name: str = "Testspieler",
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
        ),
        inventory=InventoryState(
            items={
                "ammo": 40,
                "food": 12,
                "water": 18,
                "medicine": 2,
            }
        ),
        reputation=ReputationState(
            values={
                "paveletskaya": 0,
                "hansa": 0,
                "bandits": 0,
            }
        ),
        assets=[],
        active_actions=[],
    )