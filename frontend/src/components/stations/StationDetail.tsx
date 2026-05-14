import type { Station } from "../../types/game";

type StationDetailProps = {
  station: Station | null;
};

export function StationDetail({ station }: StationDetailProps) {
  if (!station) {
    return (
      <section className="panel">
        <h2>Station Detail</h2>
        <p className="muted">Select a station.</p>
      </section>
    );
  }

  return (
    <section className="panel">
      <h2>{station.name}</h2>
      <p className="muted">{station.description_key}</p>

      <h3>Stats</h3>
      <div className="list-grid">
        {Object.entries(station.stats).map(([key, value]) => (
          <div className="list-row" key={key}>
            <span>{key}</span>
            <strong>{value}</strong>
          </div>
        ))}
      </div>

      <h3>Pressure</h3>
      <div className="list-grid">
        {Object.entries(station.pressure).map(([key, value]) => (
          <div className="list-row" key={key}>
            <span>{key}</span>
            <strong>{value}</strong>
          </div>
        ))}
      </div>

      <h3>Faction Influence</h3>
      <div className="list-grid">
        {Object.entries(station.faction_influence).map(([key, value]) => (
          <div className="list-row" key={key}>
            <span>{key}</span>
            <strong>{value}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}