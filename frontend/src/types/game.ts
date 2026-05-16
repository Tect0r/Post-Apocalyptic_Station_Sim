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

export type MarketPrice = {
  item_id: string;
  label: string;
  category: string;
  buy_price: number;
  sell_price: number;
  stock: number;
};

export type PvpImpact = {
  id: string;
  source_player_id: string;
  target_player_id: string | null;
  action_type: string;
  target_type: string;
  target_id: string;
  created_tick: number;
  effects: Record<string, unknown>;
  detected: boolean;
  reputation_cost: Record<string, number>;
};

export type MarketResponse = {
  station_id: string;
  prices: Record<string, MarketPrice>;
  stock: Record<string, number>;
  accessible?: boolean;
};

export type MarketTradeRequest = {
  item_id: string;
  amount: number;
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

export type Station = {
  id: string;
  name: string;
  complex_id?: string | null;
  line?: string | null;
  station_type: string;
  description_key?: string | null;
  inhabited: boolean;
  tags: string[];
  resources: Record<string, number>;
  population: number;
  stats: Record<string, number>;
  pressure: Record<string, number>;
  faction_influence: Record<string, number>;
  market: {
    market_type?: string;
    activity?: number;
    price_level?: number;
    item_prices?: Record<string, number>;
    stock?: Record<string, number>;
    [key: string]: unknown;
  };
  ui: {
    map_x?: number;
    map_y?: number;
    icon_type?: string;
    display_group?: string;
    [key: string]: unknown;
  };
};

export type Route = {
  id: string;
  display_name?: string | null;
  from_station_id: string;
  to_station_id: string;
  route_type: string;
  line?: string | null;
  bidirectional: boolean;
  distance: number;
  travel_time_ticks: number;
  danger: number;
  traffic: number;
  condition: number;
  control: Record<string, number>;
  pressure: Record<string, number>;
  tags: string[];
  ui: Record<string, unknown>;
};

export type WorldEvent = {
  id: string;
  event_type: string;
  target_type: string;
  target_id: string;
  started_at_tick: number;
  status: string;
  severity: number;
  causes: string[];
  data: Record<string, unknown>;
  duration_ticks: number;
  ends_at_tick: number | null;
  current_phase: string | null;
};

export type WorldMovement = {
  id: string;
  actor_type: string;
  actor_id: string;
  from_station_id: string;
  to_station_id: string;
  station_path: string[];
  route_path: string[];
  started_at_tick: number;
  arrives_at_tick: number;
  status: string;
  progress: number;
  data: Record<string, unknown>;
};

export type NpcTrader = {
  id: string;
  name: string;
  current_station_id: string;
  home_station_id: string;
  status: string;
  target_station_id: string | null;
  active_movement_id: string | null;
  rest_until_tick: number | null;
  inventory: Record<string, number>;
  data: Record<string, unknown>;
};

export type WorldLogEntry = {
  id: string;
  tick: number;
  category: string;
  message: string;
  target_type: string | null;
  target_id: string | null;
  importance: string;
  data: Record<string, unknown>;
};

export type WorldResponse = {
  tick: number;
  stations: Record<string, Station>;
  routes: Record<string, Route>;
  factions: Record<string, Faction>;
  events: WorldEvent[];
  movements: WorldMovement[];
  npc_traders: Record<string, NpcTrader>;
  logs: WorldLogEntry[];
  players?: Record<string, Player>;
};