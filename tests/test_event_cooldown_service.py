from metro_sim.world.models.world_event import WorldEvent
from metro_sim.world.services.event_cooldown_service import is_event_on_cooldown


def test_event_is_on_cooldown_when_recent_event_exists():
    events = [
        WorldEvent(
            id="event_001",
            tick=10,
            station_id="paveletskaya",
            event_type="militia_gains_control",
            severity=2,
            description_key="event.militia_gains_control",
        )
    ]

    result = is_event_on_cooldown(
        events=events,
        station_id="paveletskaya",
        event_type="militia_gains_control",
        current_tick=15,
        cooldown_ticks=12,
    )

    assert result is True


def test_event_is_not_on_cooldown_after_cooldown_passed():
    events = [
        WorldEvent(
            id="event_001",
            tick=10,
            station_id="paveletskaya",
            event_type="militia_gains_control",
            severity=2,
            description_key="event.militia_gains_control",
        )
    ]

    result = is_event_on_cooldown(
        events=events,
        station_id="paveletskaya",
        event_type="militia_gains_control",
        current_tick=23,
        cooldown_ticks=12,
    )

    assert result is False