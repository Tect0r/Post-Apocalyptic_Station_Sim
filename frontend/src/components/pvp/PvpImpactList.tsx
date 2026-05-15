import type { PvpImpact } from "../../types/game";

type PvpImpactListProps = {
  impacts: PvpImpact[];
};

export function PvpImpactList({ impacts }: PvpImpactListProps) {
  return (
    <section className="panel" id="pvp">
      <h2>Indirect PvP</h2>

      {impacts.length === 0 ? (
        <p className="muted">No PvP impacts yet.</p>
      ) : (
        <div className="list-grid">
          {impacts.slice(-10).reverse().map((impact) => (
            <div className="event-row" key={impact.id}>
              <div>
                <strong>{impact.action_type}</strong>
                <p>
                  {impact.target_type}: {impact.target_id}
                </p>
                <p className="muted">
                  Source: {impact.source_player_id}
                </p>
              </div>
              <span>{impact.detected ? "Detected" : "Hidden"}</span>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}