<script lang="ts">
	import { Car, ParkingCircle, Train, FootprintsIcon, Check, ExternalLink } from 'lucide-svelte';
	import type { RouteOption, RouteLeg } from '$lib/types';
	import { format } from 'date-fns';

	export let route: RouteOption;
	export let routeIndex: number = 0;
	export let onSelectRoute: () => void = () => {};

	const routeColors = [
		'#3B82F6', // blue
		'#10B981', // green
		'#F59E0B', // amber
		'#EF4444', // red
		'#8B5CF6', // purple
		'#EC4899', // pink
	];

	const baseColor = routeColors[routeIndex % routeColors.length];

	// Function to generate color for each leg (matching the map)
	function getLegColor(legIndex: number, totalLegs: number): string {
		if (totalLegs === 1) return baseColor;

		const r = parseInt(baseColor.slice(1, 3), 16);
		const g = parseInt(baseColor.slice(3, 5), 16);
		const b = parseInt(baseColor.slice(5, 7), 16);

		const steps = [0.3, 0.6, 0.9, 1.2, 1.5, 1.8];
		const stepIndex = Math.floor((legIndex / (totalLegs - 1)) * (steps.length - 1));
		const factor = steps[stepIndex];

		let newR = Math.min(255, Math.round(r * factor));
		let newG = Math.min(255, Math.round(g * factor));
		let newB = Math.min(255, Math.round(b * factor));

		if (legIndex % 2 === 1) {
			const gray = (newR + newG + newB) / 3;
			newR = Math.min(255, Math.round(newR + (newR - gray) * 0.5));
			newG = Math.min(255, Math.round(newG + (newG - gray) * 0.5));
			newB = Math.min(255, Math.round(newB + (newB - gray) * 0.5));
		}

		return `rgb(${newR}, ${newG}, ${newB})`;
	}

	// Generate Google Maps directions URL for a leg
	function getGoogleMapsUrl(leg: RouteLeg): string {
		const origin = `${leg.from_coords.lat},${leg.from_coords.lng}`;
		const destination = `${leg.to_coords.lat},${leg.to_coords.lng}`;

		// Map mode to Google Maps travel mode
		let travelMode = 'driving';
		if (leg.mode === 'walk') travelMode = 'walking';
		else if (leg.mode === 'bike') travelMode = 'bicycling';
		else if (leg.mode === 'transit') travelMode = 'transit';

		return `https://www.google.com/maps/dir/?api=1&origin=${origin}&destination=${destination}&travelmode=${travelMode}`;
	}

	const modeIcons: Record<string, any> = {
		drive: Car,
		park: ParkingCircle,
		walk: FootprintsIcon,
		transit: Train,
		rideshare: Car,
		bike: FootprintsIcon,
		scooter: FootprintsIcon
	};

	const modeLabels: Record<string, string> = {
		drive: 'Drive',
		park: 'Park',
		walk: 'Walk',
		transit: 'Transit',
		rideshare: 'Rideshare',
		bike: 'Bike',
		scooter: 'Scooter'
	};

	const modeColors: Record<string, string> = {
		drive: 'bg-blue-500',
		park: 'bg-purple-500',
		walk: 'bg-green-500',
		transit: 'bg-red-500',
		rideshare: 'bg-amber-500',
		bike: 'bg-cyan-500',
		scooter: 'bg-pink-500'
	};

	function formatTime(isoString: string | undefined): string {
		if (!isoString) return '--:--';
		try {
			const date = new Date(isoString);
			if (isNaN(date.getTime())) return '--:--';
			return format(date, 'h:mm a');
		} catch {
			return '--:--';
		}
	}

	function getLegLabel(leg: RouteLeg): string {
		if (leg.mode === 'transit' && leg.details?.line) {
			return leg.details.line;
		}
		if (leg.mode === 'park' && leg.details?.parking_lot) {
			return 'Park';
		}
		return modeLabels[leg.mode] || leg.mode;
	}

	// Calculate cumulative time for each step
	let cumulativeTime = 0;
	function getCumulativeTime(index: number): string {
		if (index === 0) {
			cumulativeTime = 0;
			return formatTime(route.departure_time);
		}

		for (let i = 0; i < index; i++) {
			cumulativeTime += route.legs[i].duration;
		}

		if (!route.departure_time) {
			return `+${cumulativeTime} min`;
		}

		try {
			const departureDate = new Date(route.departure_time);
			if (isNaN(departureDate.getTime())) {
				return `+${cumulativeTime} min`;
			}
			const stepTime = new Date(departureDate.getTime() + cumulativeTime * 60000);
			return formatTime(stepTime.toISOString());
		} catch {
			return `+${cumulativeTime} min`;
		}
	}
</script>

<div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 border border-gray-200 dark:border-gray-700">
	<!-- Route Header with Mode Icons -->
	<div class="mb-6">
		<!-- Mode sequence -->
		<div class="flex items-center gap-2 mb-4">
			{#each route.legs as leg, index}
				{@const legColor = getLegColor(index, route.legs.length)}
				<div class="flex items-center gap-2">
					<div class="w-12 h-12 rounded-full flex items-center justify-center text-white shadow-md" style="background-color: {legColor};">
						<svelte:component this={modeIcons[leg.mode]} class="w-6 h-6" />
					</div>
					{#if index < route.legs.length - 1}
						<div class="w-8 h-0.5 bg-gray-300 dark:bg-gray-600"></div>
					{/if}
				</div>
			{/each}
		</div>

		<!-- Summary stats -->
		<div class="flex flex-wrap gap-4 text-sm">
			<span class="text-gray-600 dark:text-gray-400">
				<span class="font-semibold text-gray-900 dark:text-gray-100">{route.total_duration} min</span> total time
			</span>
			<span class="text-gray-600 dark:text-gray-400">
				<span class="font-semibold text-gray-900 dark:text-gray-100">${route.total_cost.toFixed(2)}</span> total cost
			</span>
			{#if route.time_savings}
				<span class="text-green-600 dark:text-green-400">
					<span class="font-semibold">↓{route.time_savings} min</span> vs driving
				</span>
			{/if}
			{#if route.carbon_savings}
				<span class="text-emerald-600 dark:text-emerald-400">
					<span class="font-semibold">↓{route.carbon_savings.toFixed(1)} kg CO₂</span>
				</span>
			{/if}
		</div>
	</div>

	<!-- Timeline -->
	<div class="space-y-1 mb-6">
		{#each route.legs as leg, index}
			{@const time = getCumulativeTime(index)}
			{@const legColor = getLegColor(index, route.legs.length)}
			<div class="flex items-start gap-4 group hover:bg-gray-50 dark:hover:bg-gray-700/50 p-3 rounded-lg transition-colors border-l-4" style="border-left-color: {legColor};">
				<!-- Time -->
				<div class="w-20 flex-shrink-0 text-sm font-medium text-gray-600 dark:text-gray-400 pt-1">
					{time}
				</div>

				<!-- Icon with matching color -->
				<div class="flex-shrink-0">
					<div class="w-10 h-10 rounded-full flex items-center justify-center text-white shadow-md" style="background-color: {legColor};">
						<svelte:component this={modeIcons[leg.mode]} class="w-5 h-5" />
					</div>
				</div>

				<!-- Details -->
				<div class="flex-1 pt-1">
					<div class="flex items-center gap-2 mb-1">
						<span class="font-semibold text-gray-900 dark:text-gray-100">
							{getLegLabel(leg)} <span class="text-gray-500 dark:text-gray-400 font-normal">{leg.duration} min</span>
						</span>
						<a
							href={getGoogleMapsUrl(leg)}
							target="_blank"
							rel="noopener noreferrer"
							class="inline-flex items-center gap-1 text-xs text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 transition-colors"
							title="View in Google Maps"
						>
							<ExternalLink class="w-3 h-3" />
							<span>Maps</span>
						</a>
					</div>
					<div class="text-sm text-gray-600 dark:text-gray-400 mb-1">
						{leg.from} → {leg.to}
					</div>
					<div class="text-sm text-gray-600 dark:text-gray-400 flex flex-wrap gap-2">
						<span>{leg.distance.toFixed(1)} mi</span>
						{#if leg.details?.traffic_level}
							<span>• {leg.details.traffic_level} traffic</span>
						{/if}
						{#if leg.details?.parking_availability}
							<span>• {leg.details.parking_availability}% parking</span>
						{/if}
						{#if leg.details?.parking_rate}
							<span>• {leg.details.parking_rate}</span>
						{/if}
						{#if leg.details?.stops}
							<span>• {leg.details.stops} stops</span>
						{/if}
						{#if leg.details?.departure_time && leg.details?.arrival_time}
							<span>• Departs {formatTime(leg.details.departure_time)}</span>
						{/if}
						{#if leg.details?.provider}
							<span>• {leg.details.provider}</span>
						{/if}
						{#if leg.details?.wait_time}
							<span>• {leg.details.wait_time} min wait</span>
						{/if}
						{#if leg.details?.toll_cost && leg.details.toll_cost > 0}
							<span class="text-amber-600 dark:text-amber-400">• ${leg.details.toll_cost.toFixed(2)} toll</span>
						{/if}
					</div>
				</div>

				<!-- Cost -->
				<div class="w-16 text-right flex-shrink-0 pt-1">
					{#if leg.cost > 0}
						<span class="font-semibold text-gray-900 dark:text-gray-100">${leg.cost.toFixed(2)}</span>
					{:else}
						<span class="text-gray-400 dark:text-gray-600">—</span>
					{/if}
				</div>
			</div>
		{/each}

		<!-- Arrival -->
		<div class="flex items-start gap-4 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
			<div class="w-20 flex-shrink-0 text-sm font-medium text-gray-600 dark:text-gray-400 pt-1">
				{formatTime(route.arrival_time)}
			</div>
			<div class="flex-shrink-0">
				<div class="w-10 h-10 rounded-full bg-green-500 flex items-center justify-center text-white shadow-md">
					<Check class="w-6 h-6" />
				</div>
			</div>
			<div class="flex-1 pt-1">
				<div class="font-semibold text-green-900 dark:text-green-100">
					Arrive at destination
				</div>
			</div>
		</div>
	</div>

	<!-- Action Button -->
	<button
		on:click={onSelectRoute}
		class="w-full bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors shadow-md hover:shadow-lg"
	>
		Select This Route
	</button>
</div>
