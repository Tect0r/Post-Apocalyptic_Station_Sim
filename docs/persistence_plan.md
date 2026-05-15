# Persistence Plan

## Current JSON Persistence

Current save structure:

```text
saves/
  <save_name>/
    metadata.json
    world_state.json
    players.json

saves/auth/
  users.json
Saved State

World save includes:

stations
routes
factions
events
contracts
pvp_impacts
markets

Player save includes:

crew
crew members
inventory
reputation
assets
active actions
completed actions

Metadata includes:

save_version
save_name
saved_at
last_processed_at
Future PostgreSQL Target

Tables:

users
players
crews
crew_members
inventory
player_actions
contracts
player_assets
stations
station_market
routes
factions
events
pvp_impacts
market_transactions