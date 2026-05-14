import { apiGet, apiPost } from "./apiClient";
import type {
  ActionResponse,
  Player,
  Route,
  StartActionRequest,
  Station,
  WorldEvent,
  WorldResponse,
  PublicPlayerSummary,
  Contract,
} from "../types/game";

export function getWorld(): Promise<WorldResponse> {
  return apiGet<WorldResponse>("/world");
}

export function getPlayer(): Promise<Player> {
  return apiGet<Player>("/player/me");
}

export function getStations(): Promise<{ stations: Record<string, Station> }> {
  return apiGet<{ stations: Record<string, Station> }>("/stations");
}

export function getStation(stationId: string): Promise<Station> {
  return apiGet<Station>(`/stations/${stationId}`);
}

export function getRoutes(): Promise<{ routes: Record<string, Route> }> {
  return apiGet<{ routes: Record<string, Route> }>("/routes");
}

export function getEvents(): Promise<{ events: WorldEvent[] }> {
  return apiGet<{ events: WorldEvent[] }>("/events");
}

export function startPlayerAction(request: StartActionRequest): Promise<ActionResponse> {
  return apiPost<ActionResponse, StartActionRequest>("/player/me/actions", request);
}

export function getPlayers(): Promise<{ players: PublicPlayerSummary[] }> {
  return apiGet<{ players: PublicPlayerSummary[] }>("/player");
}

export function cancelPlayerAction(actionId: string): Promise<ActionResponse> {
  return apiPost<ActionResponse>(`/player/me/actions/${actionId}/cancel`);
}

export function getContracts(): Promise<{ contracts: Contract[] }> {
  return apiGet<{ contracts: Contract[] }>("/contracts");
}

export function acceptContract(contractId: string): Promise<ActionResponse> {
  return apiPost<ActionResponse>(`/contracts/${contractId}/accept`);
}
