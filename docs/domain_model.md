# Domain Model

## GameSession

Top-level runtime state.

Contains:

- WorldState
- players
- last_report
- last_processed_at

## WorldState

Shared world state.

Contains:

- stations
- routes
- factions
- events
- contracts
- pvp_impacts
- current_tick

## PlayerState

Per-player state.

Contains:

- id
- name
- crew
- inventory
- reputation
- assets
- active_actions
- completed_actions

## CrewState

Aggregate crew state.

Contains:

- members
- health
- morale
- fatigue
- specialization
- current_location_id
- destination_location_id
- is_traveling
- crew_members

## CrewMemberState

Individual crew member.

Contains:

- id
- name
- role
- health
- morale
- fatigue
- skills
- traits
- status
- current_location_id
- assigned_action_id

## PlayerAction

Timed execution unit.

Contains:

- id
- player_id
- action_type
- target_type
- target_id
- started_tick
- duration_ticks
- completes_at_tick
- status
- assigned_crew_member_ids
- payload

## ContractState

Playable offer that creates actions.

Contains:

- id
- title
- issuer
- target
- action_type
- cost
- reward
- effects
- status
- linked_action_id

## PlayerAsset

Persistent player-owned infrastructure.

Contains:

- owner_player_id
- asset_type
- station_id
- route_id
- level
- condition
- status
- effects

## StationState

Shared world object.

Contains:

- resources
- population
- stats
- pressure
- faction_influence
- market

## RouteState

Connection between stations.

Contains:

- from_station_id
- to_station_id
- travel_time_ticks
- danger_level
- status
- control
- modifiers