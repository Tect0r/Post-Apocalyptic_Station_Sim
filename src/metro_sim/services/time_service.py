from datetime import datetime, timedelta

from metro_sim.utils.file_loader import load_balancing

from datetime import datetime, timedelta


def advance_time(station: dict, ticks: int) -> None:
    balancing = load_balancing()
    minutes_per_tick = balancing["time"]["minutes_per_tick"]

    station["time"]["ticks_total"] += ticks

    total_minutes = station["time"]["minute"] + ticks * minutes_per_tick

    added_hours = total_minutes // 60
    station["time"]["minute"] = total_minutes % 60

    total_hours = station["time"]["hour"] + added_hours

    added_days = total_hours // 24
    station["time"]["hour"] = total_hours % 24

    if added_days > 0:
        station["time"]["day"] += added_days

        date_format = "%d.%m.%Y"
        current_date = datetime.strptime(station["time"]["date"], date_format)
        new_date = current_date + timedelta(days=added_days)
        station["time"]["date"] = new_date.strftime(date_format)
                