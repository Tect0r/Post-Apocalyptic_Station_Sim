from pydantic import BaseModel, EmailStr, Field


class RegisterRequestSchema(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=8, max_length=128)


class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: str


class AuthResponseSchema(BaseModel):
    success: bool
    message: str
    data: dict | None = None