from metro_sim.player.factories.player_factory import create_initial_player
from metro_sim.player.models.inventory_state import InventoryState
from metro_sim.player.models.reputation_state import ReputationState


def test_create_initial_player_has_crew():
    player = create_initial_player()

    assert player.id == "player_001"
    assert player.name == "Testspieler"
    assert player.crew.members == 6
    assert player.crew.specialization == "stalker"


def test_create_initial_player_has_inventory():
    player = create_initial_player()

    assert isinstance(player.inventory, InventoryState)
    assert player.inventory.items["ammo"] == 40
    assert player.inventory.items["food"] == 12
    assert player.inventory.items["water"] == 18
    assert player.inventory.items["medicine"] == 2


def test_create_initial_player_has_reputation():
    player = create_initial_player()

    assert isinstance(player.reputation, ReputationState)
    assert player.reputation.values["paveletskaya"] == 0
    assert player.reputation.values["hansa"] == 0
    assert player.reputation.values["bandits"] == 0


def test_create_initial_player_starts_without_assets_or_actions():
    player = create_initial_player()

    assert player.assets == []
    assert player.active_actions == []