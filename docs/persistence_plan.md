# Persistence Plan

## Phase 10: JSON Save Files

Current persistence target:

```text
saves/
  <save_name>/
    metadata.json
    world_state.json
    players.json
Later Database Target

PostgreSQL is the target database for web and multiplayer.

Planned tables:

users
players
crews
player_inventory
player_assets
stations
station_resources
station_stats
station_pressure
factions
station_faction_influence
routes
actions
events
market_orders
Rule

JSON persistence is temporary infrastructure for development.
The game domain should not depend on JSON-specific details.
