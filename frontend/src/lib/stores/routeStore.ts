import { writable, derived } from 'svelte/store';
import type { RouteResponse, RouteOption, FilterState } from '$lib/types';

// Store for route search results
export const routeResponse = writable<RouteResponse | null>(null);

// Store for currently selected routes
export const selectedRoutes = writable<RouteOption[]>([]);

// Store for single selected route (for main view)
export const selectedRoute = writable<RouteOption | null>(null);

// Store for loading state
export const isLoading = writable(false);

// Store for error messages
export const error = writable<string | null>(null);

// Store for filter state
export const filters = writable<FilterState>({
	modes: {
		driving: true,
		transit: true,
		rideshare: false,
		micromobility: true
	},
	optimize: 'time',
	maxCost: null,
	maxWalkingDistance: 0.75,
	avoidTolls: false,
	accessible: false
});

// Derived store: filtered routes based on current filters
export const filteredRoutes = derived(
	[routeResponse, filters],
	([$routeResponse, $filters]) => {
		if (!$routeResponse) return [];

		return $routeResponse.routes.filter((route) => {
			// Filter by modes
			const hasRequiredModes = route.legs.every((leg) => {
				if (leg.mode === 'drive' && !$filters.modes.driving) return false;
				if (leg.mode === 'transit' && !$filters.modes.transit) return false;
				if (leg.mode === 'rideshare' && !$filters.modes.rideshare) return false;
				if (
					(leg.mode === 'bike' || leg.mode === 'scooter' || leg.mode === 'walk') &&
					!$filters.modes.micromobility
				)
					return false;
				return true;
			});

			// Filter by max cost
			if ($filters.maxCost !== null && route.total_cost > $filters.maxCost) {
				return false;
			}

			// Filter by max walking distance
			const totalWalkingDistance = route.legs
				.filter((leg) => leg.mode === 'walk')
				.reduce((sum, leg) => sum + leg.distance, 0);

			if (totalWalkingDistance > $filters.maxWalkingDistance) {
				return false;
			}

			// Filter by toll avoidance
			if ($filters.avoidTolls) {
				const hasTolls = route.legs.some((leg) => leg.details?.toll_cost && leg.details.toll_cost > 0);
				if (hasTolls) return false;
			}

			return hasRequiredModes;
		});
	}
);

// Derived store: sorted filtered routes based on optimization preference
export const sortedRoutes = derived([filteredRoutes, filters], ([$filteredRoutes, $filters]) => {
	const routes = [...$filteredRoutes];

	routes.sort((a, b) => {
		switch ($filters.optimize) {
			case 'time':
				return a.total_duration - b.total_duration;
			case 'cost':
				return a.total_cost - b.total_cost;
			case 'convenience':
				// Convenience: fewer legs is better, then by time
				const legDiff = a.legs.length - b.legs.length;
				return legDiff !== 0 ? legDiff : a.total_duration - b.total_duration;
			case 'environmental':
				// Environmental: more carbon savings is better
				return (b.carbon_savings || 0) - (a.carbon_savings || 0);
			default:
				return a.total_duration - b.total_duration;
		}
	});

	return routes;
});

// Helper functions
export function clearRoutes() {
	routeResponse.set(null);
	selectedRoutes.set([]);
	selectedRoute.set(null);
	error.set(null);
}

export function selectRoute(route: RouteOption | null) {
	selectedRoute.set(route);
}

export function toggleRouteSelection(route: RouteOption) {
	selectedRoutes.update(routes => {
		const index = routes.findIndex(r => r.id === route.id);
		if (index === -1) {
			return [...routes, route];
		} else {
			return routes.filter(r => r.id !== route.id);
		}
	});
}
