export type Crew = {
  members: number;
  health: number;
  morale: number;
  fatigue: number;
  specialization: string;
};

export type PlayerAsset = {
  id: string;
  name: string;
  asset_type: string;
  location_id: string | null;
  condition: number;
};

export type ActiveAction = {
  id: string;
  action_type: string;
  target_type: string;
  target_id: string;
  started_tick: number;
  duration_ticks: number;
  completes_at_tick: number;
  status: string;
};

export type Player = {
  id: string;
  name: string;
  crew: Crew;
  inventory: Record<string, number>;
  reputation: Record<string, number>;
  assets: PlayerAsset[];
  active_actions: ActiveAction[];
};

export type Station = {
  id: string;
  name: string;
  station_type: string;
  description_key: string;
  resources: Record<string, number>;
  population: Record<string, number>;
  stats: Record<string, number>;
  pressure: Record<string, number>;
  faction_influence: Record<string, number>;
};

export type Route = {
  id: string;
  from_station_id: string;
  to_station_id: string;
  distance: number;
  danger_level: number;
  status: string;
  modifiers: Record<string, unknown>;
};

export type Faction = {
  id: string;
  name: string;
  resources: Record<string, number>;
  relations: Record<string, number>;
  controlled_stations: string[];
};

export type WorldEvent = {
  id: string;
  tick: number;
  station_id: string | null;
  event_type: string;
  severity: number;
  description_key: string;
};

export type WorldResponse = {
  tick: number;
  stations: Record<string, Station>;
  routes: Record<string, Route>;
  factions: Record<string, Faction>;
  events: WorldEvent[];
  players?: Record<string, PublicPlayerSummary>;
};

export type StartActionRequest = {
  action_type: string;
  target_id: string;
};

export type ActionResponse = {
  success: boolean;
  message: string;
  data: Record<string, unknown> | null;
};

export type PublicPlayerSummary = {
  id: string;
  name: string;
  crew: Crew;
  inventory?: Record<string, number>;
  reputation?: Record<string, number>;
  assets?: PlayerAsset[];
  active_actions?: ActiveAction[];
  active_action_count?: number;
  asset_count?: number;
};
