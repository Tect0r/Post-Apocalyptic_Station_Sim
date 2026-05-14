import type { PublicPlayerSummary } from "../../types/game";

type PlayerListProps = {
  players: PublicPlayerSummary[];
};

export function PlayerList({ players }: PlayerListProps) {
  return (
    <section className="panel" id="players">
      <h2>Players</h2>

      {players.length === 0 ? (
        <p className="muted">No players found.</p>
      ) : (
        <div className="list-grid">
          {players.map((player) => (
            <div className="list-row" key={player.id}>
              <div>
                <strong>{player.name}</strong>
                <p className="muted">{player.id}</p>
              </div>
              <span>
                Actions: {player.active_action_count ?? player.active_actions?.length ?? 0}
              </span>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}