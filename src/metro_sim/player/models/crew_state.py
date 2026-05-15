from dataclasses import dataclass


@dataclass
class CrewState:
    members: int
    health: int
    morale: int
    fatigue: int
    specialization: str
    current_location_id: str = "paveletskaya"
    destination_location_id: str | None = None
    is_traveling: bool = False