<script lang="ts">
	import { goto } from '$app/navigation';
	import { Map as MapIcon, ArrowLeft, AlertCircle } from 'lucide-svelte';
	import Map from '$lib/components/Map.svelte';
	import RouteCard from '$lib/components/RouteCard.svelte';
	import FilterPanel from '$lib/components/FilterPanel.svelte';
	import { routeResponse, selectedRoute, sortedRoutes, selectRoute } from '$lib/stores/routeStore';

	let filterOpen = false;

	// Auto-select first route if none selected
	$: if ($sortedRoutes.length > 0 && !$selectedRoute) {
		selectRoute($sortedRoutes[0]);
	}

	// If no route data, redirect to home
	$: if (!$routeResponse) {
		goto('/');
	}
</script>

<svelte:head>
	<title>Route Results - Beeline</title>
</svelte:head>

<div class="min-h-screen bg-gray-50">
	<!-- Header -->
	<header class="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-10">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
			<div class="flex items-center justify-between">
				<div class="flex items-center gap-4">
					<button
						on:click={() => goto('/')}
						class="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
					>
						<ArrowLeft class="w-5 h-5" />
						<span class="hidden sm:inline">New Search</span>
					</button>
					<div class="h-6 w-px bg-gray-300" />
					<div class="flex items-center gap-2">
						<div class="bg-primary-500 rounded-lg p-2">
							<MapIcon class="w-5 h-5 text-white" />
						</div>
						<div>
							<h1 class="text-lg font-bold text-gray-900">Beeline</h1>
						</div>
					</div>
				</div>
				{#if $routeResponse}
					<div class="text-sm text-gray-600 hidden md:block">
						<span class="font-medium">{$routeResponse.query.origin}</span>
						<span class="mx-2">→</span>
						<span class="font-medium">{$routeResponse.query.destination}</span>
					</div>
				{/if}
			</div>
		</div>
	</header>

	<!-- Main Content -->
	<main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
		{#if $routeResponse}
			<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
				<!-- Left Panel: Filters & Route List -->
				<div class="lg:col-span-1 space-y-4">
					<!-- Filter Panel -->
					<FilterPanel bind:isOpen={filterOpen} />

					<!-- Route Results -->
					<div class="bg-white border border-gray-200 rounded-lg shadow-sm p-4">
						<h2 class="font-semibold text-gray-900 mb-3">
							{$sortedRoutes.length} {$sortedRoutes.length === 1 ? 'Route' : 'Routes'} Found
						</h2>

						{#if $sortedRoutes.length === 0}
							<div class="flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-lg">
								<AlertCircle class="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
								<div class="text-sm">
									<p class="font-medium text-amber-900 mb-1">No routes match your filters</p>
									<p class="text-amber-700">Try adjusting your preferences above.</p>
								</div>
							</div>
						{:else}
							<div class="space-y-3">
								{#each $sortedRoutes as route (route.id)}
									<RouteCard
										{route}
										isSelected={$selectedRoute?.id === route.id}
										onClick={() => selectRoute(route)}
									/>
								{/each}
							</div>
						{/if}
					</div>
				</div>

				<!-- Right Panel: Map -->
				<div class="lg:col-span-2">
					<div class="bg-white border border-gray-200 rounded-lg shadow-sm p-4">
						{#if $selectedRoute}
							<div class="mb-4">
								<h2 class="text-xl font-bold text-gray-900 mb-2">
									{$selectedRoute.summary}
								</h2>
								<div class="flex flex-wrap gap-4 text-sm text-gray-600">
									<span>
										<span class="font-semibold">{$selectedRoute.total_duration} min</span> total time
									</span>
									<span>
										<span class="font-semibold">${$selectedRoute.total_cost.toFixed(2)}</span> total cost
									</span>
									{#if $selectedRoute.time_savings}
										<span class="text-green-600">
											<span class="font-semibold">{$selectedRoute.time_savings} min</span> saved vs driving
										</span>
									{/if}
									{#if $selectedRoute.carbon_savings}
										<span class="text-emerald-600">
											<span class="font-semibold">{$selectedRoute.carbon_savings.toFixed(1)} kg CO₂</span> saved
										</span>
									{/if}
								</div>
							</div>
							<Map route={$selectedRoute} height="600px" />
						{:else}
							<div class="flex items-center justify-center h-96 text-gray-500">
								<div class="text-center">
									<MapIcon class="w-12 h-12 mx-auto mb-2 text-gray-400" />
									<p>Select a route to view on map</p>
								</div>
							</div>
						{/if}
					</div>

					<!-- Route Details -->
					{#if $selectedRoute}
						<div class="mt-6 bg-white border border-gray-200 rounded-lg shadow-sm p-6">
							<h3 class="font-semibold text-gray-900 mb-4">Journey Details</h3>
							<div class="space-y-4">
								{#each $selectedRoute.legs as leg, index}
									<div class="flex gap-4">
										<div class="flex flex-col items-center">
											<div class="w-3 h-3 rounded-full bg-primary-500" />
											{#if index < $selectedRoute.legs.length - 1}
												<div class="w-px h-full bg-gray-300 my-1" />
											{/if}
										</div>
										<div class="flex-1 pb-4">
											<div class="font-medium text-gray-900 capitalize mb-1">
												{leg.mode === 'transit' && leg.details?.line ? leg.details.line : leg.mode}
											</div>
											<div class="text-sm text-gray-600 mb-2">
												<div>{leg.from}</div>
												<div class="text-gray-400 my-1">↓</div>
												<div>{leg.to}</div>
											</div>
											<div class="flex flex-wrap gap-3 text-xs text-gray-500">
												<span>{leg.duration} min</span>
												<span>{leg.distance.toFixed(1)} mi</span>
												{#if leg.cost > 0}
													<span class="font-medium text-gray-700">${leg.cost.toFixed(2)}</span>
												{/if}
												{#if leg.details?.traffic_level}
													<span class="capitalize">{leg.details.traffic_level} traffic</span>
												{/if}
												{#if leg.details?.parking_availability}
													<span>{leg.details.parking_availability}% parking available</span>
												{/if}
												{#if leg.details?.stops}
													<span>{leg.details.stops} stops</span>
												{/if}
											</div>
										</div>
									</div>
								{/each}
							</div>
						</div>
					{/if}
				</div>
			</div>
		{/if}
	</main>
</div>
