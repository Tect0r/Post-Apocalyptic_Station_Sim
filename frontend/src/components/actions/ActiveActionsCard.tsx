import type { ActiveAction } from "../../types/game";

type ActiveActionsCardProps = {
  activeActions: ActiveAction[];
  currentTick: number;
};

export function ActiveActionsCard({ activeActions, currentTick }: ActiveActionsCardProps) {
  return (
    <section className="panel">
      <h2>Active Actions</h2>

      {activeActions.length === 0 ? (
        <p className="muted">No active actions.</p>
      ) : (
        <div className="list-grid">
          {activeActions.map((action) => {
            const remainingTicks = Math.max(0, action.completes_at_tick - currentTick);

            return (
              <div className="action-row" key={action.id}>
                <div>
                  <strong>{action.action_type}</strong>
                  <p>
                    {action.target_type}: {action.target_id}
                  </p>
                  <p className="muted">
                    Started at tick {action.started_tick}, completes at tick{" "}
                    {action.completes_at_tick}
                  </p>
                </div>

                <span>{remainingTicks}s remaining</span>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}