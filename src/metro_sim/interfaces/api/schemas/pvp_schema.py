from pydantic import BaseModel, Field


class StationPressurePvpRequestSchema(BaseModel):
    station_id: str
    pressure_key: str
    amount: int = Field(ge=-10, le=10)


class AssetDamagePvpRequestSchema(BaseModel):
    target_player_id: str
    asset_id: str
    amount: int = Field(gt=0, le=20)


class PvpActionResponseSchema(BaseModel):
    success: bool
    message: str
    data: dict | None = None