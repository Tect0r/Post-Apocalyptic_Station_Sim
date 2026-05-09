def ask_until_valid(valid_inputs: set[str], prompt: str = "> ") -> str:
    while True:
        user_input = input(prompt).strip().lower()

        if user_input in valid_inputs:
            return user_input

        print("Ungültige Eingabe.")

RESOURCE_CATEGORY_MAP = {
    # food
    "mushrooms": "food",
    "pigs": "food",
    "pig_meat": "food",
    "soup": "food",
    "meat_soup": "food",
    "water": "food",

    # mechanical
    "trade_goods": "mechanical",
    "spare_parts": "mechanical",
    "scrap": "mechanical",
    "mechanical_parts": "mechanical",
    "power_units": "mechanical",

    # combat
    "ammo": "combat",
    "fuel": "combat",
    "rare_loot": "combat",
    "medicine": "combat",
    "chemicals": "combat",

    # trash
    "organic_waste": "trash",
}

def get_resource_category(resource_name: str) -> str:
    category = RESOURCE_CATEGORY_MAP.get(resource_name)

    if category is None:
        raise KeyError(f"Unknown resource: {resource_name}")

    return category


def add_resource(station: dict, resource_name: str, amount: int | float) -> None:
    category = get_resource_category(resource_name)

    station["resources"][category][resource_name] = (
        station["resources"][category].get(resource_name, 0) + amount
    )

def remove_resource(station: dict, resource_name: str, amount: int | float) -> None:
    category = get_resource_category(resource_name)

    station["resources"][category][resource_name] = max((station["resources"][category].get(resource_name, 0) - amount), 0)

def get_resource_amount(station: dict, resource_name: str) -> int | float:
    category = get_resource_category(resource_name)
    return station["resources"][category].get(resource_name, 0)