def station_matches_event_rule(station, rule: dict) -> bool:
    pressure_conditions = rule.get("station_pressure", {})

    for pressure_key, condition in pressure_conditions.items():
        current_value = station.pressure.get(pressure_key, 0)
        min_value = condition.get("min", 0)
        max_value = condition.get("max")

        if current_value < min_value:
            return False

        if max_value is not None and current_value > max_value:
            return False

    return True