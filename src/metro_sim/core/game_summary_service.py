from metro_sim.core.game_session import GameSession


def build_game_summary(session: GameSession) -> dict:
    return {
        "tick": session.world.current_tick,
        "players": {
            player_id: {
                "id": player.id,
                "name": player.name,
                "crew": {
                    "members": player.crew.members,
                    "health": player.crew.health,
                    "morale": player.crew.morale,
                    "fatigue": player.crew.fatigue,
                    "specialization": player.crew.specialization,
                },
                "inventory": player.inventory.items,
                "reputation": player.reputation.values,
                "assets": [
                    {
                        "id": asset.id,
                        "name": asset.name,
                        "asset_type": asset.asset_type,
                        "location_id": asset.location_id,
                        "condition": asset.condition,
                    }
                    for asset in player.assets
                ],
                "active_actions": [
                    {
                        "id": action.id,
                        "action_type": action.action_type.value,
                        "target_type": action.target_type,
                        "target_id": action.target_id,
                        "started_tick": action.started_tick,
                        "duration_ticks": action.duration_ticks,
                        "completes_at_tick": action.completes_at_tick,
                        "status": action.status,
                    }
                    for action in player.active_actions
                ],
            }
            for player_id, player in session.players.items()
        },
        "stations": {
            station_id: {
                "id": station.id,
                "name": station.name,
                "station_type": station.station_type,
                "description_key": station.description_key,
                "resources": station.resources,
                "population": station.population,
                "stats": station.stats,
                "pressure": station.pressure,
                "faction_influence": station.faction_influence,
            }
            for station_id, station in session.world.stations.items()
        },
        "routes": {
            route_id: {
                "id": route.id,
                "from_station_id": route.from_station_id,
                "to_station_id": route.to_station_id,
                "distance": route.distance,
                "danger_level": route.danger_level,
                "status": route.status,
                "modifiers": route.modifiers,
            }
            for route_id, route in session.world.routes.items()
        },
        "factions": {
            faction_id: {
                "id": faction.id,
                "name": faction.name,
                "resources": faction.resources,
                "relations": faction.relations,
                "controlled_stations": faction.controlled_stations,
            }
            for faction_id, faction in session.world.factions.items()
        },
        "events": [
            {
                "id": event.id,
                "tick": event.tick,
                "station_id": event.station_id,
                "event_type": event.event_type,
                "severity": event.severity,
                "description_key": event.description_key,
            }
            for event in session.world.events[-10:]
        ],
    }