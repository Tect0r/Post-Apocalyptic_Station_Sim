from metro_sim.world.models.world_effect import WorldEffect
from metro_sim.world.models.world_log_entry import WorldLogEntry, create_world_log_entry
from metro_sim.world.models.world_state import WorldState


def process_factions_tick(world: WorldState) -> tuple[list[WorldEffect], list[WorldLogEntry]]:
    effects: list[WorldEffect] = []
    logs: list[WorldLogEntry] = []

    station_effects, station_logs = process_station_faction_influence(world)
    route_effects, route_logs = process_route_faction_control(world)

    effects.extend(station_effects)
    effects.extend(route_effects)

    logs.extend(station_logs)
    logs.extend(route_logs)

    return effects, logs


def process_station_faction_influence(
    world: WorldState,
) -> tuple[list[WorldEffect], list[WorldLogEntry]]:
    effects: list[WorldEffect] = []
    logs: list[WorldLogEntry] = []

    for station_id, station in world.stations.items():
        station.id = station_id

        influence = getattr(station, "faction_influence", {}) or {}

        hansa = influence.get("hansa", 0)
        bandits = influence.get("bandits", 0)
        polis = influence.get("polis", 0)
        independent = influence.get("independent", 0)

        if hansa >= 60:
            effects.append(
                WorldEffect(
                    target_type="station",
                    target_id=station_id,
                    field_path=["stats", "order"],
                    operation="add",
                    value=1,
                    reason="strong_hansa_influence",
                    source="faction_system",
                    importance="debug",
                )
            )

        if polis >= 60:
            effects.append(
                WorldEffect(
                    target_type="station",
                    target_id=station_id,
                    field_path=["stats", "security"],
                    operation="add",
                    value=1,
                    reason="strong_polis_influence",
                    source="faction_system",
                    importance="debug",
                )
            )

        if bandits >= 40:
            effects.extend([
                WorldEffect(
                    target_type="station",
                    target_id=station_id,
                    field_path=["pressure", "smuggling"],
                    operation="add",
                    value=1,
                    reason="strong_bandit_influence",
                    source="faction_system",
                    importance="debug",
                ),
                WorldEffect(
                    target_type="station",
                    target_id=station_id,
                    field_path=["pressure", "security_risk"],
                    operation="add",
                    value=1,
                    reason="strong_bandit_influence",
                    source="faction_system",
                    importance="debug",
                ),
            ])

        if independent <= 20:
            effects.append(
                WorldEffect(
                    target_type="station",
                    target_id=station_id,
                    field_path=["pressure", "faction_tension"],
                    operation="add",
                    value=1,
                    reason="weak_independent_influence",
                    source="faction_system",
                    importance="debug",
                )
            )

        logs.append(
            create_world_log_entry(
                tick=world.current_tick,
                category="faction_station_processed",
                message=f"Faction influence processed for station: {station_id}",
                target_type="station",
                target_id=station_id,
                importance="debug",
                data={
                    "faction_influence": influence,
                },
            )
        )

    return effects, logs


def process_route_faction_control(
    world: WorldState,
) -> tuple[list[WorldEffect], list[WorldLogEntry]]:
    effects: list[WorldEffect] = []
    logs: list[WorldLogEntry] = []

    for route_id, route in world.routes.items():
        route.id = route_id

        control = getattr(route, "control", {}) or {}

        hansa = control.get("hansa", 0)
        bandits = control.get("bandits", 0)
        polis = control.get("polis", 0)

        connected_station_ids = get_connected_station_ids(
            world=world,
            route=route,
        )

        if bandits >= 40:
            for station_id in connected_station_ids:
                effects.extend([
                    WorldEffect(
                        target_type="station",
                        target_id=station_id,
                        field_path=["pressure", "security_risk"],
                        operation="add",
                        value=1,
                        reason="bandit_route_control",
                        source="faction_system",
                        importance="debug",
                    ),
                    WorldEffect(
                        target_type="station",
                        target_id=station_id,
                        field_path=["pressure", "danger"],
                        operation="add",
                        value=1,
                        reason="bandit_route_control",
                        source="faction_system",
                        importance="debug",
                    ),
                ])

        if hansa >= 60:
            for station_id in connected_station_ids:
                effects.append(
                    WorldEffect(
                        target_type="station",
                        target_id=station_id,
                        field_path=["pressure", "supply_disruption"],
                        operation="subtract",
                        value=1,
                        reason="hansa_route_control",
                        source="faction_system",
                        importance="debug",
                    )
                )

        if polis >= 60:
            for station_id in connected_station_ids:
                effects.append(
                    WorldEffect(
                        target_type="station",
                        target_id=station_id,
                        field_path=["pressure", "security_risk"],
                        operation="subtract",
                        value=1,
                        reason="polis_route_control",
                        source="faction_system",
                        importance="debug",
                    )
                )

        logs.append(
            create_world_log_entry(
                tick=world.current_tick,
                category="faction_route_processed",
                message=f"Faction control processed for route: {route_id}",
                target_type="route",
                target_id=route_id,
                importance="debug",
                data={
                    "control": control,
                    "connected_stations": connected_station_ids,
                },
            )
        )

    return effects, logs


def get_connected_station_ids(
    *,
    world: WorldState,
    route,
) -> list[str]:
    station_ids = [
        getattr(route, "from_station_id", None),
        getattr(route, "to_station_id", None),
    ]

    return [
        station_id
        for station_id in station_ids
        if station_id in world.stations
    ]