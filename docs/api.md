# Metro Sim API

## Run locally

```powershell
$env:PYTHONPATH="src"
uvicorn metro_sim.interfaces.api.app:app --reload
API Docs
http://127.0.0.1:8000/docs
Core Principles
One shared server world
Many authenticated users
One PlayerState per user
Player actions affect the shared world
The client does not manually tick the simulation
The server processes elapsed real time into game ticks
Authentication
POST /auth/register
POST /auth/login
POST /auth/logout

Protected endpoints require:

Authorization: Bearer <access_token>
World
GET /health
GET /world
GET /stations
GET /stations/{station_id}
GET /routes
GET /routes/{route_id}
GET /factions
GET /events

Important rule:

GET /world processes elapsed server time into game ticks.
Most other GET endpoints only read current state.
Player
GET /player
GET /player/me
GET /player/me/identity
GET /player/me/crew
GET /player/me/actions
Actions
POST /player/me/actions
POST /player/me/actions/{action_id}/cancel

Actions are tick-based:

started_tick
duration_ticks
completes_at_tick
status
assigned_crew_member_ids
Contracts
GET /contracts
GET /contracts/{contract_id}
POST /contracts/{contract_id}/accept

Contracts are playable offers. Accepting a contract creates a timed PlayerAction.

Movement
POST /player/me/movement/start

Movement creates a timed action and updates crew location after completion.

Assets
GET /player/me/assets
POST /player/me/assets
POST /player/me/assets/{asset_id}/upgrade
POST /player/me/assets/{asset_id}/repair

Players own assets. Players do not build or control stations directly.

Market
GET /market
GET /market/stations/{station_id}
POST /market/buy
POST /market/sell

Markets are station-local. The player can trade at the current crew location.

Indirect PvP
GET /pvp/impacts
POST /pvp/station-pressure
POST /pvp/damage-asset

PvP is indirect and world-driven. No direct account destruction. Assets may be damaged, not permanently deleted.

Admin / Debug
POST /admin/save
POST /admin/load
GET /admin/saves
POST /admin/tick

POST /admin/tick is a debug endpoint only. It is not part of the normal player loop.