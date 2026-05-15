# Testing Guide

## Run tests

```powershell
python -m compileall src
pytest
Frontend build
cd frontend
npm run build
cd ..
Auth Test Users

Tests that create users should clean them up.

Use:

with authenticated_test_user(client) as auth:
    ...

Do not manually register users without cleanup.

Tick Tests

Core tests may use:

advance_tick(session)

API/player-flow tests should not use /admin/tick as normal gameplay.

To test server-time processing, manipulate last_processed_at and call /world.

Read Endpoint Rule

Only /world should normally process elapsed ticks.

Read endpoints like /player/me, /contracts, /market, /pvp/impacts should not process ticks.

Test Categories
Unit tests: services
Integration tests: GameSession, persistence
API tests: FastAPI routes
Frontend build: TypeScript validity