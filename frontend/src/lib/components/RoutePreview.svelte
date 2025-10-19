<script lang="ts">
	import { Car, Train, FootprintsIcon, Clock, DollarSign, Eye, EyeOff } from 'lucide-svelte';
	import type { RouteOption } from '$lib/types';

	export let route: RouteOption;
	export let isSelected: boolean = false;
	export let isVisible: boolean = true;
	export let routeIndex: number = 0;
	export let onClick: () => void;
	export let onToggleVisibility: () => void;

	const routeColors = [
		'#3B82F6', // blue
		'#10B981', // green
		'#F59E0B', // amber
		'#EF4444', // red
		'#8B5CF6', // purple
		'#EC4899', // pink
	];

	const routeColor = routeColors[routeIndex % routeColors.length];

	// Get unique modes in this route
	const uniqueModes = [...new Set(route.legs.map(leg => leg.mode))];

	const modeEmojis: Record<string, string> = {
		drive: '🚗',
		park: '🅿️',
		walk: '🚶',
		transit: '🚆',
		rideshare: '🚕',
		bike: '🚴',
		scooter: '🛴'
	};
</script>

<div
	class="w-full text-left p-4 rounded-lg border-2 transition-all cursor-pointer {isSelected
		? 'bg-primary-50 dark:bg-primary-900/20 border-primary-500 shadow-md'
		: 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-700 hover:shadow-sm'}"
>
	<div class="flex items-start gap-3">
		<!-- Route color indicator -->
		<div class="mt-1 w-4 h-4 rounded-full flex-shrink-0" style="background-color: {routeColor};"></div>

		<button
			on:click|stopPropagation={onToggleVisibility}
			class="mt-1 p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
			aria-label={isVisible ? 'Hide route on map' : 'Show route on map'}
		>
			{#if isVisible}
				<Eye class="w-4 h-4 text-primary-600 dark:text-primary-400" />
			{:else}
				<EyeOff class="w-4 h-4 text-gray-400 dark:text-gray-500" />
			{/if}
		</button>
		<div class="flex-1" on:click={onClick} role="button" tabindex="0" on:keypress={(e) => e.key === 'Enter' && onClick()}>
			<!-- Route modes -->
			<div class="flex items-center gap-1 mb-2">
				{#each uniqueModes as mode}
					<span class="text-lg">{modeEmojis[mode] || '•'}</span>
				{/each}
				{#if uniqueModes.length > 1}
					<span class="text-xs text-gray-500 dark:text-gray-400 ml-1">
						{uniqueModes.length} modes
					</span>
				{/if}
			</div>

			<!-- Route summary -->
			<div class="font-semibold text-gray-900 dark:text-gray-100 mb-2 text-sm line-clamp-2">
				{route.summary}
			</div>

			<!-- Stats -->
			<div class="flex items-center gap-3 text-xs text-gray-600 dark:text-gray-400">
				<span class="flex items-center gap-1">
					<Clock class="w-3 h-3" />
					{route.total_duration}m
				</span>
				<span class="flex items-center gap-1">
					<DollarSign class="w-3 h-3" />
					{route.total_cost.toFixed(0)}
				</span>
				{#if route.carbon_savings}
					<span class="text-green-600 dark:text-green-400 font-medium">
						↓{route.carbon_savings.toFixed(1)}kg
					</span>
				{/if}
			</div>

			<!-- Confidence badge -->
			{#if route.confidence >= 90}
				<div class="mt-2">
					<span class="inline-block bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 text-xs px-2 py-0.5 rounded-full">
						{route.confidence}% confident
					</span>
				</div>
			{/if}
		</div>
	</div>
</div>

<style>
	.line-clamp-2 {
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}
</style>
