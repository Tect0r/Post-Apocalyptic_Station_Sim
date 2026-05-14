# Metro Sim API

## Run locally

```powershell
$env:PYTHONPATH="src"
uvicorn metro_sim.interfaces.api.app:app --reload
Docs
http://127.0.0.1:8000/docs
Core Endpoints
GET  /health
GET  /world
GET  /stations
GET  /stations/{station_id}
GET  /routes
GET  /routes/{route_id}
GET  /factions
GET  /events
GET  /player/me
GET  /player/me/crew
GET  /player/me/actions
POST /player/me/actions
POST /admin/tick
POST /admin/save
POST /admin/load
GET  /admin/saves
Current limitation

Authentication is not implemented yet.
All player endpoints use the fixed development player:

player_001