from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from metro_sim.interfaces.api.routes import (
    action_routes,
    admin_routes,
    event_routes,
    faction_routes,
    health_routes,
    market_routes,
    player_routes,
    route_routes,
    station_routes,
    world_routes,
    auth_routes,
    contract_routes,
    movement_routes,
    asset_routes
)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Metro Sim API",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:5174",
            "http://127.0.0.1:5174",
        ],
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    app.include_router(health_routes.router)
    app.include_router(world_routes.router)
    app.include_router(station_routes.router)
    app.include_router(route_routes.router)
    app.include_router(faction_routes.router)
    app.include_router(event_routes.router)
    app.include_router(player_routes.router)
    app.include_router(action_routes.router)
    app.include_router(admin_routes.router)
    app.include_router(auth_routes.router)
    app.include_router(contract_routes.router)
    app.include_router(movement_routes.router)
    app.include_router(asset_routes.router)
    app.include_router(market_routes.router)

    return app


app = create_app()