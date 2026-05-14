from uuid import uuid4

from metro_sim.utils.file_loader import load_world_event_rules_data
from metro_sim.world.models.world_event import WorldEvent
from metro_sim.world.models.world_state import WorldState
from metro_sim.world.services.event_cooldown_service import is_event_on_cooldown
from metro_sim.world.services.event_effect_service import apply_world_event_effects
from metro_sim.world.services.event_rule_service import station_matches_event_rule


def generate_world_events(world: WorldState) -> list[WorldEvent]:
    event_rules = load_world_event_rules_data()
    generated_events: list[WorldEvent] = []

    for station in world.stations.values():
        for rule_id, rule in event_rules.items():
            event_type = rule["event_type"]
            cooldown_ticks = rule.get("cooldown_ticks", 0)

            if is_event_on_cooldown(
                events=world.events,
                station_id=station.id,
                event_type=event_type,
                current_tick=world.current_tick,
                cooldown_ticks=cooldown_ticks,
            ):
                continue

            if not station_matches_event_rule(station, rule):
                continue

            event = WorldEvent(
                id=str(uuid4()),
                tick=world.current_tick,
                station_id=station.id,
                event_type=event_type,
                severity=rule.get("severity", 1),
                description_key=rule["description_key"],
                effects=rule.get("effects", {}),
                source="pressure",
            )

            apply_world_event_effects(station, event.effects)

            world.events.append(event)
            generated_events.append(event)

    return generated_events