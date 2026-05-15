# Web UI

## Run backend

```powershell
$env:PYTHONPATH="src"
uvicorn metro_sim.interfaces.api.app:app --reload
Run frontend
cd frontend
npm install
npm run dev
URLs
Frontend: http://localhost:5173
Backend:  http://127.0.0.1:8000
API docs: http://127.0.0.1:8000/docs
Current UI Scope

Implemented panels:

Authentication
Dashboard
Crew status
Individual crew members
Inventory
Active actions
Completed actions
Contracts
Stations
Station details
Routes and movement
Events
Assets
Market
Indirect PvP impacts
Tick Behavior

The frontend does not control simulation time.

The backend processes elapsed real time into game ticks. The dashboard auto-refreshes and displays the current world state.

Important UI Rule

The frontend should not call debug tick endpoints as part of normal gameplay.