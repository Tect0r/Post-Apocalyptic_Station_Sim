from metro_sim.core.action_result import ActionResult
import metro_sim.utils.file_loader as loader


def assign_workers_to_building(
    station: dict,
    slot_id: str,
    worker_amount: int,
) -> ActionResult:
    if slot_id not in station["slots"]:
        return ActionResult(False, "slot_not_found")
    
    slot = station["slots"][slot_id]
    building = slot.get("building")

    if building is None:
        return ActionResult(False, "slot_has_no_building")
    
    result = is_worker_amount_valid(station, worker_amount, slot_id)

    if not result.success:
        return result

    current_level = str(slot.get("level"))
    building_data = loader.load_production_data()[building]["levels"][current_level]

    max_workers = building_data["max_workers"]
    current_workers = slot.get("assigned_workers", 0)

    if worker_amount > max_workers:
        return ActionResult(False, "too_many_workers_for_building")

    worker_difference = worker_amount - current_workers



    station["population"]["worker_available"] -= worker_difference
    slot["assigned_workers"] = worker_amount

    return ActionResult(
        True,
        "workers_assigned",
        {
            "slot_id": slot_id,
            "worker_amount": worker_amount,
        },
    )

def is_worker_amount_valid(station: dict, new_amount: int, selected_slot_id: str) -> ActionResult:
    selected_slot = station["slots"][selected_slot_id]

    building = selected_slot.get("building")
    current_level = str(selected_slot.get("level"))
    building_data = loader.load_production_data()[building]["levels"][current_level]
    current_workers = selected_slot.get("assigned_workers", 0)
    
    if new_amount < 0:
        return ActionResult(False, "invalid_worker_amount")

    if new_amount > building_data["max_workers"]:
        return ActionResult(False, "too_many_workers_for_building")

    worker_difference = new_amount - current_workers

    if worker_difference > station["population"]["worker_available"]:
        return ActionResult(False, "not_enough_available_workers")
    
    return ActionResult(True, "can_assign_workers")