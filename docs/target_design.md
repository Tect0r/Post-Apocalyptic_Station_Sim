# Target Design

## Core Direction

Metro Sim is a multiplayer-oriented browser game about managing a crew in a shared post-apocalyptic metro world.

The player does not own a station. The player owns:

- crew
- inventory
- reputation
- assets
- contracts
- active actions
- completed actions
- networks and influence

## Shared World

The world contains:

- stations
- routes
- factions
- events
- contracts
- markets
- PvP impacts

All players interact with the same WorldState.

## Player Progression

Progression comes from:

- better crew members
- better assets
- reputation
- trade opportunities
- access to better contracts
- safer route access
- faction relationships

## No Direct Station Management

Players do not directly assign station workers, build station buildings, control station production or own entire stations.

## Tick Model

The simulation is tick-based.

Currently:

```text
1 real second = 1 game tick

The server advances game ticks. The frontend only reads state and sends player decisions.

PvP Philosophy

PvP is indirect.

Allowed:

pressure manipulation
faction influence
market pressure
asset damage
contract competition

Not allowed as core flow:

permanent account destruction
unrestricted direct attacks
asset deletion without counterplay