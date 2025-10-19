<script lang="ts">
	import '../app.css';
	import ChatBubble from '../lib/components/ChatBubble.svelte';
	import { chatWithAssistant, searchRoutes } from '$lib/services/api';
	import { routeResponse, filters, selectedRoute, sortedRoutes, isLoading, error } from '$lib/stores/routeStore';
	import { goto } from '$app/navigation';

	async function handleChatMessage(message: string): Promise<{ response: string; action?: any }> {
		try {
			// Prepare comprehensive context with current route and filter state
			const context = {
				// Query information
				query: $routeResponse ? {
					origin: $routeResponse.query.origin,
					destination: $routeResponse.query.destination,
					arrival_time: $routeResponse.query.arrival_time
				} : null,

				// Available routes
				routes: $sortedRoutes.map(route => ({
					id: route.id,
					summary: route.summary,
					total_duration: route.total_duration,
					total_cost: route.total_cost,
					time_savings: route.time_savings,
					carbon_savings: route.carbon_savings,
					legs: route.legs.map(leg => ({
						mode: leg.mode,
						from: leg.from,
						to: leg.to,
						duration: leg.duration,
						distance: leg.distance,
						cost: leg.cost
					}))
				})),

				// Currently selected route
				selectedRoute: $selectedRoute ? {
					id: $selectedRoute.id,
					summary: $selectedRoute.summary,
					total_duration: $selectedRoute.total_duration,
					total_cost: $selectedRoute.total_cost
				} : null,

				// Current filters
				filters: {
					modes: $filters.modes,
					optimize: $filters.optimize,
					maxCost: $filters.maxCost,
					maxWalkingDistance: $filters.maxWalkingDistance,
					avoidTolls: $filters.avoidTolls,
					accessible: $filters.accessible
				}
			};

			// Call the backend chat API
			const result = await chatWithAssistant(message, context);
			return result;
		} catch (err) {
			console.error('Chat error:', err);
			return {
				response: "Sorry, I'm having trouble connecting right now. Please try again in a moment."
			};
		}
	}

	async function handleExecuteAction(action: any) {
		if (!action) return;

		if (action.type === 'search') {
			// Execute the search
			isLoading.set(true);
			error.set(null);

			try {
				const response = await searchRoutes(action.query);
				routeResponse.set(response);

				// Navigate to home page if not already there
				goto('/');
			} catch (err) {
				error.set(err instanceof Error ? err.message : 'An error occurred');
			} finally {
				isLoading.set(false);
			}
		}
	}
</script>

<div>
	<slot />
	<ChatBubble onSendMessage={handleChatMessage} onExecuteAction={handleExecuteAction} />
</div>
