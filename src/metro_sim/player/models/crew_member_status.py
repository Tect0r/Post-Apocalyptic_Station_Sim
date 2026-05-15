from enum import StrEnum


class CrewMemberStatus(StrEnum):
    AVAILABLE = "available"
    ASSIGNED = "assigned"
    TRAVELING = "traveling"
    INJURED = "injured"
    RESTING = "resting"
    DEAD = "dead"