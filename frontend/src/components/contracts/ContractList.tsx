import type { Contract } from "../../types/game";

type ContractListProps = {
  contracts: Contract[];
  onAcceptContract: (contractId: string) => Promise<void>;
};

function formatResourceMap(values: Record<string, number>): string {
  const entries = Object.entries(values);

  if (entries.length === 0) {
    return "None";
  }

  return entries.map(([key, value]) => `${key}: ${value}`).join(", ");
}

export function ContractList({ contracts, onAcceptContract }: ContractListProps) {
  return (
    <section className="panel" id="contracts">
      <h2>Contracts</h2>

      {contracts.length === 0 ? (
        <p className="muted">No contracts available.</p>
      ) : (
        <div className="card-list">
          {contracts.map((contract) => (
            <div className="route-card" key={contract.id}>
              <strong>{contract.title}</strong>
              <span>
                Issuer: {contract.issuer_type} / {contract.issuer_id}
              </span>
              <span>
                Target: {contract.target_type} / {contract.target_id}
              </span>
              <span>Action: {contract.action_type}</span>
              <span>Duration: {contract.duration_ticks}s</span>
              <span>Cost: {formatResourceMap(contract.cost)}</span>
              <span>Reward: {formatResourceMap(contract.reward)}</span>

              <button onClick={() => void onAcceptContract(contract.id)}>
                Accept Contract
              </button>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}