from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def get_health() -> dict:
    return {
        "status": "ok",
        "service": "metro_sim_api",
    }