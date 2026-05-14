from fastapi import FastAPI

from metro_sim.interfaces.api.routes import (
    action_routes,
    admin_routes,
    event_routes,
    faction_routes,
    health_routes,
    player_routes,
    route_routes,
    station_routes,
    world_routes,
)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Metro Sim API",
        version="0.1.0",
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

    return app


app = create_app()