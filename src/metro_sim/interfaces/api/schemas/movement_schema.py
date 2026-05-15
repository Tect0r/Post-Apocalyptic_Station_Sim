from pydantic import BaseModel


class StartMovementRequestSchema(BaseModel):
    route_id: str