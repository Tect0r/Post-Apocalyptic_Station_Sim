import type { Player } from "../../types/game";

type CrewStatusCardProps = {
  player: Player;
};

export function CrewStatusCard({ player }: CrewStatusCardProps) {
  return (
    <section className="panel" id="crew">
      <h2>Crew</h2>

      <div className="stat-grid">
        <div>
          <span>Members</span>
          <strong>{player.crew.members}</strong>
        </div>
        <div>
          <span>Health</span>
          <strong>{player.crew.health}</strong>
        </div>
        <div>
          <span>Morale</span>
          <strong>{player.crew.morale}</strong>
        </div>
        <div>
          <span>Fatigue</span>
          <strong>{player.crew.fatigue}</strong>
        </div>
        <div>
          <span>Specialization</span>
          <strong>{player.crew.specialization}</strong>
        </div>
      </div>
    </section>
  );
}