import type { PlayerAsset } from "../../types/game";

type AssetListProps = {
  assets: PlayerAsset[];
  onUpgradeAsset: (assetId: string) => Promise<void>;
  onRepairAsset: (assetId: string) => Promise<void>;
};

function formatLocation(asset: PlayerAsset): string {
  if (asset.station_id) {
    return `Station: ${asset.station_id}`;
  }

  if (asset.route_id) {
    return `Route: ${asset.route_id}`;
  }

  return "No location";
}

function formatEffects(effects: Record<string, number>): string {
  const entries = Object.entries(effects);

  if (entries.length === 0) {
    return "No effects";
  }

  return entries.map(([key, value]) => `${key}: ${value}`).join(", ");
}

export function AssetList({
  assets,
  onUpgradeAsset,
  onRepairAsset,
}: AssetListProps) {
  return (
    <section className="panel" id="assets">
      <h2>Assets</h2>

      {assets.length === 0 ? (
        <p className="muted">No assets yet.</p>
      ) : (
        <div className="card-list">
          {assets.map((asset) => (
            <div className="route-card" key={asset.id}>
              <strong>{asset.name}</strong>
              <span>Type: {asset.asset_type}</span>
              <span>{formatLocation(asset)}</span>
              <span>Level: {asset.level}</span>
              <span>Condition: {asset.condition}</span>
              <span>Status: {asset.status}</span>
              <span>Effects: {formatEffects(asset.effects)}</span>

              <div className="button-row">
                <button onClick={() => void onUpgradeAsset(asset.id)}>
                  Upgrade
                </button>
                <button onClick={() => void onRepairAsset(asset.id)}>
                  Repair
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}