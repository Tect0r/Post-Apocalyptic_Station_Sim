import type { Route } from "../../types/game";

type RouteListProps = {
  routes: Record<string, Route>;
  currentLocationId: string;
  isTraveling: boolean;
  onStartMovement: (routeId: string) => Promise<void>;
};

export function RouteList({
  routes,
  currentLocationId,
  isTraveling,
  onStartMovement,
}: RouteListProps) {
  return (
    <section className="panel" id="routes">
      <h2>Routes</h2>

      <div className="card-list">
        {Object.values(routes).map((route) => {
          const isConnected =
            route.from_station_id === currentLocationId ||
            route.to_station_id === currentLocationId;

          const canTravel =
            isConnected &&
            !isTraveling &&
            route.status === "open";

          return (
            <div className="route-card" key={route.id}>
              <strong>{route.id}</strong>

              <span>
                {route.from_station_id} → {route.to_station_id}
              </span>

              <span>Danger: {route.danger}</span>
              <span>Status: {route.status}</span>
              <span>Travel Time: {route.travel_time_ticks}s</span>

              {!isConnected && (
                <span className="muted">
                  Not connected to current crew location.
                </span>
              )}

              {isTraveling && (
                <span className="muted">
                  Crew is already traveling.
                </span>
              )}

              <button
                disabled={!canTravel}
                onClick={() => void onStartMovement(route.id)}
              >
                Travel
              </button>
            </div>
          );
        })}
      </div>
    </section>
  );
}