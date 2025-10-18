import type { RouteResponse, RouteOption } from '$lib/types';

// Helper function to generate random route based on query
export function generateMockRoutes(query: string): RouteResponse {
	// Parse query to determine origin/destination
	const lowerQuery = query.toLowerCase();

	// Determine which mock to use based on query
	if (lowerQuery.includes('oracle park') || lowerQuery.includes('palo alto')) {
		return mockPaloAltoRoute;
	} else if (lowerQuery.includes('milpitas') || lowerQuery.includes('moscone')) {
		return mockMilpitasRoute;
	} else if (lowerQuery.includes('berkeley') || lowerQuery.includes('downtown')) {
		return mockBerkeleyRoute;
	} else {
		// Default: San Jose to SF
		return mockRouteResponse;
	}
}

export const mockRouteResponse: RouteResponse = {
	query: {
		origin: 'San Jose, CA',
		destination: 'Salesforce Tower, San Francisco, CA',
		arrival_time: '2025-10-18T10:00:00-07:00',
		preferences: {
			modes: {
				driving: true,
				parking: true,
				transit: ['Caltrain'],
				rideshare: [],
				micromobility: [],
				combinations: ['drive_and_ride']
			},
			optimize_for: 'time',
			constraints: {
				max_walking_distance: 0.5,
				max_cost: null,
				avoid_tolls: false,
				accessible: false
			}
		}
	},
	routes: [
		{
			id: 'route-1',
			summary: 'Drive to Millbrae, Caltrain to SF',
			total_duration: 75,
			total_cost: 18.5,
			departure_time: '2025-10-18T08:45:00-07:00',
			arrival_time: '2025-10-18T10:00:00-07:00',
			confidence: 92,
			carbon_savings: 8.5,
			time_savings: 15,
			legs: [
				{
					mode: 'drive',
					from: 'San Jose, CA',
					to: 'Millbrae Station Parking',
					from_coords: { lat: 37.3382, lng: -121.8863 },
					to_coords: { lat: 37.5996, lng: -122.3869 },
					duration: 35,
					distance: 28.5,
					cost: 0,
					details: {
						traffic_level: 'moderate',
						toll_cost: 0
					}
				},
				{
					mode: 'park',
					from: 'Millbrae Station Parking',
					to: 'Millbrae Station Platform',
					from_coords: { lat: 37.5996, lng: -122.3869 },
					to_coords: { lat: 37.5996, lng: -122.3869 },
					duration: 5,
					distance: 0.1,
					cost: 5.5,
					details: {
						parking_lot: 'Millbrae Station Lot A',
						parking_availability: 65,
						parking_rate: '$5.50/day'
					}
				},
				{
					mode: 'transit',
					from: 'Millbrae Station',
					to: 'San Francisco 4th & King',
					from_coords: { lat: 37.5996, lng: -122.3869 },
					to_coords: { lat: 37.7766, lng: -122.3943 },
					duration: 28,
					distance: 15.2,
					cost: 8.75,
					details: {
						line: 'Caltrain Local 232',
						departure_time: '2025-10-18T09:20:00-07:00',
						arrival_time: '2025-10-18T09:48:00-07:00',
						stops: 5
					}
				},
				{
					mode: 'walk',
					from: 'San Francisco 4th & King',
					to: 'Salesforce Tower',
					from_coords: { lat: 37.7766, lng: -122.3943 },
					to_coords: { lat: 37.7897, lng: -122.3972 },
					duration: 12,
					distance: 0.6,
					cost: 0
				}
			]
		},
		{
			id: 'route-2',
			summary: 'Drive to Mountain View, Caltrain Express to SF',
			total_duration: 82,
			total_cost: 14.25,
			departure_time: '2025-10-18T08:38:00-07:00',
			arrival_time: '2025-10-18T10:00:00-07:00',
			confidence: 88,
			carbon_savings: 7.2,
			time_savings: 8,
			legs: [
				{
					mode: 'drive',
					from: 'San Jose, CA',
					to: 'Mountain View Station Parking',
					from_coords: { lat: 37.3382, lng: -121.8863 },
					to_coords: { lat: 37.3945, lng: -122.0762 },
					duration: 22,
					distance: 15.8,
					cost: 0,
					details: {
						traffic_level: 'light',
						toll_cost: 0
					}
				},
				{
					mode: 'park',
					from: 'Mountain View Station Parking',
					to: 'Mountain View Station Platform',
					from_coords: { lat: 37.3945, lng: -122.0762 },
					to_coords: { lat: 37.3945, lng: -122.0762 },
					duration: 5,
					distance: 0.1,
					cost: 3.0,
					details: {
						parking_lot: 'Mountain View Station Lot B',
						parking_availability: 45,
						parking_rate: '$3.00/day'
					}
				},
				{
					mode: 'transit',
					from: 'Mountain View Station',
					to: 'San Francisco 4th & King',
					from_coords: { lat: 37.3945, lng: -122.0762 },
					to_coords: { lat: 37.7766, lng: -122.3943 },
					duration: 43,
					distance: 31.5,
					cost: 11.25,
					details: {
						line: 'Caltrain Express 423',
						departure_time: '2025-10-18T09:05:00-07:00',
						arrival_time: '2025-10-18T09:48:00-07:00',
						stops: 3
					}
				},
				{
					mode: 'walk',
					from: 'San Francisco 4th & King',
					to: 'Salesforce Tower',
					from_coords: { lat: 37.7766, lng: -122.3943 },
					to_coords: { lat: 37.7897, lng: -122.3972 },
					duration: 12,
					distance: 0.6,
					cost: 0
				}
			]
		},
		{
			id: 'route-3',
			summary: 'Drive to Daly City BART, BART to Downtown SF',
			total_duration: 85,
			total_cost: 14.2,
			departure_time: '2025-10-18T08:35:00-07:00',
			arrival_time: '2025-10-18T10:00:00-07:00',
			confidence: 85,
			carbon_savings: 9.1,
			time_savings: 5,
			legs: [
				{
					mode: 'drive',
					from: 'San Jose, CA',
					to: 'Daly City BART Parking',
					from_coords: { lat: 37.3382, lng: -121.8863 },
					to_coords: { lat: 37.7059, lng: -122.4696 },
					duration: 48,
					distance: 42.3,
					cost: 0,
					details: {
						traffic_level: 'moderate',
						toll_cost: 0
					}
				},
				{
					mode: 'park',
					from: 'Daly City BART Parking',
					to: 'Daly City BART Platform',
					from_coords: { lat: 37.7059, lng: -122.4696 },
					to_coords: { lat: 37.7059, lng: -122.4696 },
					duration: 5,
					distance: 0.05,
					cost: 3.0,
					details: {
						parking_lot: 'Daly City BART Garage',
						parking_availability: 80,
						parking_rate: '$3.00/day'
					}
				},
				{
					mode: 'transit',
					from: 'Daly City BART',
					to: 'Montgomery St BART',
					from_coords: { lat: 37.7059, lng: -122.4696 },
					to_coords: { lat: 37.7894, lng: -122.4017 },
					duration: 22,
					distance: 7.8,
					cost: 4.2,
					details: {
						line: 'BART Red Line',
						departure_time: '2025-10-18T09:28:00-07:00',
						arrival_time: '2025-10-18T09:50:00-07:00',
						stops: 6
					}
				},
				{
					mode: 'walk',
					from: 'Montgomery St BART',
					to: 'Salesforce Tower',
					from_coords: { lat: 37.7894, lng: -122.4017 },
					to_coords: { lat: 37.7897, lng: -122.3972 },
					duration: 10,
					distance: 0.3,
					cost: 0
				}
			]
		}
	],
	generated_at: '2025-10-18T08:00:00-07:00'
};

// Additional mock routes for different queries
export const mockPaloAltoRoute: RouteResponse = {
	query: {
		origin: 'Palo Alto, CA',
		destination: 'Oracle Park, San Francisco, CA',
		arrival_time: '2025-10-18T19:00:00-07:00',
		preferences: {
			modes: {
				driving: false,
				parking: false,
				transit: ['Caltrain', 'Muni'],
				rideshare: [],
				micromobility: ['walking'],
				combinations: ['transit_only']
			},
			optimize_for: 'cost',
			constraints: {
				max_walking_distance: 0.75,
				max_cost: null,
				avoid_tolls: false,
				accessible: false
			}
		}
	},
	routes: [
		{
			id: 'route-pa-1',
			summary: 'Caltrain to 4th & King, walk to Oracle Park',
			total_duration: 68,
			total_cost: 8.75,
			departure_time: '2025-10-18T17:52:00-07:00',
			arrival_time: '2025-10-18T19:00:00-07:00',
			confidence: 95,
			carbon_savings: 12.4,
			legs: [
				{
					mode: 'walk',
					from: 'Palo Alto, CA',
					to: 'Palo Alto Caltrain Station',
					from_coords: { lat: 37.4436, lng: -122.1605 },
					to_coords: { lat: 37.4431, lng: -122.1643 },
					duration: 8,
					distance: 0.3,
					cost: 0
				},
				{
					mode: 'transit',
					from: 'Palo Alto Station',
					to: 'San Francisco 4th & King',
					from_coords: { lat: 37.4431, lng: -122.1643 },
					to_coords: { lat: 37.7766, lng: -122.3943 },
					duration: 48,
					distance: 28.4,
					cost: 8.75,
					details: {
						line: 'Caltrain Local 156',
						departure_time: '2025-10-18T18:00:00-07:00',
						arrival_time: '2025-10-18T18:48:00-07:00',
						stops: 8
					}
				},
				{
					mode: 'walk',
					from: 'San Francisco 4th & King',
					to: 'Oracle Park',
					from_coords: { lat: 37.7766, lng: -122.3943 },
					to_coords: { lat: 37.7786, lng: -122.3893 },
					duration: 12,
					distance: 0.4,
					cost: 0
				}
			]
		}
	],
	generated_at: '2025-10-18T17:00:00-07:00'
};

// Milpitas to Moscone Center - Mix of BART and rideshare
export const mockMilpitasRoute: RouteResponse = {
	query: {
		origin: 'Milpitas, CA',
		destination: 'Moscone Center, San Francisco, CA',
		arrival_time: '2025-10-18T11:00:00-07:00',
		preferences: {
			modes: {
				driving: true,
				parking: true,
				transit: ['BART'],
				rideshare: ['Uber'],
				micromobility: [],
				combinations: ['drive_and_ride', 'rideshare_to_transit']
			},
			optimize_for: 'time',
			constraints: {
				max_walking_distance: 0.5,
				max_cost: 25.0,
				avoid_tolls: false,
				accessible: false
			}
		}
	},
	routes: [
		{
			id: 'route-mil-1',
			summary: 'Drive to Warm Springs BART, BART to Powell',
			total_duration: 62,
			total_cost: 11.75,
			departure_time: '2025-10-18T09:58:00-07:00',
			arrival_time: '2025-10-18T11:00:00-07:00',
			confidence: 91,
			carbon_savings: 15.2,
			time_savings: 18,
			legs: [
				{
					mode: 'drive',
					from: 'Milpitas, CA',
					to: 'Warm Springs BART Parking',
					from_coords: { lat: 37.4323, lng: -121.9018 },
					to_coords: { lat: 37.5025, lng: -121.9396 },
					duration: 12,
					distance: 8.2,
					cost: 0,
					details: {
						traffic_level: 'light',
						toll_cost: 0
					}
				},
				{
					mode: 'park',
					from: 'Warm Springs BART Parking',
					to: 'Warm Springs BART Platform',
					from_coords: { lat: 37.5025, lng: -121.9396 },
					to_coords: { lat: 37.5025, lng: -121.9396 },
					duration: 5,
					distance: 0.05,
					cost: 3.0,
					details: {
						parking_lot: 'Warm Springs BART Garage',
						parking_availability: 75,
						parking_rate: '$3.00/day'
					}
				},
				{
					mode: 'transit',
					from: 'Warm Springs BART',
					to: 'Powell St BART',
					from_coords: { lat: 37.5025, lng: -121.9396 },
					to_coords: { lat: 37.7844, lng: -122.4079 },
					duration: 38,
					distance: 42.1,
					cost: 5.95,
					details: {
						line: 'BART Orange Line',
						departure_time: '2025-10-18T10:15:00-07:00',
						arrival_time: '2025-10-18T10:53:00-07:00',
						stops: 12
					}
				},
				{
					mode: 'walk',
					from: 'Powell St BART',
					to: 'Moscone Center',
					from_coords: { lat: 37.7844, lng: -122.4079 },
					to_coords: { lat: 37.7840, lng: -122.4008 },
					duration: 7,
					distance: 0.3,
					cost: 0
				}
			]
		},
		{
			id: 'route-mil-2',
			summary: 'Uber to Fremont BART, BART to Moscone',
			total_duration: 58,
			total_cost: 22.45,
			departure_time: '2025-10-18T10:02:00-07:00',
			arrival_time: '2025-10-18T11:00:00-07:00',
			confidence: 88,
			carbon_savings: 11.8,
			time_savings: 22,
			legs: [
				{
					mode: 'rideshare',
					from: 'Milpitas, CA',
					to: 'Fremont BART Station',
					from_coords: { lat: 37.4323, lng: -121.9018 },
					to_coords: { lat: 37.5571, lng: -121.9761 },
					duration: 15,
					distance: 9.5,
					cost: 16.50,
					details: {
						provider: 'Uber',
						wait_time: 3
					}
				},
				{
					mode: 'transit',
					from: 'Fremont BART',
					to: 'Powell St BART',
					from_coords: { lat: 37.5571, lng: -121.9761 },
					to_coords: { lat: 37.7844, lng: -122.4079 },
					duration: 36,
					distance: 38.2,
					cost: 5.95,
					details: {
						line: 'BART Orange Line',
						departure_time: '2025-10-18T10:17:00-07:00',
						arrival_time: '2025-10-18T10:53:00-07:00',
						stops: 11
					}
				},
				{
					mode: 'walk',
					from: 'Powell St BART',
					to: 'Moscone Center',
					from_coords: { lat: 37.7844, lng: -122.4079 },
					to_coords: { lat: 37.7840, lng: -122.4008 },
					duration: 7,
					distance: 0.3,
					cost: 0
				}
			]
		},
		{
			id: 'route-mil-3',
			summary: 'Drive to Milpitas BART, BART + walk',
			total_duration: 68,
			total_cost: 9.95,
			departure_time: '2025-10-18T09:52:00-07:00',
			arrival_time: '2025-10-18T11:00:00-07:00',
			confidence: 94,
			carbon_savings: 16.5,
			time_savings: 12,
			legs: [
				{
					mode: 'drive',
					from: 'Milpitas, CA',
					to: 'Milpitas BART Parking',
					from_coords: { lat: 37.4323, lng: -121.9018 },
					to_coords: { lat: 37.4094, lng: -121.8909 },
					duration: 8,
					distance: 3.1,
					cost: 0,
					details: {
						traffic_level: 'light',
						toll_cost: 0
					}
				},
				{
					mode: 'park',
					from: 'Milpitas BART Parking',
					to: 'Milpitas BART Platform',
					from_coords: { lat: 37.4094, lng: -121.8909 },
					to_coords: { lat: 37.4094, lng: -121.8909 },
					duration: 5,
					distance: 0.05,
					cost: 4.0,
					details: {
						parking_lot: 'Milpitas BART Lot',
						parking_availability: 60,
						parking_rate: '$4.00/day'
					}
				},
				{
					mode: 'transit',
					from: 'Milpitas BART',
					to: 'Powell St BART',
					from_coords: { lat: 37.4094, lng: -121.8909 },
					to_coords: { lat: 37.7844, lng: -122.4079 },
					duration: 48,
					distance: 45.8,
					cost: 5.95,
					details: {
						line: 'BART Orange Line',
						departure_time: '2025-10-18T10:05:00-07:00',
						arrival_time: '2025-10-18T10:53:00-07:00',
						stops: 14
					}
				},
				{
					mode: 'walk',
					from: 'Powell St BART',
					to: 'Moscone Center',
					from_coords: { lat: 37.7844, lng: -122.4079 },
					to_coords: { lat: 37.7840, lng: -122.4008 },
					duration: 7,
					distance: 0.3,
					cost: 0
				}
			]
		}
	],
	generated_at: '2025-10-18T09:00:00-07:00'
};

// Berkeley to Downtown Oakland - Short trip with multiple options
export const mockBerkeleyRoute: RouteResponse = {
	query: {
		origin: 'Berkeley, CA',
		destination: 'Downtown Oakland, CA',
		arrival_time: '2025-10-18T14:00:00-07:00',
		preferences: {
			modes: {
				driving: true,
				parking: true,
				transit: ['BART', 'AC Transit'],
				rideshare: ['Lyft'],
				micromobility: ['bike', 'scooter'],
				combinations: ['transit_only', 'bike', 'rideshare_to_transit']
			},
			optimize_for: 'convenience',
			constraints: {
				max_walking_distance: 1.0,
				max_cost: null,
				avoid_tolls: false,
				accessible: false
			}
		}
	},
	routes: [
		{
			id: 'route-berk-1',
			summary: 'BART from Downtown Berkeley to 12th St',
			total_duration: 18,
			total_cost: 2.50,
			departure_time: '2025-10-18T13:42:00-07:00',
			arrival_time: '2025-10-18T14:00:00-07:00',
			confidence: 97,
			carbon_savings: 2.1,
			time_savings: 12,
			legs: [
				{
					mode: 'walk',
					from: 'Berkeley, CA',
					to: 'Downtown Berkeley BART',
					from_coords: { lat: 37.8715, lng: -122.2730 },
					to_coords: { lat: 37.8700, lng: -122.2681 },
					duration: 6,
					distance: 0.3,
					cost: 0
				},
				{
					mode: 'transit',
					from: 'Downtown Berkeley BART',
					to: '12th St Oakland BART',
					from_coords: { lat: 37.8700, lng: -122.2681 },
					to_coords: { lat: 37.8036, lng: -122.2718 },
					duration: 8,
					distance: 5.2,
					cost: 2.50,
					details: {
						line: 'BART Red Line',
						departure_time: '2025-10-18T13:48:00-07:00',
						arrival_time: '2025-10-18T13:56:00-07:00',
						stops: 2
					}
				},
				{
					mode: 'walk',
					from: '12th St Oakland BART',
					to: 'Downtown Oakland',
					from_coords: { lat: 37.8036, lng: -122.2718 },
					to_coords: { lat: 37.8044, lng: -122.2712 },
					duration: 4,
					distance: 0.15,
					cost: 0
				}
			]
		},
		{
			id: 'route-berk-2',
			summary: 'AC Transit Bus 51 direct',
			total_duration: 32,
			total_cost: 2.25,
			departure_time: '2025-10-18T13:28:00-07:00',
			arrival_time: '2025-10-18T14:00:00-07:00',
			confidence: 89,
			carbon_savings: 1.8,
			legs: [
				{
					mode: 'walk',
					from: 'Berkeley, CA',
					to: 'Shattuck & University',
					from_coords: { lat: 37.8715, lng: -122.2730 },
					to_coords: { lat: 37.8710, lng: -122.2682 },
					duration: 5,
					distance: 0.25,
					cost: 0
				},
				{
					mode: 'transit',
					from: 'Shattuck & University',
					to: 'Broadway & 14th St',
					from_coords: { lat: 37.8710, lng: -122.2682 },
					to_coords: { lat: 37.8040, lng: -122.2718 },
					duration: 22,
					distance: 5.5,
					cost: 2.25,
					details: {
						line: 'AC Transit 51',
						departure_time: '2025-10-18T13:33:00-07:00',
						arrival_time: '2025-10-18T13:55:00-07:00',
						stops: 12
					}
				},
				{
					mode: 'walk',
					from: 'Broadway & 14th St',
					to: 'Downtown Oakland',
					from_coords: { lat: 37.8040, lng: -122.2718 },
					to_coords: { lat: 37.8044, lng: -122.2712 },
					duration: 5,
					distance: 0.2,
					cost: 0
				}
			]
		},
		{
			id: 'route-berk-3',
			summary: 'Bike share (Bay Wheels)',
			total_duration: 28,
			total_cost: 3.50,
			departure_time: '2025-10-18T13:32:00-07:00',
			arrival_time: '2025-10-18T14:00:00-07:00',
			confidence: 82,
			carbon_savings: 3.2,
			time_savings: 2,
			legs: [
				{
					mode: 'walk',
					from: 'Berkeley, CA',
					to: 'Bay Wheels Station - Center St',
					from_coords: { lat: 37.8715, lng: -122.2730 },
					to_coords: { lat: 37.8705, lng: -122.2695 },
					duration: 3,
					distance: 0.15,
					cost: 0
				},
				{
					mode: 'bike',
					from: 'Bay Wheels Station - Center St',
					to: 'Bay Wheels Station - 14th St Oakland',
					from_coords: { lat: 37.8705, lng: -122.2695 },
					to_coords: { lat: 37.8042, lng: -122.2715 },
					duration: 22,
					distance: 5.3,
					cost: 3.50,
					details: {}
				},
				{
					mode: 'walk',
					from: 'Bay Wheels Station - 14th St Oakland',
					to: 'Downtown Oakland',
					from_coords: { lat: 37.8042, lng: -122.2715 },
					to_coords: { lat: 37.8044, lng: -122.2712 },
					duration: 3,
					distance: 0.1,
					cost: 0
				}
			]
		}
	],
	generated_at: '2025-10-18T13:00:00-07:00'
};
