from fastapi import APIRouter, HTTPException

from metro_sim.auth.services.login_service import login_user
from metro_sim.auth.services.registration_service import register_user
from metro_sim.interfaces.api.schemas.auth_schema import (
    AuthResponseSchema,
    LoginRequestSchema,
    RegisterRequestSchema,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponseSchema)
def register(request: RegisterRequestSchema) -> AuthResponseSchema:
    result = register_user(
        email=request.email,
        username=request.username,
        password=request.password,
    )

    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)

    return AuthResponseSchema(
        success=True,
        message=result.message,
        data=result.data,
    )


@router.post("/login", response_model=AuthResponseSchema)
def login(request: LoginRequestSchema) -> AuthResponseSchema:
    result = login_user(
        email=request.email,
        password=request.password,
    )

    if not result.success:
        raise HTTPException(status_code=401, detail=result.message)

    return AuthResponseSchema(
        success=True,
        message=result.message,
        data=result.data,
    )


@router.post("/logout")
def logout() -> dict:
    return {
        "success": True,
        "message": "logout_client_side",
    }