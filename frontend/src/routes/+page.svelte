<script lang="ts">
	import { Sun, Moon, Zap, DollarSign, Leaf } from 'lucide-svelte';
	import Map from '$lib/components/Map.svelte';
	import RouteTimeline from '$lib/components/RouteTimeline.svelte';
	import RoutePreview from '$lib/components/RoutePreview.svelte';
	import { searchRoutes } from '$lib/services/api';
	import { routeResponse, selectedRoute, sortedRoutes, selectRoute, filters, isLoading, error } from '$lib/stores/routeStore';
	import { theme, toggleTheme } from '$lib/stores/themeStore';
	import type { OptimizationPreference } from '$lib/types';

	let query = '';
	let isSearching = false;
	let exampleQueryIndex = -1;

	const exampleQueries = [
		'Get me from San Jose to Salesforce Tower by 10 am',
		'Palo Alto to Oracle Park by 7pm',
		'Milpitas to Moscone Center by 11am',
		'Berkeley to downtown Oakland by 2pm'
	];

	// Auto-select first route when routes are loaded
	$: if ($sortedRoutes.length > 0 && !$selectedRoute) {
		selectRoute($sortedRoutes[0]);
	}

	async function handleSearch() {
		if (!query.trim()) {
			error.set('Please enter a destination or query');
			return;
		}

		isSearching = true;
		isLoading.set(true);
		error.set(null);

		try {
			const response = await searchRoutes(query);
			routeResponse.set(response);
		} catch (err) {
			error.set(err instanceof Error ? err.message : 'An error occurred');
		} finally {
			isSearching = false;
			isLoading.set(false);
		}
	}

	function handleKeyPress(event: KeyboardEvent) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			handleSearch();
		}
	}

	function handleKeyDown(event: KeyboardEvent) {
		if (event.key === 'Tab') {
			event.preventDefault();
			exampleQueryIndex = (exampleQueryIndex + 1) % exampleQueries.length;
			query = exampleQueries[exampleQueryIndex];
		}
	}

	function useExample(exampleQuery: string) {
		query = exampleQuery;
		handleSearch();
	}

	function setOptimization(pref: OptimizationPreference) {
		filters.update(f => ({ ...f, optimize: pref }));
	}

	function handleSelectRoute(route: any) {
		selectRoute(route);
	}
</script>

<svelte:head>
	<title>Beeline - Smart Multi-Modal Transit</title>
	<meta name="description" content="AI-powered transit routing for the Bay Area" />
</svelte:head>

<div class="bg-gray-50 dark:bg-gray-900 transition-colors min-h-screen flex flex-col">
	<!-- Header with Search Bar -->
	<header class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-sm sticky top-0 z-20 transition-colors">
		<div class="max-w-full mx-auto px-6 py-4">
			<div class="flex items-center justify-between gap-4">
				<!-- Logo -->
				<div class="flex items-center gap-3 flex-shrink-0">
					<img src="/beeline_logo.png" alt="Beeline Logo" class="w-10 h-10 object-contain" />
					<div>
						<h1 class="text-xl font-bold text-gray-900 dark:text-gray-100">Beeline</h1>
						<p class="text-xs text-gray-600 dark:text-gray-400">Multi-Modal Transit</p>
					</div>
				</div>

				<!-- Search Bar -->
				<div class="flex-1 max-w-3xl">
					<div class="flex gap-2">
						<input
							type="text"
							bind:value={query}
							on:keypress={handleKeyPress}
							on:keydown={handleKeyDown}
							placeholder="Where do you want to go? (e.g., San Jose to Salesforce Tower by 10am)"
							class="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400"
							disabled={isSearching}
						/>
						<button
							on:click={handleSearch}
							disabled={isSearching || !query.trim()}
							class="px-6 py-2 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-300 dark:disabled:bg-gray-600 text-white font-semibold rounded-lg transition-all flex-shrink-0"
						>
							{#if isSearching}
								<div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
							{:else}
								Search
							{/if}
						</button>
					</div>

					{#if $error}
						<div class="mt-2 p-2 bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-400 text-sm">
							{$error}
						</div>
					{/if}
				</div>

				<!-- Theme Toggle -->
				<button
					on:click={toggleTheme}
					class="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors flex-shrink-0"
					aria-label="Toggle theme"
				>
					{#if $theme === 'light'}
						<Moon class="w-5 h-5 text-gray-600" />
					{:else}
						<Sun class="w-5 h-5 text-gray-400" />
					{/if}
				</button>
			</div>
		</div>
	</header>

	<!-- Main Content -->
	<div class="flex flex-1">
		<!-- Left Sidebar (25%) -->
		<aside class="w-1/4 bg-slate-800 dark:bg-slate-900 text-white overflow-y-auto border-r border-slate-700 transition-colors">
			<div class="p-6 space-y-6">
				<!-- Query Summary -->
				{#if $routeResponse}
				<div class="pb-4 border-b border-slate-700">
					<p class="text-xs text-slate-400 mb-1">Route from</p>
					<p class="text-sm font-semibold">{$routeResponse.query.origin}</p>
					<p class="text-xs text-slate-400 mt-2 mb-1">to</p>
					<p class="text-sm font-semibold">{$routeResponse.query.destination}</p>
				</div>
				{/if}

				<!-- Quick Presets -->
				<div>
					<h3 class="text-xs uppercase tracking-wider text-slate-400 mb-3 font-semibold">Quick Filters</h3>
					<div class="space-y-2">
						<button
							on:click={() => setOptimization('time')}
							class="w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all {$filters.optimize === 'time'
								? 'bg-cyan-600 shadow-lg shadow-cyan-600/30'
								: 'bg-slate-700 hover:bg-slate-600'}"
						>
							<Zap class="w-5 h-5" />
							<span class="font-medium">Fastest</span>
						</button>
						<button
							on:click={() => setOptimization('cost')}
							class="w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all {$filters.optimize === 'cost'
								? 'bg-green-600 shadow-lg shadow-green-600/30'
								: 'bg-slate-700 hover:bg-slate-600'}"
						>
							<DollarSign class="w-5 h-5" />
							<span class="font-medium">Cheapest</span>
						</button>
						<button
							on:click={() => setOptimization('environmental')}
							class="w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all {$filters.optimize === 'environmental'
								? 'bg-emerald-600 shadow-lg shadow-emerald-600/30'
								: 'bg-slate-700 hover:bg-slate-600'}"
						>
							<Leaf class="w-5 h-5" />
							<span class="font-medium">Greenest</span>
						</button>
					</div>
				</div>

				<!-- Transportation Modes -->
				<div>
					<h3 class="text-xs uppercase tracking-wider text-slate-400 mb-3 font-semibold">Transportation Modes</h3>
					<div class="space-y-2">
						<label class="flex items-center gap-3 cursor-pointer group">
							<input
								type="checkbox"
								bind:checked={$filters.modes.driving}
								class="w-4 h-4 text-cyan-600 rounded focus:ring-cyan-500 focus:ring-offset-slate-800"
							/>
							<span class="text-sm group-hover:text-cyan-400 transition-colors">Driving</span>
						</label>
						<label class="flex items-center gap-3 cursor-pointer group">
							<input
								type="checkbox"
								bind:checked={$filters.modes.transit}
								class="w-4 h-4 text-cyan-600 rounded focus:ring-cyan-500 focus:ring-offset-slate-800"
							/>
							<span class="text-sm group-hover:text-cyan-400 transition-colors">Public Transit</span>
						</label>
						<label class="flex items-center gap-3 cursor-pointer group">
							<input
								type="checkbox"
								bind:checked={$filters.modes.rideshare}
								class="w-4 h-4 text-cyan-600 rounded focus:ring-cyan-500 focus:ring-offset-slate-800"
							/>
							<span class="text-sm group-hover:text-cyan-400 transition-colors">Rideshare</span>
						</label>
						<label class="flex items-center gap-3 cursor-pointer group">
							<input
								type="checkbox"
								bind:checked={$filters.modes.micromobility}
								class="w-4 h-4 text-cyan-600 rounded focus:ring-cyan-500 focus:ring-offset-slate-800"
							/>
							<span class="text-sm group-hover:text-cyan-400 transition-colors">Walking / Biking</span>
						</label>
					</div>
				</div>

				<!-- Constraints -->
				<div>
					<h3 class="text-xs uppercase tracking-wider text-slate-400 mb-3 font-semibold">Constraints</h3>
					<div class="space-y-4">
						<div>
							<label class="text-sm text-slate-300 mb-2 block">
								Max walking: {$filters.maxWalkingDistance} mi
							</label>
							<input
								type="range"
								min="0.25"
								max="2"
								step="0.25"
								bind:value={$filters.maxWalkingDistance}
								class="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-cyan-600"
							/>
						</div>
						<label class="flex items-center gap-3 cursor-pointer group">
							<input
								type="checkbox"
								bind:checked={$filters.avoidTolls}
								class="w-4 h-4 text-cyan-600 rounded focus:ring-cyan-500 focus:ring-offset-slate-800"
							/>
							<span class="text-sm group-hover:text-cyan-400 transition-colors">Avoid tolls</span>
						</label>
						<label class="flex items-center gap-3 cursor-pointer group">
							<input
								type="checkbox"
								bind:checked={$filters.accessible}
								class="w-4 h-4 text-cyan-600 rounded focus:ring-cyan-500 focus:ring-offset-slate-800"
							/>
							<span class="text-sm group-hover:text-cyan-400 transition-colors">Accessible routes</span>
						</label>
					</div>
				</div>

				<!-- Route Previews -->
				{#if $sortedRoutes.length > 0}
					<div>
						<h3 class="text-xs uppercase tracking-wider text-slate-400 mb-3 font-semibold">
							{$sortedRoutes.length} {$sortedRoutes.length === 1 ? 'Route' : 'Routes'} Found
						</h3>
						<div class="space-y-2">
							{#each $sortedRoutes as route (route.id)}
								<RoutePreview
									{route}
									isSelected={$selectedRoute?.id === route.id}
									onClick={() => handleSelectRoute(route)}
								/>
							{/each}
						</div>
					</div>
				{/if}
			</div>
		</aside>

		<!-- Right Content (75%) -->
		<main class="flex-1 overflow-y-auto flex flex-col">
			<!-- Map (60% height) -->
			<div class="h-[60vh] border-b border-gray-200 dark:border-gray-700">
				<Map route={$selectedRoute} height="100%" />
			</div>

			{#if $selectedRoute}
				<div class="h-[40vh] flex-1 flex">
					<!-- Timeline (40% height) -->
					<div class="flex-1 overflow-y-auto bg-gray-50 dark:bg-gray-900 p-6">
						<RouteTimeline
							route={$selectedRoute}
							onSelectRoute={() => {
								alert('Route selected! (Connect to navigation app)');
							}}
						/>
					</div>
				</div>
			{:else}
				<div class="flex items-center justify-center h-[40vh] text-gray-500 dark:text-gray-400">
					<div class="text-center">
						<p class="text-lg">{$routeResponse ? 'Select a route to view details' : 'Welcome to Beeline! Enter a query to get started.'}</p>
					</div>
				</div>
			{/if}
		</main>
	</div>
</div>
