from metro_sim.services import time_service
from metro_sim.services.simulation_service import simulate_next_day
from metro_sim.utils.file_loader import load_balancing, load_buildings_data, load_buildings_effects_data
import metro_sim.services.production_service as production_service
import metro_sim.services.consumption_service as consumption_service
from metro_sim.services.report_service import add_resource_change, add_stat_change


def calculate_next_tick(station: dict, report: dict) -> dict:
    # Berechnet die Ereignisse des nächsten Ticks und aktualisiert den Stationsstatus entsprechend
    time_service.advance_time(station, 1)
    balancing_dict = load_balancing()

    if station["time"]["hour"] >= balancing_dict["time"]["work_start_hour"] and station["time"]["hour"] <= balancing_dict["time"]["work_end_hour"]:
        production_report = calculate_production_for_tick(station)
        merge_reports(report, production_report)

    consumption_report = calculate_consumption_for_tick(station)
        
    merge_reports(report, consumption_report)

def merge_reports(target: dict, source: dict) -> None:
    for resource, change in source.get("resource_changes", {}).items():
        target["resource_changes"][resource] = (
            target["resource_changes"].get(resource, 0) + change
        )

    for stat, change in source.get("stat_changes", {}).items():
        target["stat_changes"][stat] = (
            target["stat_changes"].get(stat, 0) + change
        )

    target["messages"].extend(source.get("messages", []))

def calculate_consumption_for_tick(station: dict) -> dict:
    balancing = load_balancing()

    report = {
        "resource_changes": {},
        "stat_changes": {},
        "messages": []
    }

    is_meal_time = (
        station["time"]["hour"] in balancing["time"]["meal_hours"]
        and station["time"]["minute"] == 0
    )

    if is_meal_time:
        consumption_service.apply_food_consumption(station, report=report)

    return report

def calculate_production_for_tick(station: dict) -> dict:
    """
    Berechnet die Produktion für einen einzelnen Tick.

    Ein Tick erhöht den Produktionsfortschritt belegter Gebäudeslots.
    Wenn der Fortschritt eines Gebäudes den Wert `ticks_per_yield`
    erreicht, wird der passende Ertrag erzeugt und der Fortschritt
    des Slots zurückgesetzt.

    Gibt einen Report mit den erzeugten Ressourcen und Effekten zurück.
    """

    building_slots = station.get("slots", {})
    building_effects = load_buildings_effects_data()

    report = {
        "resource_changes": {},
        "stat_changes": {},
        "messages": []
    }

    for slot_id, slot in building_slots.items():
        building = slot.get("building")
        level = slot.get("level", 0)

        if building is None or level <= 0:
            continue

        level_key = str(level)
        effects = building_effects[building]["effects_by_level"][level_key]

        ticks_per_yield = effects.get("ticks_per_yield")

        if ticks_per_yield is None:
            continue

        slot["production_progress"] += 1

        if slot["production_progress"] < ticks_per_yield:
            continue

        slot["production_progress"] = 0

        apply_building_yield(
            station=station,
            building=building,
            effects=effects,
            report=report
        )

    return report

def apply_building_yield(
    station: dict,
    building: str,
    effects: dict,
    report: dict
) -> None:
    """
    Wendet den Ertrag eines Gebäudes an, sobald dessen Produktionsintervall
    abgeschlossen ist.
    """

    match building:
        case "mushroom_farm":
            amount = production_service.calculate_mushroom_production(station, effects)
            station["ressources"]["mushrooms"] += amount
            add_resource_change(report, "mushrooms", amount)

        case "pig_farm":
            amount = production_service.calculate_pig_production(station, effects)

            station["ressources"]["pigs"] += amount
            add_resource_change(report, "pigs", amount)

        case "trading_goods":
            amount = production_service.calculate_trade_goods_production(station, effects)

            station["ressources"]["trade_goods"] += amount
            add_resource_change(report, "trade_goods", amount)

        case "machine_shop":
            amount = production_service.calculate_machine_shop_production(station, effects)

            station["ressources"]["spare_parts"] += amount
            add_resource_change(report, "spare_parts", amount)

        case "medical":
            amount = production_service.calculate_medical_production(station, effects)

            station["ressources"]["medicine"] += amount
            add_resource_change(report, "medicine", amount)

        case "generator":
            # Generator erzeugt keine lagerbare Ressource,
            # sondern kann später die verfügbare kWh-Leistung erhöhen.
            #amount = effects["kwh_per_day"]
            #add_resource_change(report, "generated_kwh", amount)
            pass

        case "bar":
            morale_bonus = effects["morale_bonus_per_day"]

            station["stats"]["morale"] = min(
                100,
                station["stats"]["morale"] + morale_bonus
            )

            add_stat_change(report, "morale", morale_bonus)

        case "market":
            morale_bonus = effects["morale_bonus"]

            station["stats"]["morale"] = min(
                100,
                station["stats"]["morale"] + morale_bonus
            )

            add_stat_change(report, "morale", morale_bonus)

        case "station_leadership":
            # Passive Effekte wie Effizienzbonus oder Verlustreduktion
            # werden später besser zentral in den jeweiligen Berechnungen genutzt.
            report["messages"].append("Stationsleitung koordiniert die Arbeit.")

        case "stalker_den":
            # Loot-Logik später mit Zufall/Event-System.
            report["messages"].append("Stalker bereiten eine Expedition vor.")

        case "kitchen":
            amount = production_service.calculate_kitchen_production(station, effects)

            report["messages"].append("Küche verbessert die Essensversorgung.")

        case _:
            report["messages"].append(f"Kein Yield für Gebäude '{building}' definiert.")
                    
