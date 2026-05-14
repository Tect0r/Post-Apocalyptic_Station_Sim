import { useState } from "react";
import type { Station, Route } from "../../types/game";

const ACTION_OPTIONS = [
  "scout_tunnel",
  "secure_route",
  "support_militia",
  "repair_water_filter",
  "hide_contraband",
  "run_market_stall",
  "rent_storage",
  "start_stalker_expedition",
  "treat_wounded",
  "maintain_faction_contact",
];

type StartActionPanelProps = {
  stations: Record<string, Station>;
  routes: Record<string, Route>;
  onStartAction: (actionType: string, targetId: string) => Promise<void>;
};

export function StartActionPanel({ stations, routes, onStartAction }: StartActionPanelProps) {
  const [actionType, setActionType] = useState(ACTION_OPTIONS[0]);
  const [targetId, setTargetId] = useState("paveletskaya");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const targets = {
    ...Object.fromEntries(Object.keys(stations).map((stationId) => [stationId, `Station: ${stationId}`])),
    ...Object.fromEntries(Object.keys(routes).map((routeId) => [routeId, `Route: ${routeId}`])),
  };

  async function handleSubmit() {
    setIsSubmitting(true);

    try {
      await onStartAction(actionType, targetId);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section className="panel" id="actions">
      <h2>Start Action</h2>

      <label>
        Action
        <select value={actionType} onChange={(event) => setActionType(event.target.value)}>
          {ACTION_OPTIONS.map((option) => (
            <option value={option} key={option}>
              {option}
            </option>
          ))}
        </select>
      </label>

      <label>
        Target
        <select value={targetId} onChange={(event) => setTargetId(event.target.value)}>
          {Object.entries(targets).map(([id, label]) => (
            <option value={id} key={id}>
              {label}
            </option>
          ))}
        </select>
      </label>

      <button onClick={handleSubmit} disabled={isSubmitting}>
        {isSubmitting ? "Starting..." : "Start Action"}
      </button>
    </section>
  );
}