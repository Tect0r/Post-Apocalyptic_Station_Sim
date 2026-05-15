# Post-Apocalyptic Station Sim

A multiplayer-oriented browser game prototype about managing a crew in a shared post-apocalyptic metro world.

Players do not control stations directly. Instead, they manage a crew, accept contracts, move through routes, trade at station markets, build personal assets and influence the shared world through pressure, events and indirect PvP.

## Current Stack

- Python
- FastAPI
- React
- TypeScript
- JSON persistence for development
- pytest

## Current Features

- Authentication
- Shared world state
- Crew management
- Individual crew members
- Tick-based server clock
- Actions and completed action history
- Contracts
- Route movement
- Player assets
- Station-local markets
- World events
- Pressure and faction influence
- Indirect PvP
- Web dashboard

## Run Backend

```powershell
$env:PYTHONPATH="src"
uvicorn metro_sim.interfaces.api.app:app --reload
Run Frontend
cd frontend
npm install
npm run dev
Run Tests
python -m compileall src
pytest
cd frontend
npm run build
cd ..
Documentation

See:

docs/system_overview.md
docs/domain_model.md
docs/api.md
docs/web_ui.md
docs/tick_model.md
docs/gameplay_loop.md
docs/data_files.md
docs/testing.md
docs/roadmap.md