from dataclasses import dataclass


@dataclass
class CrewState:
    members: int
    health: int
    morale: int
    fatigue: int
    specialization: str