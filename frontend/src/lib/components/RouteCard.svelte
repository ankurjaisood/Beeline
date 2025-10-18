<script lang="ts">
	import { Clock, DollarSign, TrendingDown, Car, Train, FootprintsIcon, ParkingCircle } from 'lucide-svelte';
	import type { RouteOption, RouteLeg } from '$lib/types';
	import { format } from 'date-fns';

	export let route: RouteOption;
	export let isSelected: boolean = false;
	export let onClick: () => void = () => {};

	const modeIcons: Record<string, any> = {
		drive: Car,
		park: ParkingCircle,
		walk: FootprintsIcon,
		transit: Train,
		rideshare: Car,
		bike: FootprintsIcon,
		scooter: FootprintsIcon
	};

	const modeColors: Record<string, string> = {
		drive: 'bg-blue-100 text-blue-700',
		park: 'bg-purple-100 text-purple-700',
		walk: 'bg-green-100 text-green-700',
		transit: 'bg-red-100 text-red-700',
		rideshare: 'bg-amber-100 text-amber-700',
		bike: 'bg-cyan-100 text-cyan-700',
		scooter: 'bg-pink-100 text-pink-700'
	};

	function formatTime(isoString: string): string {
		return format(new Date(isoString), 'h:mm a');
	}

	function getModeLabel(leg: RouteLeg): string {
		if (leg.mode === 'transit' && leg.details?.line) {
			return leg.details.line;
		}
		if (leg.mode === 'park' && leg.details?.parking_lot) {
			return 'Park';
		}
		return leg.mode.charAt(0).toUpperCase() + leg.mode.slice(1);
	}
</script>

<button
	on:click={onClick}
	class="w-full text-left p-4 bg-white border-2 rounded-xl hover:shadow-lg transition-all {isSelected
		? 'border-primary-500 shadow-md'
		: 'border-gray-200'}"
>
	<!-- Header -->
	<div class="flex items-start justify-between mb-3">
		<div class="flex-1">
			<h3 class="font-semibold text-gray-900 mb-1">{route.summary}</h3>
			<div class="flex items-center gap-4 text-sm text-gray-600">
				<span class="flex items-center gap-1">
					<Clock class="w-4 h-4" />
					{route.total_duration} min
				</span>
				<span class="flex items-center gap-1">
					<DollarSign class="w-4 h-4" />
					${route.total_cost.toFixed(2)}
				</span>
				{#if route.carbon_savings}
					<span class="flex items-center gap-1 text-green-600">
						<TrendingDown class="w-4 h-4" />
						{route.carbon_savings.toFixed(1)} kg CO₂ saved
					</span>
				{/if}
			</div>
		</div>
		<div class="ml-4">
			<div class="bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-xs font-semibold">
				{route.confidence}% confident
			</div>
		</div>
	</div>

	<!-- Timeline -->
	<div class="space-y-2">
		{#each route.legs as leg, index}
			<div class="flex items-center gap-3">
				<div class="flex-shrink-0 w-8 h-8 rounded-full {modeColors[leg.mode]} flex items-center justify-center">
					<svelte:component this={modeIcons[leg.mode]} class="w-4 h-4" />
				</div>
				<div class="flex-1 min-w-0">
					<div class="text-sm font-medium text-gray-900 truncate">
						{getModeLabel(leg)}
					</div>
					<div class="text-xs text-gray-500 truncate">
						{#if leg.mode === 'transit' && leg.details}
							{leg.details.departure_time ? formatTime(leg.details.departure_time) : ''} - {leg.details.arrival_time ? formatTime(leg.details.arrival_time) : ''} • {leg.details.stops} stops
						{:else if leg.mode === 'park' && leg.details}
							{leg.details.parking_rate} • {leg.details.parking_availability}% available
						{:else}
							{leg.duration} min • {leg.distance.toFixed(1)} mi
						{/if}
					</div>
				</div>
				<div class="flex-shrink-0 text-sm font-medium text-gray-700">
					{#if leg.cost > 0}
						${leg.cost.toFixed(2)}
					{/if}
				</div>
			</div>
		{/each}
	</div>

	<!-- Times -->
	<div class="mt-3 pt-3 border-t border-gray-200 flex items-center justify-between text-sm">
		<span class="text-gray-600">
			Depart: <span class="font-medium text-gray-900">{formatTime(route.departure_time)}</span>
		</span>
		<span class="text-gray-600">
			Arrive: <span class="font-medium text-gray-900">{formatTime(route.arrival_time)}</span>
		</span>
	</div>
</button>
