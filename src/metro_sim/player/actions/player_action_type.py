from enum import StrEnum


class PlayerActionType(StrEnum):
    SCOUT_TUNNEL = "scout_tunnel"
    SECURE_ROUTE = "secure_route"
    SUPPORT_MILITIA = "support_militia"
    REPAIR_WATER_FILTER = "repair_water_filter"
    HIDE_CONTRABAND = "hide_contraband"
    RUN_MARKET_STALL = "run_market_stall"
    RENT_STORAGE = "rent_storage"
    START_STALKER_EXPEDITION = "start_stalker_expedition"
    TREAT_WOUNDED = "treat_wounded"
    MAINTAIN_FACTION_CONTACT = "maintain_faction_contact"