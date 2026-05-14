from enum import StrEnum


class EventType(StrEnum):
    WATER_FILTER_DAMAGED = "water_filter_damaged"
    MARKET_PRICES_RISING = "market_prices_rising"
    ROUTE_UNSAFE = "route_unsafe"
    MILITIA_GAINS_CONTROL = "militia_gains_control"
    BANDIT_ACTIVITY_RISING = "bandit_activity_rising"
    MEDICAL_SHORTAGE = "medical_shortage"
    HANSA_SECURITY_DEPLOYED = "hansa_security_deployed"