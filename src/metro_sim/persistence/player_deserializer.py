from metro_sim.player.actions.player_action import PlayerAction
from metro_sim.player.actions.player_action_type import PlayerActionType
from metro_sim.player.actions.player_action_status import PlayerActionStatus
from metro_sim.player.models.crew_state import CrewState
from metro_sim.player.models.inventory_state import InventoryState
from metro_sim.player.models.player_asset import PlayerAsset
from metro_sim.player.models.player_state import PlayerState
from metro_sim.player.models.reputation_state import ReputationState
from metro_sim.player.models.crew_member_state import CrewMemberState
from metro_sim.player.models.crew_member_status import CrewMemberStatus


def deserialize_player_action(action_data: dict) -> PlayerAction:
    return PlayerAction(
        id=action_data["id"],
        player_id=action_data["player_id"],
        assigned_crew_member_ids=action_data.get("assigned_crew_member_ids", []),
        action_type=PlayerActionType(action_data["action_type"]),
        target_type=action_data["target_type"],
        target_id=action_data["target_id"],
        started_tick=action_data["started_tick"],
        duration_ticks=action_data["duration_ticks"],
        status=PlayerActionStatus(action_data.get("status", "active")),
        payload=action_data.get("payload", {}),
    )


def deserialize_player_state(data: dict) -> PlayerState:
    crew_data = data["crew"]

    return PlayerState(
        id=data["id"],
        name=data["name"],
        crew=CrewState(
            members=crew_data["members"],
            health=crew_data["health"],
            morale=crew_data["morale"],
            fatigue=crew_data["fatigue"],
            specialization=crew_data["specialization"],
            current_location_id=crew_data.get("current_location_id", "paveletskaya"),
            destination_location_id=crew_data.get("destination_location_id"),
            is_traveling=crew_data.get("is_traveling", False),
            crew_members=[
                deserialize_crew_member(member_data)
                for member_data in crew_data.get("crew_members", [])
            ],
        ),
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
        completed_actions=[
            deserialize_player_action(action_data)
            for action_data in data.get("completed_actions", [])
        ],
    )


def deserialize_players(data: dict) -> dict[str, PlayerState]:
    return {
        player_id: deserialize_player_state(player_data)
        for player_id, player_data in data.items()
    }

def deserialize_crew_member(member_data: dict) -> CrewMemberState:
    return CrewMemberState(
        id=member_data["id"],
        name=member_data["name"],
        role=member_data["role"],
        health=member_data["health"],
        morale=member_data["morale"],
        fatigue=member_data["fatigue"],
        skills=member_data.get("skills", {}),
        traits=member_data.get("traits", []),
        status=CrewMemberStatus(member_data.get("status", "available")),
        current_location_id=member_data.get("current_location_id", "paveletskaya"),
        assigned_action_id=member_data.get("assigned_action_id"),
    )