from metro_sim.world.models.world_event import WorldEvent


def is_event_on_cooldown(
    events: list[WorldEvent],
    station_id: str,
    event_type: str,
    current_tick: int,
    cooldown_ticks: int,
) -> bool:
    for event in reversed(events):
        if event.station_id != station_id:
            continue

        if event.event_type != event_type:
            continue

        return current_tick - event.tick < cooldown_ticks

    return False