<script lang="ts">
	import { goto } from '$app/navigation';
	import { Map, ArrowRight, Sparkles, Clock, DollarSign, Leaf } from 'lucide-svelte';
	import { searchRoutes } from '$lib/services/api';
	import { routeResponse, isLoading, error } from '$lib/stores/routeStore';

	let query = '';
	let isSearching = false;

	const exampleQueries = [
		'Get me from San Jose to Salesforce Tower by 10 am. I want to drive to a Caltrain station.',
		'I\'m at Palo Alto downtown. Need to get to Oracle Park by 7pm. Don\'t want to pay for parking.',
		'From San Mateo to SF Ferry Building by 9am. I prefer BART over Caltrain.',
		'Get me from Milpitas to Moscone Center by 11am. I\'m okay with ride-sharing to transit.'
	];

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
			goto('/results');
		} catch (err) {
			error.set(err instanceof Error ? err.message : 'An error occurred');
		} finally {
			isSearching = false;
			isLoading.set(false);
		}
	}

	function useExample(exampleQuery: string) {
		query = exampleQuery;
	}

	function handleKeyPress(event: KeyboardEvent) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			handleSearch();
		}
	}
</script>

<svelte:head>
	<title>Beeline - Smart Multi-Modal Transit</title>
	<meta name="description" content="AI-powered transit routing for the Bay Area" />
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50">
	<!-- Header -->
	<header class="bg-white border-b border-gray-200 shadow-sm">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
			<div class="flex items-center gap-3">
				<div class="bg-primary-500 rounded-lg p-2">
					<Map class="w-6 h-6 text-white" />
				</div>
				<div>
					<h1 class="text-2xl font-bold text-gray-900">Beeline</h1>
					<p class="text-sm text-gray-600">Smart Multi-Modal Transit</p>
				</div>
			</div>
		</div>
	</header>

	<!-- Main Content -->
	<main class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
		<!-- Hero Section -->
		<div class="text-center mb-12 animate-fade-in">
			<div class="inline-flex items-center gap-2 bg-primary-100 text-primary-700 px-4 py-2 rounded-full text-sm font-medium mb-4">
				<Sparkles class="w-4 h-4" />
				<span>AI-Powered Route Optimization</span>
			</div>
			<h2 class="text-4xl sm:text-5xl font-bold text-gray-900 mb-4">
				Drive, Park, and Ride<br />in Perfect Harmony
			</h2>
			<p class="text-xl text-gray-600 max-w-2xl mx-auto">
				Beeline combines driving, parking, and public transit to get you to your Bay Area destination faster and cheaper.
			</p>
		</div>

		<!-- Search Box -->
		<div class="mb-12 animate-slide-in-up">
			<div class="bg-white rounded-2xl shadow-xl p-6 border border-gray-200">
				<label for="query" class="block text-sm font-medium text-gray-700 mb-2">
					Where do you want to go?
				</label>
				<div class="flex gap-3">
					<textarea
						id="query"
						bind:value={query}
						on:keypress={handleKeyPress}
						placeholder="e.g., Get me from San Jose to Salesforce Tower by 10 am. I want to drive to a Caltrain station."
						rows="3"
						class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
						disabled={isSearching}
					/>
				</div>

				{#if $error}
					<div class="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
						{$error}
					</div>
				{/if}

				<button
					on:click={handleSearch}
					disabled={isSearching || !query.trim()}
					class="mt-4 w-full bg-primary-600 hover:bg-primary-700 disabled:bg-gray-300 text-white font-semibold py-3 px-6 rounded-lg flex items-center justify-center gap-2 transition-all"
				>
					{#if isSearching}
						<div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
						<span>Finding best routes...</span>
					{:else}
						<span>Find Routes</span>
						<ArrowRight class="w-5 h-5" />
					{/if}
				</button>
			</div>
		</div>

		<!-- Example Queries -->
		<div class="mb-16">
			<h3 class="text-sm font-semibold text-gray-700 mb-3">Try an example:</h3>
			<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
				{#each exampleQueries as example}
					<button
						on:click={() => useExample(example)}
						class="text-left p-4 bg-white border border-gray-200 rounded-lg hover:border-primary-500 hover:shadow-md transition-all group"
					>
						<p class="text-sm text-gray-700 group-hover:text-primary-700 line-clamp-2">
							{example}
						</p>
					</button>
				{/each}
			</div>
		</div>

		<!-- Features -->
		<div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
			<div class="bg-white p-6 rounded-xl border border-gray-200">
				<div class="bg-blue-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
					<Clock class="w-6 h-6 text-blue-600" />
				</div>
				<h3 class="text-lg font-semibold text-gray-900 mb-2">Save Time</h3>
				<p class="text-gray-600 text-sm">
					Smart algorithms find the fastest drive-and-ride combinations, saving you up to 30 minutes per trip.
				</p>
			</div>

			<div class="bg-white p-6 rounded-xl border border-gray-200">
				<div class="bg-green-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
					<DollarSign class="w-6 h-6 text-green-600" />
				</div>
				<h3 class="text-lg font-semibold text-gray-900 mb-2">Save Money</h3>
				<p class="text-gray-600 text-sm">
					Compare costs across parking, gas, and transit. Find the most economical route to your destination.
				</p>
			</div>

			<div class="bg-white p-6 rounded-xl border border-gray-200">
				<div class="bg-emerald-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
					<Leaf class="w-6 h-6 text-emerald-600" />
				</div>
				<h3 class="text-lg font-semibold text-gray-900 mb-2">Reduce Carbon</h3>
				<p class="text-gray-600 text-sm">
					See your carbon savings by choosing multi-modal transit over driving the entire way.
				</p>
			</div>
		</div>

		<!-- How It Works -->
		<div class="bg-gradient-to-r from-primary-500 to-cyan-600 rounded-2xl p-8 text-white">
			<h3 class="text-2xl font-bold mb-6 text-center">How Beeline Works</h3>
			<div class="grid grid-cols-1 md:grid-cols-4 gap-6">
				<div class="text-center">
					<div class="bg-white/20 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3 text-xl font-bold">
						1
					</div>
					<h4 class="font-semibold mb-2">Describe Your Trip</h4>
					<p class="text-sm text-blue-50">Tell us where and when you need to go in plain English</p>
				</div>
				<div class="text-center">
					<div class="bg-white/20 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3 text-xl font-bold">
						2
					</div>
					<h4 class="font-semibold mb-2">AI Plans Routes</h4>
					<p class="text-sm text-blue-50">Our AI finds optimal park-and-ride combinations</p>
				</div>
				<div class="text-center">
					<div class="bg-white/20 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3 text-xl font-bold">
						3
					</div>
					<h4 class="font-semibold mb-2">Compare Options</h4>
					<p class="text-sm text-blue-50">View 1-3 routes with time, cost, and environmental impact</p>
				</div>
				<div class="text-center">
					<div class="bg-white/20 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3 text-xl font-bold">
						4
					</div>
					<h4 class="font-semibold mb-2">Hit the Road</h4>
					<p class="text-sm text-blue-50">Follow your optimized route with confidence</p>
				</div>
			</div>
		</div>
	</main>

	<!-- Footer -->
	<footer class="bg-white border-t border-gray-200 mt-16">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
			<p class="text-center text-gray-600 text-sm">
				Built with Claude AI, OpenStreetMap, and 511.org Transit Data
			</p>
		</div>
	</footer>
</div>

<style>
	.line-clamp-2 {
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
		overflow: hidden;
	}
</style>
