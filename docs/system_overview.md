# System Overview

## Layers

```text
frontend/
  React + TypeScript

src/metro_sim/interfaces/api/
  FastAPI routes and API schemas

src/metro_sim/core/
  GameSession, server clock, summaries

src/metro_sim/world/
  WorldState, stations, routes, factions, events

src/metro_sim/player/
  PlayerState, crew, actions, assets

src/metro_sim/contracts/
  contracts and contract lifecycle

src/metro_sim/market/
  station-local market logic

src/metro_sim/pvp/
  indirect PvP systems

src/metro_sim/persistence/
  JSON save/load layer
Request Flow
Frontend
  -> FastAPI route
    -> domain service
      -> GameSession / WorldState / PlayerState
        -> save if state changed
Shared World Principle

All authenticated players interact with the same server world.

Users do not get separate worlds.