from enum import StrEnum


class PlayerAssetStatus(StrEnum):
    ACTIVE = "active"
    DAMAGED = "damaged"
    DISABLED = "disabled"
    LOST = "lost"