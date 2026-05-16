from metro_sim.world.models.npc_trader import NpcTrader, create_npc_trader


def create_initial_npc_traders() -> dict[str, NpcTrader]:
    traders: dict[str, NpcTrader] = {}

    trader = create_npc_trader(
        name="Paveletskaya Supply Trader",
        current_station_id="paveletskaya_ring",
        home_station_id="paveletskaya_ring",
        inventory={
            "food": 20,
            "water": 15,
            "medicine": 3,
            "trade_goods": 10
        },
        data={
            "rest_duration_ticks": 30,
            "preferred_targets": [
                "paveletskaya_radial",
                "dobryninskaya_serpukhovskaya",
                "tulskaya"
            ]
        },
    )

    traders[trader.id] = trader

    return traders