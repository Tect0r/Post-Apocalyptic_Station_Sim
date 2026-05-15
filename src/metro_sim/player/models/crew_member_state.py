from dataclasses import dataclass, field

from metro_sim.player.models.crew_member_status import CrewMemberStatus


@dataclass
class CrewMemberState:
    id: str
    name: str
    role: str
    health: int
    morale: int
    fatigue: int
    skills: dict[str, int] = field(default_factory=dict)
    traits: list[str] = field(default_factory=list)
    status: CrewMemberStatus = CrewMemberStatus.AVAILABLE
    current_location_id: str = "paveletskaya"
    assigned_action_id: str | None = None