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
                    "current_location_id": player.crew.current_location_id,
                    "destination_location_id": player.crew.destination_location_id,
                    "is_traveling": player.crew.is_traveling,
                    "crew_members": [
                        {
                            "id": member.id,
                            "name": member.name,
                            "role": member.role,
                            "health": member.health,
                            "morale": member.morale,
                            "fatigue": member.fatigue,
                            "skills": member.skills,
                            "traits": member.traits,
                            "status": member.status.value if hasattr(member.status, "value") else member.status,
                            "current_location_id": member.current_location_id,
                            "assigned_action_id": member.assigned_action_id,
                        }
                        for member in player.crew.crew_members
                    ],
                },
                "inventory": player.inventory.items,
                "reputation": player.reputation.values,
                "assets": [
                    {
                        "id": asset.id,
                        "owner_player_id": asset.owner_player_id,
                        "name": asset.name,
                        "asset_type": asset.asset_type,
                        "station_id": asset.station_id,
                        "route_id": asset.route_id,
                        "level": asset.level,
                        "condition": asset.condition,
                        "status": asset.status.value if hasattr(asset.status, "value") else asset.status,
                        "effects": asset.effects,
                        "metadata": asset.metadata,
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
                "completed_actions": [
                    {
                        "id": action.id,
                        "action_type": action.action_type.value,
                        "target_type": action.target_type,
                        "target_id": action.target_id,
                        "started_tick": action.started_tick,
                        "duration_ticks": action.duration_ticks,
                        "completes_at_tick": action.completes_at_tick,
                        "status": action.status.value if hasattr(action.status, "value") else action.status,
                    }
                    for action in player.completed_actions[-20:]
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
                "complex_id": station.complex_id,
                "line": station.line,
                "inhabited": station.inhabited,
                "tags": station.tags,
                "market": station.market,
                "ui": station.ui,
            }
            for station_id, station in session.world.stations.items()
        },
        "routes": {
            route_id: {
                "id": route.id,
                "from_station_id": route.from_station_id,
                "to_station_id": route.to_station_id,
                "route_type": route.route_type,
                "distance": route.distance,
                "travel_time_ticks": route.travel_time_ticks,
                "danger": route.danger,
                "traffic": route.traffic,
                "condition": route.condition,
                "control": route.control,
                "pressure": route.pressure,
                "tags": route.tags,
                "display_name": route.display_name,
                "line": route.line,
                "bidirectional": route.bidirectional,
                "ui": route.ui,
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
                "event_type": event.event_type,
                "target_type": event.target_type,
                "target_id": event.target_id,
                "started_at_tick": event.started_at_tick,
                "status": event.status,
                "severity": event.severity,
                "causes": event.causes,
                "data": event.data,
                "duration_ticks": event.duration_ticks,
                "ends_at_tick": event.ends_at_tick,
                "current_phase": event.current_phase,
            }
            for event in session.world.events[-10:]
        ],
        "movements": [
            {
                "id": movement.id,
                "actor_type": movement.actor_type,
                "actor_id": movement.actor_id,
                "from_station_id": movement.from_station_id,
                "to_station_id": movement.to_station_id,
                "station_path": movement.station_path,
                "route_path": movement.route_path,
                "started_at_tick": movement.started_at_tick,
                "arrives_at_tick": movement.arrives_at_tick,
                "status": movement.status,
                "progress": calculate_movement_progress(
                    current_tick=session.world.current_tick,
                    started_at_tick=movement.started_at_tick,
                    arrives_at_tick=movement.arrives_at_tick,
                ),
                "data": movement.data,
            }
            for movement in session.world.movements
        ],
        "npc_traders": {
            trader_id: {
                "id": trader.id,
                "name": trader.name,
                "current_station_id": trader.current_station_id,
                "home_station_id": trader.home_station_id,
                "status": trader.status,
                "target_station_id": trader.target_station_id,
                "active_movement_id": trader.active_movement_id,
                "rest_until_tick": trader.rest_until_tick,
                "inventory": trader.inventory,
                "data": trader.data,
            }
            for trader_id, trader in session.world.npc_traders.items()
        },
        "logs": [
            {
                "id": log.id,
                "tick": log.tick,
                "category": log.category,
                "message": log.message,
                "target_type": log.target_type,
                "target_id": log.target_id,
                "importance": log.importance,
                "data": log.data,
            }
            for log in session.world.logs[-50:]
        ],
    }

def calculate_movement_progress(
    *,
    current_tick: int,
    started_at_tick: int,
    arrives_at_tick: int,
) -> float:
    duration = arrives_at_tick - started_at_tick

    if duration <= 0:
        return 1.0

    progress = (current_tick - started_at_tick) / duration
    return max(0.0, min(1.0, progress))