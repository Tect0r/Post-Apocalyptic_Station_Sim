# Current State

## Game Model

The game is now a multiplayer-oriented crew management simulation.

Players do not control stations directly. Stations are shared world objects. Each registered user owns a PlayerState with crew, inventory, reputation, assets, active actions and completed actions.

## Core Systems

Implemented systems:

- Shared WorldState
- PlayerState and authentication
- individual CrewMemberState
- tick-based server clock
- PlayerAction lifecycle
- Contracts
- Routes and crew movement
- Station pressure and faction influence
- World events
- Player assets
- Station-local markets
- indirect PvP impacts
- JSON persistence
- FastAPI backend
- React/TypeScript frontend

## Tick Model

The game remains tick-based.

One real second currently equals one game tick.

The frontend does not advance the simulation manually. The backend processes elapsed real time into game ticks. The `/world` endpoint synchronizes server time for normal reads. Write endpoints may process elapsed ticks before applying player actions.

## Interface

The primary interface is now:

- FastAPI backend
- React/TypeScript web frontend

The old CLI is no longer the target interface.

## Persistence

The game currently uses JSON save files under `saves/`.

This is temporary development infrastructure. PostgreSQL is still the intended long-term persistence layer.