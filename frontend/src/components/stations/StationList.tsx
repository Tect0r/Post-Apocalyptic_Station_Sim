import type { Station } from "../../types/game";

type StationListProps = {
  stations: Record<string, Station>;
  selectedStationId: string | null;
  onSelectStation: (stationId: string) => void;
};

export function StationList({ stations, selectedStationId, onSelectStation }: StationListProps) {
  return (
    <section className="panel" id="stations">
      <h2>Stations</h2>

      <div className="card-list">
        {Object.values(stations).map((station) => (
          <button
            className={station.id === selectedStationId ? "station-card selected" : "station-card"}
            key={station.id}
            onClick={() => onSelectStation(station.id)}
          >
            <strong>{station.name}</strong>
            <span>{station.station_type}</span>
            <span>Security: {station.stats.security ?? "n/a"}</span>
          </button>
        ))}
      </div>
    </section>
  );
}