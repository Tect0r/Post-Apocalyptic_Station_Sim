import type { Route } from "../../types/game";

type RouteListProps = {
  routes: Record<string, Route>;
};

export function RouteList({ routes }: RouteListProps) {
  return (
    <section className="panel" id="routes">
      <h2>Routes</h2>

      <div className="card-list">
        {Object.values(routes).map((route) => (
          <div className="route-card" key={route.id}>
            <strong>{route.id}</strong>
            <span>
              {route.from_station_id} → {route.to_station_id}
            </span>
            <span>Danger: {route.danger_level}</span>
            <span>Status: {route.status}</span>
          </div>
        ))}
      </div>
    </section>
  );
}