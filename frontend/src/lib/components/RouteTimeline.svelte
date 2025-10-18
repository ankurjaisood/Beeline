<script lang="ts">
	import { Car, ParkingCircle, Train, FootprintsIcon, Check } from 'lucide-svelte';
	import type { RouteOption, RouteLeg } from '$lib/types';
	import { format } from 'date-fns';

	export let route: RouteOption;
	export let onSelectRoute: () => void = () => {};

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
	<!-- Route Header -->
	<div class="mb-6">
		<h2 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-2">
			{route.summary}
		</h2>
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
			<div class="flex items-start gap-4 group hover:bg-gray-50 dark:hover:bg-gray-700/50 p-3 rounded-lg transition-colors">
				<!-- Time -->
				<div class="w-20 flex-shrink-0 text-sm font-medium text-gray-600 dark:text-gray-400 pt-1">
					{time}
				</div>

				<!-- Icon -->
				<div class="flex-shrink-0">
					<div class="w-10 h-10 rounded-full {modeColors[leg.mode]} flex items-center justify-center text-white shadow-md">
						<svelte:component this={modeIcons[leg.mode]} class="w-5 h-5" />
					</div>
				</div>

				<!-- Details -->
				<div class="flex-1 pt-1">
					<div class="font-semibold text-gray-900 dark:text-gray-100 mb-1">
						{getLegLabel(leg)} <span class="text-gray-500 dark:text-gray-400 font-normal">{leg.duration} min</span>
					</div>
					<div class="text-sm text-gray-600 dark:text-gray-400">
						{leg.distance.toFixed(1)} mi
						{#if leg.details?.traffic_level}
							• {leg.details.traffic_level} traffic
						{/if}
						{#if leg.details?.parking_availability}
							• {leg.details.parking_availability}% available
						{/if}
						{#if leg.details?.stops}
							• {leg.details.stops} stops
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
