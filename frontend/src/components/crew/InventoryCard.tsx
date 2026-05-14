type InventoryCardProps = {
  inventory: Record<string, number>;
};

export function InventoryCard({ inventory }: InventoryCardProps) {
  return (
    <section className="panel">
      <h2>Inventory</h2>

      <div className="list-grid">
        {Object.entries(inventory).map(([itemId, amount]) => (
          <div className="list-row" key={itemId}>
            <span>{itemId}</span>
            <strong>{amount}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}