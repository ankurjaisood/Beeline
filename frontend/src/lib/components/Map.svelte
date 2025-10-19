<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
		import { browser } from '$app/environment';
		import type { RouteOption } from '$lib/types';
		import { decodePolyline } from '$lib/utils/polyline';

		export let route: RouteOption | null = null;
		export let routes: RouteOption[] | null = null;
		export let selectedRoute: RouteOption | null = null;
		export let height: string = '500px';

		let mapContainer: HTMLDivElement;
		let map: any = null;
		let L: any = null;
		let markers: any[] = [];
		let polylines: any[] = [];

		// Convert single route to array for uniform handling
		$: routesToDraw = route ? [route] : (routes || []);
		$: console.log('Map component - route:', route, 'routes:', routes, 'routesToDraw:', routesToDraw);

		// Mode colors for route legs
		const modeColors: Record<string, string> = {
			drive: '#3b82f6', // blue
			park: '#8b5cf6', // purple
			walk: '#10b981', // green
			transit: '#ef4444', // red
			rideshare: '#f59e0b', // amber
			bike: '#06b6d4', // cyan
			scooter: '#ec4899' // pink
		};

		const routeColors = [
			'#3B82F6', // blue
			'#10B981', // green
			'#F59E0B', // amber
			'#EF4444', // red
			'#8B5CF6', // purple
			'#EC4899', // pink
		];

		// Function to generate highly distinct color variations for legs within a route
		function getLegColor(baseColor: string, legIndex: number, totalLegs: number): string {
			if (totalLegs === 1) return baseColor;

			// Parse hex color
			const r = parseInt(baseColor.slice(1, 3), 16);
			const g = parseInt(baseColor.slice(3, 5), 16);
			const b = parseInt(baseColor.slice(5, 7), 16);

			// Create dramatically different shades with very high contrast
			// Using discrete steps instead of smooth gradient for maximum distinction
			const steps = [0.3, 0.6, 0.9, 1.2, 1.5, 1.8];
			const stepIndex = Math.floor((legIndex / (totalLegs - 1)) * (steps.length - 1));
			const factor = steps[stepIndex];

			// Also shift hue slightly for even more distinction
			const hueShift = (legIndex / totalLegs) * 30; // Shift up to 30 degrees

			// Apply brightness factor with dramatic range
			let newR = Math.min(255, Math.round(r * factor));
			let newG = Math.min(255, Math.round(g * factor));
			let newB = Math.min(255, Math.round(b * factor));

			// Add alternating saturation boost for odd/even legs
			if (legIndex % 2 === 1) {
				// Boost saturation for odd legs
				const gray = (newR + newG + newB) / 3;
				newR = Math.min(255, Math.round(newR + (newR - gray) * 0.5));
				newG = Math.min(255, Math.round(newG + (newG - gray) * 0.5));
				newB = Math.min(255, Math.round(newB + (newB - gray) * 0.5));
			}

			return `rgb(${newR}, ${newG}, ${newB})`;
		}

		// Function to fetch route from OSRM (OpenStreetMap Routing Machine)
		async function fetchOSRMRoute(fromCoords: any, toCoords: any, mode: string = 'driving') {
			try {
				// Map our modes to OSRM profiles
				// Note: OSRM public demo only supports 'car', 'bike', and 'foot'
				const profileMap: Record<string, string> = {
					'drive': 'car',
					'rideshare': 'car',
					'bike': 'bike',
					'walk': 'foot'
				};
				const profile = profileMap[mode] || 'car';

				const url = `https://router.project-osrm.org/route/v1/${profile}/${fromCoords.lng},${fromCoords.lat};${toCoords.lng},${toCoords.lat}?overview=full&geometries=geojson`;
				console.log(`Fetching ${mode} route (${profile} profile):`, url);

				const response = await fetch(url);
				const data = await response.json();

				console.log(`OSRM response for ${mode}:`, data);

				if (data.code === 'Ok' && data.routes && data.routes.length > 0) {
					// OSRM returns GeoJSON coordinates [lng, lat]
					const coordinates = data.routes[0].geometry.coordinates.map((coord: number[]) => [coord[1], coord[0]]);
					console.log(`Successfully got ${coordinates.length} coordinates for ${mode}`);
					return coordinates;
				} else {
					console.warn(`OSRM failed for ${mode}:`, data.code, data.message);
				}
			} catch (error) {
				console.error(`Failed to fetch OSRM route for ${mode}:`, error);
			}
			return null;
		}

		onMount(async () => {
			if (!browser) return;

			// Dynamically import Leaflet (browser only)
			L = await import('leaflet');

			// Initialize map centered on SF Bay Area
			map = L.map(mapContainer).setView([37.7749, -122.4194], 9);

			// Add OpenStreetMap tiles (completely free!)
			L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
				attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
				maxZoom: 19
			}).addTo(map);

			if (routesToDraw && routesToDraw.length > 0) {
				drawRoutes(routesToDraw);
			}
		});

		onDestroy(() => {
			if (map) {
				map.remove();
			}
		});

		function clearMap() {
			if (!map || !L) return;

			// Remove existing markers
			markers.forEach(marker => map.removeLayer(marker));
			markers = [];

			// Remove existing polylines
			polylines.forEach(polyline => map.removeLayer(polyline));
			polylines = [];
		}

		async function drawRoutes(routeOptions: RouteOption[]) {

					if (!map || !L || !routeOptions || routeOptions.length === 0) {
						console.log('drawRoutes early return:', { map: !!map, L: !!L, routeOptions, length: routeOptions?.length });
						return;
					}

					console.log('Drawing routes:', routeOptions);

					clearMap();



					const bounds = L.latLngBounds([]);



					for (const [routeIndex, routeOption] of routeOptions.entries()) {

						const baseColor = routeColors[routeIndex % routeColors.length];
						const isSelected = selectedRoute?.id === routeOption.id;



						// Draw each leg

						for (const [index, leg] of routeOption.legs.entries()) {

							const color = getLegColor(baseColor, index, routeOption.legs.length);

							// Check if coordinates exist
							if (!leg.from_coords || !leg.to_coords) {
								console.warn('Missing coordinates for leg:', leg);
								continue;
							}

							const fromLatLng = L.latLng(leg.from_coords.lat, leg.from_coords.lng);

							const toLatLng = L.latLng(leg.to_coords.lat, leg.to_coords.lng);



							// Add markers for start and end

							if (index === 0) {

								// Start marker (green)

								const startMarker = L.marker(fromLatLng, {

									icon: L.divIcon({

										className: 'custom-marker',

										html: `<div style="background: #10b981; width: 24px; height: 24px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>`,

										iconSize: [24, 24],

										iconAnchor: [12, 12]

									})

								}).addTo(map);

								startMarker.bindPopup(`<strong>Start:</strong> ${leg.from}`);

								markers.push(startMarker);

							}



							// Transit stop or parking marker

							if (leg.mode === 'transit' || leg.mode === 'park') {

								const marker = L.marker(fromLatLng, {

									icon: L.divIcon({

										className: 'custom-marker',

										html: `<div style="background: ${color}; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>`,

										iconSize: [20, 20],

										iconAnchor: [10, 10]

									})

								}).addTo(map);



								const popupContent = `<strong>${leg.mode === 'park' ? 'Park' : 'Transit'}:</strong> ${leg.from}<br/>` +

									`<span style="font-size: 0.875rem;">${leg.details?.line || leg.details?.parking_lot || ''}</span>`;

								marker.bindPopup(popupContent);

								markers.push(marker);

							}



							if (index === routeOption.legs.length - 1) {

								// End marker (red)

								const endMarker = L.marker(toLatLng, {

									icon: L.divIcon({

										className: 'custom-marker',

										html: `<div style="background: #ef4444; width: 24px; height: 24px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>`,

										iconSize: [24, 24],

										iconAnchor: [12, 12]

									})

								}).addTo(map);

								endMarker.bindPopup(`<strong>Destination:</strong> ${leg.to}`);

								markers.push(endMarker);

							}



							// Draw polyline for this leg
							let routeCoordinates = null;

							// First priority: Use polyline from backend if available (Google Maps data)
							if (leg.polyline) {
								try {
									const decodedCoords = decodePolyline(leg.polyline);
									routeCoordinates = decodedCoords;
									console.log(`Using Google Maps polyline for ${leg.mode}: ${decodedCoords.length} points`);
								} catch (error) {
									console.warn('Failed to decode polyline:', error);
								}
							}

							// Second priority: Fetch from OSRM for road-based modes if no polyline
							if (!routeCoordinates) {
								if (leg.mode === 'drive' || leg.mode === 'rideshare') {
									routeCoordinates = await fetchOSRMRoute(leg.from_coords, leg.to_coords, 'drive');
								} else if (leg.mode === 'bike') {
									routeCoordinates = await fetchOSRMRoute(leg.from_coords, leg.to_coords, 'bike');
								} else if (leg.mode === 'walk') {
									routeCoordinates = await fetchOSRMRoute(leg.from_coords, leg.to_coords, 'walk');
								}
							}

							// Fallback to straight line if all else fails
							const coordinates = routeCoordinates || [fromLatLng, toLatLng];

							const polyline = L.polyline(coordinates, {

								color: color,

								weight: isSelected ? 6 : 4,

								opacity: isSelected ? 1 : 0.6

							}).addTo(map);



							polylines.push(polyline);



							// Extend bounds

							bounds.extend(fromLatLng);

							bounds.extend(toLatLng);

						}

					}



					// Fit map to route bounds

					map.fitBounds(bounds, { padding: [50, 50], maxZoom: 12 });

				}



				$: if (map && L && routesToDraw) {

					drawRoutes(routesToDraw);

				}	</script>
<svelte:head>
	<!-- Leaflet CSS -->
	<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
		integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
		crossorigin="" />
</svelte:head>

<div bind:this={mapContainer} style="height: {height};" class="rounded-lg overflow-hidden shadow-lg" />
