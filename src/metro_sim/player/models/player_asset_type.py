from enum import StrEnum


class PlayerAssetType(StrEnum):
    STORAGE_ROOM = "storage_room"
    MARKET_STALL = "market_stall"
    WORKBENCH = "workbench"
    SLEEPING_QUARTERS = "sleeping_quarters"
    SMUGGLER_CACHE = "smuggler_cache"
    CONTACT_PERSON = "contact_person"
    ESCORT_CONTRACT = "escort_contract"
    TRADE_ROUTE_ACCESS = "trade_route_access"