import { useCallback, useEffect, useMemo, useState, } from "react";
import {
  getPlayers,
  getPlayer,
  getWorld,
  startPlayerAction,
  cancelPlayerAction,
  acceptContract,
  getContracts,
  startCrewMovement,
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
import type { Player, PublicPlayerSummary, WorldResponse, Contract, } from "../types/game";
import { logoutUser } from "../api/authApi";
import { PlayerList } from "../components/players/PlayerList";
import { CompletedActionsCard } from "../components/actions/CompletedActionsCard";
import { ContractList } from "../components/contracts/ContractList";
import { CrewMemberList } from "../components/crew/CrewMemberList";

type DashboardPageProps = {
  onLogout: () => void;
};

export function DashboardPage({ onLogout }: DashboardPageProps) {
  const [world, setWorld] = useState<WorldResponse | null>(null);
  const [player, setPlayer] = useState<Player | null>(null);
  const [selectedStationId, setSelectedStationId] = useState<string | null>("paveletskaya");
  const [error, setError] = useState<string | null>(null);
  const [players, setPlayers] = useState<PublicPlayerSummary[]>([]);
  const [contracts, setContracts] = useState<Contract[]>([]);

  const loadData = useCallback(async () => {
    setError(null);

    try {
      const [worldResponse, playerResponse, playersResponse, contractsResponse] = await Promise.all([
        getWorld(),
        getPlayer(),
        getPlayers(),
        getContracts(),
      ]);

    setWorld(worldResponse);
    setPlayer(playerResponse);
    setPlayers(playersResponse.players);
    setContracts(contractsResponse.contracts);

      setWorld(worldResponse);
      setPlayer(playerResponse);
      setPlayers(playersResponse.players);

      if (!selectedStationId && Object.keys(worldResponse.stations).length > 0) {
        setSelectedStationId(Object.keys(worldResponse.stations)[0]);
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : "Unknown error");
    }
  }, [selectedStationId]);

  async function handleCancelAction(actionId: string) {
    setError(null);

    try {
      await cancelPlayerAction(actionId);
      await loadData();
    } catch (error) {
      setError(error instanceof Error ? error.message : "Unknown error");
    }
  }

  async function handleStartMovement(routeId: string) {
    setError(null);

    try {
      await startCrewMovement(routeId);
      await loadData();
    } catch (error) {
      setError(error instanceof Error ? error.message : "Unknown error");
    }
  }

  async function handleAcceptContract(contractId: string) {
    setError(null);

    try {
      await acceptContract(contractId);
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

  function handleLogout() {
    logoutUser();
    onLogout();
    }


  useEffect(() => {
    void loadData();
  }, [loadData]);

  useEffect(() => {
  const intervalId = window.setInterval(() => {
    void loadData();
  }, 1000);

  return () => window.clearInterval(intervalId);
}, [loadData]);

  const selectedStation = useMemo(() => {
    if (!world || !selectedStationId) {
      return null;
    }

    return world.stations[selectedStationId] ?? null;
  }, [world, selectedStationId]);

  if (!world || !player) {
    return (
        <AppLayout onLogout={handleLogout}>
            <section className="panel">
            <h1>Loading...</h1>
            {error && <p className="error">{error}</p>}
            </section>
        </AppLayout>
    );
  }

    return (
    <AppLayout onLogout={handleLogout}>
        <DashboardHeader
        tick={world.tick}
        onRefresh={loadData}
        />

      {error && <div className="error-banner">{error}</div>}

      <div className="dashboard-grid">
        <CrewStatusCard player={player} />
        <CrewMemberList crewMembers={player.crew.crew_members} />
        <InventoryCard inventory={player.inventory} />
        <ActiveActionsCard
          activeActions={player.active_actions}
          currentTick={world.tick}
          onCancelAction={handleCancelAction}
        />
        <CompletedActionsCard completedActions={player.completed_actions} />
        <PlayerList players={players} />
        <ContractList
          contracts={contracts}
          onAcceptContract={handleAcceptContract}
        />
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
        <RouteList
          routes={world.routes}
          currentLocationId={player.crew.current_location_id}
          isTraveling={player.crew.is_traveling}
          onStartMovement={handleStartMovement}
        />
        <EventList events={world.events} />
      </div>
    </AppLayout>
  );
}