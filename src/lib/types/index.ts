// Transportation modes
export type TransitMode = 'BART' | 'Caltrain' | 'Muni' | 'VTA' | 'AC Transit';
export type RideshareMode = 'Uber' | 'Lyft' | 'Waymo';
export type MicromobilityMode = 'bike' | 'scooter' | 'walking';
export type RouteCombination = 'drive_and_ride' | 'rideshare_to_transit' | 'transit_only' | 'drive_only';

// Query preferences
export interface TravelModes {
	driving: boolean;
	parking: boolean;
	transit: TransitMode[];
	rideshare: RideshareMode[];
	micromobility: MicromobilityMode[];
	combinations: RouteCombination[];
}

export interface TravelConstraints {
	max_walking_distance: number; // in miles
	max_cost: number | null;
	avoid_tolls: boolean;
	accessible: boolean;
}

export type OptimizationPreference = 'time' | 'cost' | 'convenience' | 'environmental';

export interface TravelPreferences {
	modes: TravelModes;
	optimize_for: OptimizationPreference;
	constraints: TravelConstraints;
}

// Parsed query from LLM
export interface ParsedQuery {
	origin: string;
	destination: string;
	arrival_time: string; // ISO timestamp
	preferences: TravelPreferences;
}

// Route leg types
export type LegMode = 'drive' | 'park' | 'walk' | 'transit' | 'rideshare' | 'bike' | 'scooter';

export interface Coordinates {
	lat: number;
	lng: number;
}

export interface RouteLeg {
	mode: LegMode;
	from: string;
	to: string;
	from_coords: Coordinates;
	to_coords: Coordinates;
	duration: number; // in minutes
	distance: number; // in miles
	cost: number; // in dollars
	details?: {
		// For transit
		line?: string;
		departure_time?: string;
		arrival_time?: string;
		stops?: number;
		// For parking
		parking_lot?: string;
		parking_availability?: number; // percentage
		parking_rate?: string;
		// For driving
		traffic_level?: 'light' | 'moderate' | 'heavy';
		toll_cost?: number;
		// For rideshare
		provider?: RideshareMode;
		wait_time?: number;
	};
	polyline?: string; // encoded polyline for map
}

// Complete route option
export interface RouteOption {
	id: string;
	summary: string;
	total_duration: number; // in minutes
	total_cost: number; // in dollars
	departure_time: string; // ISO timestamp
	arrival_time: string; // ISO timestamp
	legs: RouteLeg[];
	confidence: number; // 0-100
	carbon_savings?: number; // in kg CO2
	time_savings?: number; // minutes saved vs driving
}

// Route response from backend
export interface RouteResponse {
	query: ParsedQuery;
	routes: RouteOption[];
	generated_at: string; // ISO timestamp
}

// UI state
export interface FilterState {
	modes: {
		driving: boolean;
		transit: boolean;
		rideshare: boolean;
		micromobility: boolean;
	};
	optimize: OptimizationPreference;
	maxCost: number | null;
	maxWalkingDistance: number;
	avoidTolls: boolean;
	accessible: boolean;
}

// API errors
export interface ApiError {
	error: string;
	message: string;
	details?: any;
}
