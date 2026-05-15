import { useState } from "react";
import type { MarketResponse } from "../../types/game";

type MarketPanelProps = {
  market: MarketResponse | null;
  onBuyItem: (itemId: string, amount: number) => Promise<void>;
  onSellItem: (itemId: string, amount: number) => Promise<void>;
};

export function MarketPanel({ market, onBuyItem, onSellItem }: MarketPanelProps) {
  const [amountByItem, setAmountByItem] = useState<Record<string, number>>({});

  if (!market) {
    return (
      <section className="panel" id="market">
        <h2>Market</h2>
        <p className="muted">No market data loaded.</p>
      </section>
    );
  }

  return (
    <section className="panel" id="market">
      <h2>Market</h2>
      <p className="muted">Current station: {market.station_id}</p>

      <div className="card-list">
        {Object.values(market.prices).map((price) => {
          const amount = amountByItem[price.item_id] ?? 1;

          return (
            <div className="route-card" key={price.item_id}>
              <strong>{price.label}</strong>
              <span>Item: {price.item_id}</span>
              <span>Category: {price.category}</span>
              <span>Buy Price: {price.buy_price} ammo</span>
              <span>Sell Price: {price.sell_price} ammo</span>
              <span>Stock: {price.stock}</span>

              <label>
                Amount
                <input
                  type="number"
                  min={1}
                  value={amount}
                  onChange={(event) =>
                    setAmountByItem({
                      ...amountByItem,
                      [price.item_id]: Number(event.target.value),
                    })
                  }
                />
              </label>

              <div className="button-row">
                <button onClick={() => void onBuyItem(price.item_id, amount)}>
                  Buy
                </button>
                <button onClick={() => void onSellItem(price.item_id, amount)}>
                  Sell
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}