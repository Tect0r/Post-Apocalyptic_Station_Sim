from enum import StrEnum


class PlayerActionType(StrEnum):
    START_EXPEDITION = "start_expedition"
    SECURE_ROUTE = "secure_route"
    RENT_STORAGE = "rent_storage"
    SUPPORT_REPAIR_TEAM = "support_repair_team"
    FUND_MILITIA = "fund_militia"