from enum import StrEnum


class PvPActionType(StrEnum):
    COMPETE_FOR_CONTRACT = "compete_for_contract"
    INFLUENCE_FACTION = "influence_faction"
    PRESSURE_STATION = "pressure_station"
    MANIPULATE_MARKET = "manipulate_market"
    DAMAGE_ASSET = "damage_asset"