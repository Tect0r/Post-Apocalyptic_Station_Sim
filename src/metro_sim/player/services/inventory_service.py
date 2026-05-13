from metro_sim.player.models.inventory_state import InventoryState


def can_afford(inventory: InventoryState, cost: dict[str, int]) -> bool:
    for item_id, amount in cost.items():
        if inventory.items.get(item_id, 0) < amount:
            return False

    return True


def pay_cost(inventory: InventoryState, cost: dict[str, int]) -> None:
    for item_id, amount in cost.items():
        inventory.items[item_id] = inventory.items.get(item_id, 0) - amount