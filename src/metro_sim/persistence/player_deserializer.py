from metro_sim.player.actions.player_action import PlayerAction
from metro_sim.player.actions.player_action_type import PlayerActionType
from metro_sim.player.models.crew_state import CrewState
from metro_sim.player.models.inventory_state import InventoryState
from metro_sim.player.models.player_asset import PlayerAsset
from metro_sim.player.models.player_state import PlayerState
from metro_sim.player.models.reputation_state import ReputationState


def deserialize_player_action(action_data: dict) -> PlayerAction:
    return PlayerAction(
        id=action_data["id"],
        player_id=action_data["player_id"],
        action_type=PlayerActionType(action_data["action_type"]),
        target_type=action_data["target_type"],
        target_id=action_data["target_id"],
        started_tick=action_data["started_tick"],
        duration_ticks=action_data["duration_ticks"],
        status=action_data.get("status", "active"),
        payload=action_data.get("payload", {}),
    )


def deserialize_player_state(data: dict) -> PlayerState:
    return PlayerState(
        id=data["id"],
        name=data["name"],
        crew=CrewState(**data["crew"]),
        inventory=InventoryState(**data["inventory"]),
        reputation=ReputationState(**data["reputation"]),
        assets=[
            PlayerAsset(**asset_data)
            for asset_data in data.get("assets", [])
        ],
        active_actions=[
            deserialize_player_action(action_data)
            for action_data in data.get("active_actions", [])
        ],
    )


def deserialize_players(data: dict) -> dict[str, PlayerState]:
    return {
        player_id: deserialize_player_state(player_data)
        for player_id, player_data in data.items()
    }