from pydantic import BaseModel


class StartActionRequestSchema(BaseModel):
    action_type: str
    target_id: str


class ActionResponseSchema(BaseModel):
    success: bool
    message: str
    data: dict | None = None