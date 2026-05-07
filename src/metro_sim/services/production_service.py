from metro_sim.utils.file_loader import load_balancing, load_buildings_cost_data, load_buildings_effects_data
import metro_sim.services.report_service as report_service

def calculate_mushroom_production(station: dict, effects: dict) -> int:
    # Berechnet die Pilzproduktion basierend auf den zugewiesenen Arbeitern und der Infrastruktur
    workers = station["employment"]["mushroom_production"]
    amount = workers * effects["food_per_worker"]
    return amount

def calculate_pig_production(station: dict, effects: dict) -> int:
    # Berechnet die Schweineproduktion basierend auf den zugewiesenen Arbeitern und der Infrastruktur
    workers = station["employment"]["pig_production"]
    amount = workers * effects["food_per_worker"]
    return amount

def calculate_kitchen_production(station: dict, effects: dict) -> int:
    # Berechnet die Nahrungsproduktion basierend auf den zugewiesenen Arbeitern und der Infrastruktur
    # nimm 1 pilz 1 pig und mach daraus 1 soup
    #strom verbrauch balancen
    # suppe gibt komfort
    return 0

def calculate_trade_goods_production(station: dict, effects: dict) -> int:
    # Berechnet die Produktion von Handelsgütern basierend auf den zugewiesenen Arbeitern und der Infrastruktur
    workers = station["employment"]["trade_goods_production"]
    amount = workers * effects["trade_goods_per_worker"]
    return amount

def calculate_machine_shop_production(station: dict, effects: dict) -> int:
    # Berechnet die Produktion von Ersatzteilen basierend auf den zugewiesenen Arbeitern und der Infrastruktur
    workers = station["employment"]["machine_shop"]
    amount = workers * effects["spare_parts_per_worker"]
    return amount

def calculate_medical_production(station: dict, effects: dict) -> int:
    # Berechnet die medizinische Produktion basierend auf den zugewiesenen Arbeitern und der Infrastruktur
    workers = station["employment"]["medical"]
    amount = workers * effects["medicine_per_worker"]
    return amount

def calculate_production_for_tick(station: dict) -> dict:
    """
    Berechnet die Produktion für einen einzelnen Tick.

    Ein Tick erhöht den Produktionsfortschritt belegter Gebäudeslots.
    Wenn der Fortschritt eines Gebäudes den Wert `ticks_per_yield`
    erreicht, wird der passende Ertrag erzeugt und der Fortschritt
    des Slots zurückgesetzt.

    Gibt einen Report mit den erzeugten resourcen und Effekten zurück.
    """

    building_slots = station.get("slots", {})
    building_effects = load_buildings_effects_data()

    report = report_service.create_empty_report()

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
            amount = calculate_mushroom_production(station, effects)
            station["resources"]["mushrooms"] += amount
            report_service.add_resource_change(report, "mushrooms", amount)

        case "pig_farm":
            amount = calculate_pig_production(station, effects)

            station["resources"]["pigs"] += amount
            report_service.add_resource_change(report, "pigs", amount)

        case "trading_goods":
            amount = calculate_trade_goods_production(station, effects)

            station["resources"]["trade_goods"] += amount
            report_service.add_resource_change(report, "trade_goods", amount)

        case "machine_shop":
            amount = calculate_machine_shop_production(station, effects)

            station["resources"]["spare_parts"] += amount
            report_service.add_resource_change(report, "spare_parts", amount)

        case "medical":
            amount = calculate_medical_production(station, effects)

            station["resources"]["medicine"] += amount
            report_service.add_resource_change(report, "medicine", amount)

        case "generator":
            # Generator erzeugt keine lagerbare resource,
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

            report_service.add_stat_change(report, "morale", morale_bonus)

        case "market":
            morale_bonus = effects["morale_bonus"]

            station["stats"]["morale"] = min(
                100,
                station["stats"]["morale"] + morale_bonus
            )

            report_service.add_stat_change(report, "morale", morale_bonus)

        case "station_leadership":
            # Passive Effekte wie Effizienzbonus oder Verlustreduktion
            # werden später besser zentral in den jeweiligen Berechnungen genutzt.
            report["messages"].append("Stationsleitung koordiniert die Arbeit.")

        case "stalker_den":
            # Loot-Logik später mit Zufall/Event-System.
            report["messages"].append("Stalker bereiten eine Expedition vor.")

        case "kitchen":
            amount = calculate_kitchen_production(station, effects)

            report["messages"].append("Küche verbessert die Essensversorgung.")

        case _:
            report["messages"].append(f"Kein Yield für Gebäude '{building}' definiert.")
                    
