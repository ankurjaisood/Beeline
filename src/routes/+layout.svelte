<script lang="ts">
	import '../app.css';
	import ChatBubble from '../lib/components/ChatBubble.svelte';

	async function handleChatMessage(message: string): Promise<string> {
		// TODO: Connect to LLM service for route modifications
		// For now, return a placeholder response
		await new Promise(resolve => setTimeout(resolve, 1000));

		if (message.toLowerCase().includes('cheaper')) {
			return "I can help you find cheaper options! Try filtering by 'Cheapest' in the sidebar, or I can search for routes with less expensive parking options.";
		} else if (message.toLowerCase().includes('faster')) {
			return "Looking for faster routes? Click the 'Fastest' filter on the left to see the quickest options. I can also suggest routes with express transit services.";
		} else if (message.toLowerCase().includes('bart') || message.toLowerCase().includes('caltrain')) {
			return "I can adjust your route preferences! Would you like me to show only routes using that transit system? Just let me know your preferences.";
		} else {
			return "I can help you modify your route! Try asking about:\n• Cheaper options\n• Faster routes\n• Different transit systems (BART, Caltrain)\n• Avoiding certain modes of transport";
		}
	}
</script>

<div>
	<slot />
	<ChatBubble onSendMessage={handleChatMessage} />
</div>
