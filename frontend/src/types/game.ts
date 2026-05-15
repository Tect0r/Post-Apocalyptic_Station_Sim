//TODO: Sortieren

export type ActiveAction = {
  id: string;
  action_type: string;
  assigned_crew_member_ids: string[];
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
  completed_actions: ActiveAction[];
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

export type CrewMember = {
  id: string;
  name: string;
  role: string;
  health: number;
  morale: number;
  fatigue: number;
  skills: Record<string, number>;
  traits: string[];
  status: string;
  current_location_id: string;
  assigned_action_id: string | null;
};

export type Route = {
  id: string;
  from_station_id: string;
  to_station_id: string;
  distance: number;
  danger_level: number;
  travel_time_ticks: number;
  status: string;
  control: Record<string, number>;
  modifiers: Record<string, unknown>;
};

export type PlayerAsset = {
  id: string;
  owner_player_id: string;
  name: string;
  asset_type: string;
  station_id: string | null;
  route_id: string | null;
  level: number;
  condition: number;
  status: string;
  effects: Record<string, number>;
  metadata: Record<string, unknown>;
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
  completed_actions: ActiveAction[];
  active_action_count?: number;
  asset_count?: number;
};

export type Crew = {
  members: number;
  crew_members: CrewMember[];
  health: number;
  morale: number;
  fatigue: number;
  specialization: string;
  current_location_id: string;
  destination_location_id: string | null;
  is_traveling: boolean;
};

export type Contract = {
  id: string;
  title: string;
  description_key: string;
  issuer_type: string;
  issuer_id: string;
  target_type: string;
  target_id: string;
  action_type: string;
  duration_ticks: number;
  cost: Record<string, number>;
  reward: Record<string, number>;
  effects: Record<string, unknown>;
  status: string;
  accepted_by_player_id: string | null;
  linked_action_id: string | null;
  created_tick: number;
  accepted_tick: number | null;
  completed_tick: number | null;
};
