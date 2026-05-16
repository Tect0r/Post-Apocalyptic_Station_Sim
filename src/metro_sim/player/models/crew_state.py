from dataclasses import dataclass, field

from metro_sim.player.models.crew_member_state import CrewMemberState


@dataclass
class CrewState:
    members: int
    health: int
    morale: int
    fatigue: int
    specialization: str
    current_location_id: str = "paveletskaya_radial"
    destination_location_id: str | None = None
    is_traveling: bool = False
    crew_members: list[CrewMemberState] = field(default_factory=list)
