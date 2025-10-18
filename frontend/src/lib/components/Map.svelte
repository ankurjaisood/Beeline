<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
		import { browser } from '$app/environment';
		import type { RouteOption } from '$lib/types';

		export let route: RouteOption | null = null;
		export let routes: RouteOption[] | null = null;
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

		const routeColors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#A133FF', '#33FFA1'];

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

		function drawRoutes(routeOptions: RouteOption[]) {

					if (!map || !L || !routeOptions || routeOptions.length === 0) {
						console.log('drawRoutes early return:', { map: !!map, L: !!L, routeOptions, length: routeOptions?.length });
						return;
					}

					console.log('Drawing routes:', routeOptions);

					clearMap();



					const bounds = L.latLngBounds([]);



					routeOptions.forEach((routeOption, routeIndex) => {

						const routeColor = routeColors[routeIndex % routeColors.length];



						// Draw each leg

						routeOption.legs.forEach((leg, index) => {

							const color = routeColor;

							// Check if coordinates exist
							if (!leg.from_coords || !leg.to_coords) {
								console.warn('Missing coordinates for leg:', leg);
								return;
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

							const polyline = L.polyline([fromLatLng, toLatLng], {

								color: color,

								weight: 4,

								opacity: 0.8

							}).addTo(map);



							polylines.push(polyline);



							// Extend bounds

							bounds.extend(fromLatLng);

							bounds.extend(toLatLng);

						});

					});



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
