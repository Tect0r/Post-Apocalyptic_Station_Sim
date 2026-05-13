from metro_sim.player.actions.forbidden_station_actions import FORBIDDEN_PLAYER_ACTION_TYPES
from metro_sim.player.actions.player_action_type import PlayerActionType


def test_player_action_types_do_not_include_direct_station_management():
    forbidden_values = {
        "assign_workers",
        "assign_workers_to_building",
        "upgrade_building",
        "build_station_building",
        "change_station_production",
        "set_station_maintenance",
    }

    action_values = {action_type.value for action_type in PlayerActionType}

    assert action_values.isdisjoint(forbidden_values)


def test_forbidden_station_actions_are_documented():
    assert "assign_workers_to_building" in FORBIDDEN_PLAYER_ACTION_TYPES
    assert "upgrade_building" in FORBIDDEN_PLAYER_ACTION_TYPES