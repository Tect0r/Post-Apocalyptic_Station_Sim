from pydantic import BaseModel


class AddAssetRequestSchema(BaseModel):
    asset_type: str
    station_id: str | None = None
    route_id: str | None = None


class AssetActionResponseSchema(BaseModel):
    success: bool
    message: str
    data: dict | None = None