import type { ActiveAction } from "../../types/game";

type ActiveActionsCardProps = {
  activeActions: ActiveAction[];
};

export function ActiveActionsCard({ activeActions }: ActiveActionsCardProps) {
  return (
    <section className="panel">
      <h2>Active Actions</h2>

      {activeActions.length === 0 ? (
        <p className="muted">No active actions.</p>
      ) : (
        <div className="list-grid">
          {activeActions.map((action) => (
            <div className="action-row" key={action.id}>
              <div>
                <strong>{action.action_type}</strong>
                <p>
                  {action.target_type}: {action.target_id}
                </p>
              </div>
              <span>
                completes at tick {action.completes_at_tick}
              </span>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}