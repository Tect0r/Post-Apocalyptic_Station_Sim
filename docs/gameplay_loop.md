# Gameplay Loop

## Current Loop

1. Login
2. Check crew status
3. Check current station and market
4. Review available contracts
5. Assign crew/action/contract
6. Wait for server ticks
7. Collect result
8. Upgrade assets / repair / trade / move
9. React to events and world pressure

## Crew Loop

- crew members have roles, skills, fatigue and status
- actions can assign crew members
- movement changes crew location
- future systems will use skills for success chance

## Contract Loop

- contracts are available in the shared world
- accepting a contract starts a timed PlayerAction
- completing the action completes the linked contract
- contracts may grant inventory, reputation, assets or world effects

## Market Loop

- markets are station-local
- crew can trade at current station
- prices differ by station
- assets may affect prices
- movement enables trade opportunities

## Indirect PvP Loop

- players influence shared station pressure
- players can damage assets indirectly
- PvP impacts are logged
- cooldowns and detection reduce toxicity