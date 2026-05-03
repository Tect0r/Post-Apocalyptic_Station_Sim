
def create_initial_station():
    return {
        "name": "Paveletskaya",
        "day": 1,
        "date": "01.01.2033",

    "population": {
        "total": 200,
        "employed": 150,
        "unemployed": 50
    },

    "resources": {
        "food": 1000,
        "water": 500,
        "medicine": 200,
        "power_usage": 50,
        "trade_goods": 100,
        "ammo": 300
    },

    "stats": {
        "morale": 80,
        "comfort": 70,
        "safety": 90,
        "power_stability": 85,
        "power_level": 2
    },

    "work_assignment": {
        "food_production": 50,
        "service_work": 30,
        "trading_goods_production": 20,
        "trading": 15,
        "guards": 35
    }
}