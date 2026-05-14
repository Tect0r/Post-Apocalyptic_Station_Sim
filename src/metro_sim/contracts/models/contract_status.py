from enum import StrEnum


class ContractStatus(StrEnum):
    AVAILABLE = "available"
    ACCEPTED = "accepted"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"