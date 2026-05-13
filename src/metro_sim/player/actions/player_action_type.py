from enum import StrEnum


class PlayerActionType(StrEnum):
    SUPPORT_MILITIA = "support_militia"
    REPAIR_WATER_FILTER = "repair_water_filter"
    SECURE_ROUTE = "secure_route"