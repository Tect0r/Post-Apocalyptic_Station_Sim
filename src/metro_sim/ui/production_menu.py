def create_employment_menu(station: dict) -> tuple[list[str], dict[str, str]]:
    station_slots = station.get("slots", {})

    job_order = [
        "mushroom_production",
        "pig_production",
        "kitchen_work",
        "maintenance",
        "trade_goods_production",
        "trading",
        "guards",
        "medical",
        "machine_shop",
        "stalker_expedition",
        "service_work",
    ]

    building_to_job = {
        "mushroom_farm": "mushroom_production",
        "pig_farm": "pig_production",
        "kitchen": "kitchen_work",
        "maintenance": "maintenance",
        "trading_goods": "trade_goods_production",
        "trading_post": "trading",
        "guard_post": "guards",
        "medical": "medical",
        "machine_shop": "machine_shop",
        "stalker_den": "stalker_expedition",
        "bar": "service_work",
        "market": "service_work",
    }

    job_to_label = {
        "mushroom_production": "Pilzfarm",
        "pig_production": "Schweinefarm",
        "kitchen_work": "Küche",
        "maintenance": "Wartung",
        "trade_goods_production": "Handelswarenproduktion",
        "trading": "Handel",
        "guards": "Wachen",
        "medical": "Medizin",
        "machine_shop": "Werkstatt",
        "stalker_expedition": "Stalker-Expedition",
        "service_work": "Service / Bar / Markt",
    }

    available_jobs = set()

    for slot in station_slots.values():
        building = slot.get("building")
        level = slot.get("level", 0)

        if building is None or level <= 0:
            continue

        job = building_to_job.get(building)

        if job is not None:
            available_jobs.add(job)

    ordered_jobs = [job for job in job_order if job in available_jobs]

    menu_lines = ["Bewohner zuweisen:"]
    menu_actions = {}

    for index, job in enumerate(ordered_jobs, start=1):
        key = str(index)
        label = job_to_label.get(job, job)

        menu_lines.append(f"{key}. {label}")
        menu_actions[key] = job

    menu_lines.append("0. Zurück")

    return menu_lines, menu_actions