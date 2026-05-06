import metro_sim.utils.file_loader as loader

def calculate_trade_goods_consumption(station: dict) -> int:
    # Berechnet den Verbrauch von Handelsgütern basierend auf der Bevölkerung und den zugewiesenen Arbeitern
    balancing_dict = loader.load_balancing()
    trade_goods_consumption = station['work_assignment']['trading'] * balancing_dict["trade_post"]["trade_capacity_per_worker_by_level"][str(station['infrastructure_levels']['trade_post'])]
    ammo_gained = station['work_assignment']['trading'] * balancing_dict["trade_goods"]["ammo_per_trade_good"]
    return trade_goods_consumption, ammo_gained