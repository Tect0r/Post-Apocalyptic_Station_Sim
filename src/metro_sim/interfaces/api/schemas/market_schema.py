from pydantic import BaseModel, Field


class MarketTradeRequestSchema(BaseModel):
    item_id: str
    amount: int = Field(gt=0)


class MarketTradeResponseSchema(BaseModel):
    success: bool
    message: str
    data: dict | None = None