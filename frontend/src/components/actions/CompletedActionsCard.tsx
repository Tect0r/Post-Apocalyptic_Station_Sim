import type { ActiveAction } from "../../types/game";

type CompletedActionsCardProps = {
  completedActions: ActiveAction[];
};

export function CompletedActionsCard({ completedActions }: CompletedActionsCardProps) {
  return (
    <section className="panel">
      <h2>Completed Actions</h2>

      {completedActions.length === 0 ? (
        <p className="muted">No completed actions yet.</p>
      ) : (
        <div className="list-grid">
          {completedActions.slice(-10).reverse().map((action) => (
            <div className="action-row" key={action.id}>
              <div>
                <strong>{action.action_type}</strong>
                <p>
                  {action.target_type}: {action.target_id}
                </p>
              </div>
              <span>{action.status}</span>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}