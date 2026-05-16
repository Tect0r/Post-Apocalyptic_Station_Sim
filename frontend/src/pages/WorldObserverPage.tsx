import { useCallback, useEffect, useMemo, useState } from "react";
import {
  advanceWorldTicks,
  getWorld,
  resetWorld,
} from "../api/gameApi";
import type {
  NpcTrader,
  Route,
  Station,
  WorldLogEntry,
  WorldMovement,
  WorldResponse,
} from "../types/game";

type WorldObserverPageProps = {
  onLogout: () => void;
};

export function WorldObserverPage({ onLogout }: WorldObserverPageProps) {
  const [world, setWorld] = useState<WorldResponse | null>(null);
  const [selectedStationId, setSelectedStationId] = useState<string | null>(null);
  const [selectedTraderId, setSelectedTraderId] = useState<string | null>(null);
  const [showDebugLogs, setShowDebugLogs] = useState(false);
  const [autoRun, setAutoRun] = useState(false);
  const [autoRunDelayMs, setAutoRunDelayMs] = useState(1000);
  const [error, setError] = useState<string | null>(null);

  const stations = world?.stations ?? {};
  const routes = world?.routes ?? {};
  const events = world?.events ?? [];
  const movements = world?.movements ?? [];
  const npcTraders = world?.npc_traders ?? {};
  const worldLogs = world?.logs ?? [];

  const loadWorld = useCallback(async () => {
    try {
      setError(null);

      const response: any = await getWorld();
      console.log("WORLD RESPONSE", response);

      const worldResponse: WorldResponse = response.data ?? response;

      setWorld(worldResponse);

      if (!selectedStationId && worldResponse?.stations) {
        const firstStationId = Object.keys(worldResponse.stations)[0] ?? null;
        setSelectedStationId(firstStationId);
      }
    } catch (error) {
      console.error(error);
      setError(error instanceof Error ? error.message : "Failed to load world");
    }
  }, [selectedStationId]);

  const handleAdvanceTicks = useCallback(
    async (ticks: number) => {
      try {
        setError(null);
        await advanceWorldTicks(ticks);
        await loadWorld();
      } catch (error) {
        console.error(error);
        setError(error instanceof Error ? error.message : "Failed to advance ticks");
      }
    },
    [loadWorld],
  );

  async function handleResetWorld() {
    try {
      setError(null);
      await resetWorld();
      setAutoRun(false);
      setSelectedStationId(null);
      setSelectedTraderId(null);
      await loadWorld();
    } catch (error) {
      console.error(error);
      setError(error instanceof Error ? error.message : "Failed to reset world");
    }
  }

  useEffect(() => {
    void loadWorld();
  }, [loadWorld]);

  useEffect(() => {
    if (!autoRun) {
      return;
    }

    const intervalId = window.setInterval(() => {
      void handleAdvanceTicks(1);
    }, autoRunDelayMs);

    return () => {
      window.clearInterval(intervalId);
    };
  }, [autoRun, autoRunDelayMs, handleAdvanceTicks]);

  const selectedStation = useMemo(() => {
    if (!selectedStationId) {
      return null;
    }

    return stations[selectedStationId] ?? null;
  }, [stations, selectedStationId]);

  const selectedTrader = useMemo(() => {
    if (!selectedTraderId) {
      return null;
    }

    return npcTraders[selectedTraderId] ?? null;
  }, [npcTraders, selectedTraderId]);

  if (!world) {
    return (
      <main className="main-content">
        <h1>World Observer</h1>
        {error && <div className="error-banner">{error}</div>}
        <p className="muted">Loading world...</p>
      </main>
    );
  }

  const visibleLogs = showDebugLogs
    ? worldLogs
    : worldLogs.filter((log) => log.importance !== "debug");

  return (
    <div className="observer-page">
      <header className="dashboard-header">
        <div>
          <h1>World Observer</h1>
          <p>
            Tick {world.tick} · {autoRun ? "Auto running" : "Paused"}
          </p>
        </div>

        <div className="button-row">
          <button onClick={() => void handleAdvanceTicks(1)}>+1 Tick</button>
          <button onClick={() => void handleAdvanceTicks(10)}>+10</button>
          <button onClick={() => void handleAdvanceTicks(100)}>+100</button>

          <button onClick={() => setAutoRun((value) => !value)}>
            {autoRun ? "Pause Auto" : "Auto Run"}
          </button>

          <select
            value={autoRunDelayMs}
            onChange={(event) => setAutoRunDelayMs(Number(event.target.value))}
          >
            <option value={1000}>1 tick/sec</option>
            <option value={500}>2 ticks/sec</option>
            <option value={250}>4 ticks/sec</option>
          </select>

          <button onClick={() => void handleResetWorld()}>Reset</button>
          <button onClick={onLogout}>Logout</button>
        </div>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <section className="observer-grid">
        <StationListPanel
          stations={stations}
          selectedStationId={selectedStationId}
          onSelectStation={setSelectedStationId}
        />

        <StationDetailsPanel station={selectedStation} />

        <RouteListPanel routes={routes} stations={stations} />

        <TraderPanel
          traders={npcTraders}
          movements={movements}
          selectedTraderId={selectedTraderId}
          onSelectTrader={setSelectedTraderId}
        />

        <MovementPanel movements={movements} traders={npcTraders} />

        <SelectedTraderPanel trader={selectedTrader} />

        <EventPanel events={events} />

        <LogPanel
          logs={visibleLogs}
          showDebugLogs={showDebugLogs}
          onToggleDebug={setShowDebugLogs}
        />
      </section>
    </div>
  );
}

function StationListPanel(props: {
  stations: Record<string, Station>;
  selectedStationId: string | null;
  onSelectStation: (stationId: string) => void;
}) {
  const stations = Object.values(props.stations).sort(
    (a, b) => (a.ui?.map_y ?? 0) - (b.ui?.map_y ?? 0),
  );

  return (
    <section className="panel">
      <h2>Stations</h2>

      <div className="card-list">
        {stations.length === 0 && <p className="muted">No stations available.</p>}

        {stations.map((station) => (
          <button
            key={station.id}
            className={`station-card ${
              props.selectedStationId === station.id ? "selected" : ""
            }`}
            onClick={() => props.onSelectStation(station.id)}
          >
            <strong>{station.name}</strong>
            <span>{station.station_type}</span>
            <span>{station.inhabited ? `Pop ${station.population}` : "Abandoned"}</span>
            <span>
              Morale {station.stats?.morale ?? "-"} | Security{" "}
              {station.stats?.security ?? "-"}
            </span>
            <span>
              Danger {station.pressure?.danger ?? 0} | Supply{" "}
              {station.pressure?.supply_disruption ?? 0}
            </span>
          </button>
        ))}
      </div>
    </section>
  );
}

function StationDetailsPanel({ station }: { station: Station | null }) {
  if (!station) {
    return (
      <section className="panel">
        <h2>Station Details</h2>
        <p className="muted">No station selected.</p>
      </section>
    );
  }

  return (
    <section className="panel">
      <h2>{station.name}</h2>
      <p className="muted">
        {station.line ?? "unknown line"} · {station.station_type}
      </p>

      <h3>Stats</h3>
      <KeyValueGrid values={station.stats ?? {}} />

      <h3>Resources</h3>
      <KeyValueGrid values={station.resources ?? {}} />

      <h3>Pressure</h3>
      <KeyValueGrid values={station.pressure ?? {}} />

      <h3>Market Prices</h3>
      <KeyValueGrid values={station.market?.item_prices ?? {}} />
    </section>
  );
}

function RouteListPanel(props: {
  routes: Record<string, Route>;
  stations: Record<string, Station>;
}) {
  const routes = Object.values(props.routes).sort(
    (a, b) =>
      ((a.ui?.display_order as number | undefined) ?? 0) -
      ((b.ui?.display_order as number | undefined) ?? 0),
  );

  return (
    <section className="panel">
      <h2>Routes</h2>

      <div className="card-list">
        {routes.length === 0 && <p className="muted">No routes available.</p>}

        {routes.map((route) => (
          <div key={route.id} className="route-card">
            <strong>{route.display_name ?? route.id}</strong>
            <span>
              {props.stations[route.from_station_id]?.name ?? route.from_station_id}
              {" → "}
              {props.stations[route.to_station_id]?.name ?? route.to_station_id}
            </span>
            <span>
              Travel {route.travel_time_ticks} ticks · Danger {route.danger} ·
              Condition {route.condition}
            </span>
            <span>
              Traffic {route.traffic} · Type {route.route_type}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}

function TraderPanel(props: {
  traders: Record<string, NpcTrader>;
  movements: WorldMovement[];
  selectedTraderId: string | null;
  onSelectTrader: (traderId: string) => void;
}) {
  const traders = Object.values(props.traders);

  return (
    <section className="panel">
      <h2>NPC Traders</h2>

      <div className="card-list">
        {traders.length === 0 && <p className="muted">No NPC traders available.</p>}

        {traders.map((trader) => {
          const movement = props.movements.find(
            (item) => item.id === trader.active_movement_id,
          );

          return (
            <button
              key={trader.id}
              className={`station-card ${
                props.selectedTraderId === trader.id ? "selected" : ""
              }`}
              onClick={() => props.onSelectTrader(trader.id)}
            >
              <strong>{trader.name}</strong>
              <span>Status: {trader.status}</span>
              <span>At: {trader.current_station_id}</span>
              {trader.target_station_id && (
                <span>Target: {trader.target_station_id}</span>
              )}
              {movement && <span>Progress: {Math.round(movement.progress * 100)}%</span>}
            </button>
          );
        })}
      </div>
    </section>
  );
}

function SelectedTraderPanel({ trader }: { trader: NpcTrader | null }) {
  if (!trader) {
    return (
      <section className="panel">
        <h2>Selected Trader</h2>
        <p className="muted">No trader selected.</p>
      </section>
    );
  }

  const lastChoice = trader.data?.last_target_choice as
    | { selected_station_id?: string; evaluations?: unknown[] }
    | undefined;

  return (
    <section className="panel">
      <h2>{trader.name}</h2>
      <p className="muted">{trader.id}</p>

      <div className="list-grid">
        <div className="list-row">
          <span>Status</span>
          <strong>{trader.status}</strong>
        </div>
        <div className="list-row">
          <span>Current Station</span>
          <strong>{trader.current_station_id}</strong>
        </div>
        <div className="list-row">
          <span>Target</span>
          <strong>{trader.target_station_id ?? "-"}</strong>
        </div>
      </div>

      <h3>Inventory</h3>
      <KeyValueGrid values={trader.inventory ?? {}} />

      <h3>Last Target Choice</h3>
      {lastChoice ? (
        <pre className="debug-json">{JSON.stringify(lastChoice, null, 2)}</pre>
      ) : (
        <p className="muted">No target decision logged yet.</p>
      )}
    </section>
  );
}

function MovementPanel(props: {
  movements: WorldMovement[];
  traders: Record<string, NpcTrader>;
}) {
  const activeMovements = props.movements.filter(
    (movement) => movement.status === "active",
  );

  return (
    <section className="panel">
      <h2>Active Movements</h2>

      <div className="card-list">
        {activeMovements.length === 0 && <p className="muted">No active movements.</p>}

        {activeMovements.map((movement) => (
          <div key={movement.id} className="route-card">
            <strong>{props.traders[movement.actor_id]?.name ?? movement.actor_id}</strong>
            <span>
              {movement.from_station_id} → {movement.to_station_id}
            </span>
            <span>Progress: {Math.round((movement.progress ?? 0) * 100)}%</span>
            <span>Arrives at tick {movement.arrives_at_tick}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

function EventPanel({ events }: { events: WorldResponse["events"] }) {
  const safeEvents = events ?? [];

  return (
    <section className="panel">
      <h2>Events</h2>

      <div className="card-list">
        {safeEvents.length === 0 && <p className="muted">No recent events.</p>}

        {safeEvents
          .slice()
          .reverse()
          .map((event) => (
            <div key={event.id} className="event-row">
              <div>
                <strong>{event.event_type}</strong>
                <span>
                  {event.target_type}:{event.target_id}
                </span>
              </div>
              <span>{event.status}</span>
            </div>
          ))}
      </div>
    </section>
  );
}

function LogPanel(props: {
  logs: WorldLogEntry[];
  showDebugLogs: boolean;
  onToggleDebug: (value: boolean) => void;
}) {
  return (
    <section className="panel observer-wide">
      <div className="panel-header">
        <h2>World Feed</h2>

        <label className="inline-toggle">
          <input
            type="checkbox"
            checked={props.showDebugLogs}
            onChange={(event) => props.onToggleDebug(event.target.checked)}
          />
          Show debug logs
        </label>
      </div>

      <div className="log-list">
        {props.logs.length === 0 && <p className="muted">No logs available.</p>}

        {props.logs
          .slice()
          .reverse()
          .map((log) => (
            <div key={log.id} className="log-row">
              <span>Tick {log.tick}</span>
              <strong>{log.category}</strong>
              <p>{log.message}</p>
            </div>
          ))}
      </div>
    </section>
  );
}

function KeyValueGrid({ values }: { values: Record<string, number> }) {
  const entries = Object.entries(values ?? {});

  if (entries.length === 0) {
    return <p className="muted">No data.</p>;
  }

  return (
    <div className="stat-grid">
      {entries.map(([key, value]) => (
        <div key={key}>
          <span>{key}</span>
          <strong>{value}</strong>
        </div>
      ))}
    </div>
  );
}