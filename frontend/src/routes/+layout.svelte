<script lang="ts">
	import '../app.css';
	import ChatBubble from '../lib/components/ChatBubble.svelte';
	import { chatWithAssistant } from '$lib/services/api';
	import { routeResponse, filters } from '$lib/stores/routeStore';

	async function handleChatMessage(message: string): Promise<string> {
		try {
			// Prepare context with current route and filter state
			const context = {
				hasRoutes: $routeResponse !== null,
				currentFilters: $filters,
				routeCount: $routeResponse?.routes?.length || 0
			};

			// Call the backend chat API
			const response = await chatWithAssistant(message, context);
			return response;
		} catch (error) {
			console.error('Chat error:', error);
			return "Sorry, I'm having trouble connecting right now. Please try again in a moment.";
		}
	}
</script>

<div>
	<slot />
	<ChatBubble onSendMessage={handleChatMessage} />
</div>
