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
  PlayerAsset,
  MarketResponse,
  MarketTradeRequest,
  PvpImpact
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

export function startCrewMovement(routeId: string): Promise<ActionResponse> {
  return apiPost<ActionResponse, { route_id: string }>("/player/me/movement/start", {
    route_id: routeId,
  });
}

export function getPlayerAssets(): Promise<{ assets: PlayerAsset[] }> {
  return apiGet<{ assets: PlayerAsset[] }>("/player/me/assets");
}

export function upgradePlayerAsset(assetId: string): Promise<ActionResponse> {
  return apiPost<ActionResponse>(`/player/me/assets/${assetId}/upgrade`);
}

export function repairPlayerAsset(assetId: string): Promise<ActionResponse> {
  return apiPost<ActionResponse>(`/player/me/assets/${assetId}/repair`);
}

export function getCurrentMarket(): Promise<MarketResponse> {
  return apiGet<MarketResponse>("/market");
}

export function buyMarketItem(request: MarketTradeRequest): Promise<ActionResponse> {
  return apiPost<ActionResponse, MarketTradeRequest>("/market/buy", request);
}

export function sellMarketItem(request: MarketTradeRequest): Promise<ActionResponse> {
  return apiPost<ActionResponse, MarketTradeRequest>("/market/sell", request);
}

export function getPvpImpacts(): Promise<{ impacts: PvpImpact[] }> {
  return apiGet<{ impacts: PvpImpact[] }>("/pvp/impacts");
}

export function influenceStationPressure(request: {
  station_id: string;
  pressure_key: string;
  amount: number;
}): Promise<ActionResponse> {
  return apiPost<ActionResponse, typeof request>("/pvp/station-pressure", request);
}

export function advanceWorldTicks(ticks: number): Promise<{
  success: boolean;
  mode: string;
  tick: number;
  ticks_advanced: number;
}> {
  return apiPost(`/admin/tick?ticks=${ticks}`);
}

export function resetWorld(): Promise<{
  success: boolean;
  tick: number;
}> {
  return apiPost("/admin/reset");
}