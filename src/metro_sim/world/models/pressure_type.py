from enum import StrEnum


class PressureType(StrEnum):
    SABOTAGE = "sabotage"
    SUPPLY_SUPPORT = "supply_support"
    MILITIA_SUPPORT = "militia_support"
    SMUGGLING = "smuggling"
    MEDICAL_SUPPORT = "medical_support"
    TRADE_ACTIVITY = "trade_activity"