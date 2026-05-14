import { useEffect, useMemo, useState } from "react";
import {
  advanceWorldTick,
  getPlayer,
  getWorld,
  startPlayerAction,
} from "../api/gameApi";
import { ActiveActionsCard } from "../components/actions/ActiveActionsCard";
import { StartActionPanel } from "../components/actions/StartActionPanel";
import { CrewStatusCard } from "../components/crew/CrewStatusCard";
import { InventoryCard } from "../components/crew/InventoryCard";
import { DashboardHeader } from "../components/dashboard/DashboardHeader";
import { EventList } from "../components/events/EventList";
import { AppLayout } from "../components/layout/AppLayout";
import { RouteList } from "../components/routes/RouteList";
import { StationDetail } from "../components/stations/StationDetail";
import { StationList } from "../components/stations/StationList";
import type { Player, WorldResponse } from "../types/game";

export function DashboardPage() {
  const [world, setWorld] = useState<WorldResponse | null>(null);
  const [player, setPlayer] = useState<Player | null>(null);
  const [selectedStationId, setSelectedStationId] = useState<string | null>("paveletskaya");
  const [error, setError] = useState<string | null>(null);

  async function loadData() {
    setError(null);

    try {
      const [worldResponse, playerResponse] = await Promise.all([
        getWorld(),
        getPlayer(),
      ]);

      setWorld(worldResponse);
      setPlayer(playerResponse);

      if (!selectedStationId && Object.keys(worldResponse.stations).length > 0) {
        setSelectedStationId(Object.keys(worldResponse.stations)[0]);
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : "Unknown error");
    }
  }

  async function handleAdvanceTick() {
    setError(null);

    try {
      await advanceWorldTick(1);
      await loadData();
    } catch (error) {
      setError(error instanceof Error ? error.message : "Unknown error");
    }
  }

  async function handleStartAction(actionType: string, targetId: string) {
    setError(null);

    try {
      await startPlayerAction({
        action_type: actionType,
        target_id: targetId,
      });

      await loadData();
    } catch (error) {
      setError(error instanceof Error ? error.message : "Unknown error");
    }
  }

  useEffect(() => {
    void loadData();
  }, []);

  const selectedStation = useMemo(() => {
    if (!world || !selectedStationId) {
      return null;
    }

    return world.stations[selectedStationId] ?? null;
  }, [world, selectedStationId]);

  if (!world || !player) {
    return (
      <AppLayout>
        <section className="panel">
          <h1>Loading...</h1>
          {error && <p className="error">{error}</p>}
        </section>
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      <DashboardHeader
        tick={world.tick}
        onRefresh={loadData}
        onAdvanceTick={handleAdvanceTick}
      />

      {error && <div className="error-banner">{error}</div>}

      <div className="dashboard-grid">
        <CrewStatusCard player={player} />
        <InventoryCard inventory={player.inventory} />
        <ActiveActionsCard activeActions={player.active_actions} />
        <StartActionPanel
          stations={world.stations}
          routes={world.routes}
          onStartAction={handleStartAction}
        />
        <StationList
          stations={world.stations}
          selectedStationId={selectedStationId}
          onSelectStation={setSelectedStationId}
        />
        <StationDetail station={selectedStation} />
        <RouteList routes={world.routes} />
        <EventList events={world.events} />
      </div>
    </AppLayout>
  );
}