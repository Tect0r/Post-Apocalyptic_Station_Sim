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
Frontend: http://http://localhost:5173/
Backend:  http://127.0.0.1:8000
API docs: http://127.0.0.1:8000/docs

Current UI scope
    Dashboard
    Crew status
    Inventory
    Active actions
    Stations
    Station details
    Routes
    Events
    Start action
    Manual tick