<script lang="ts">
	import { MessageCircle, X, Send, Minimize2, Search } from 'lucide-svelte';
	import { onMount } from 'svelte';

	export let onSendMessage: (message: string) => Promise<{ response: string; action?: any }> = async () => ({ response: '' });
	export let onExecuteAction: (action: any) => void = () => {};

	let isOpen = false;
	let isMinimized = false;
	let message = '';
	let messages: Array<{ role: 'user' | 'assistant'; content: string; action?: any }> = [];
	let chatContainer: HTMLDivElement;
	let isLoading = false;

	function toggleChat() {
		if (isMinimized) {
			isMinimized = false;
		} else {
			isOpen = !isOpen;
			if (isOpen && messages.length === 0) {
				// Welcome message
				messages = [
					{
						role: 'assistant',
						content: "Hi! I'm your Beeline assistant. Ask me to modify your route, change preferences, or find alternative options!"
					}
				];
			}
		}
	}

	function minimizeChat() {
		isMinimized = true;
	}

	async function sendMessage() {
		if (!message.trim()) return;

		const userMessage = message.trim();
		message = '';

		// Add user message
		messages = [...messages, { role: 'user', content: userMessage }];

		// Scroll to bottom
		setTimeout(() => {
			if (chatContainer) {
				chatContainer.scrollTop = chatContainer.scrollHeight;
			}
		}, 10);

		// Show loading
		isLoading = true;

		try {
			// Get AI response
			const result = await onSendMessage(userMessage);

			// Add assistant message with optional action
			messages = [...messages, {
				role: 'assistant',
				content: result.response,
				action: result.action
			}];
		} catch (error) {
			messages = [
				...messages,
				{ role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }
			];
		} finally {
			isLoading = false;

			// Scroll to bottom
			setTimeout(() => {
				if (chatContainer) {
					chatContainer.scrollTop = chatContainer.scrollHeight;
				}
			}, 10);
		}
	}

	function handleKeyPress(event: KeyboardEvent) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			sendMessage();
		}
	}
</script>

<!-- Chat Bubble Button -->
{#if !isOpen || isMinimized}
	<button
		on:click={toggleChat}
		class="fixed bottom-6 right-6 w-14 h-14 bg-primary-600 hover:bg-primary-700 text-white rounded-full shadow-lg hover:shadow-xl transition-all z-50 flex items-center justify-center group"
		aria-label="Open chat"
	>
		<MessageCircle class="w-6 h-6 group-hover:scale-110 transition-transform" />
	</button>
{/if}

<!-- Chat Window -->
{#if isOpen && !isMinimized}
	<div
		class="fixed bottom-6 right-6 w-96 bg-white dark:bg-gray-800 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-700 flex flex-col overflow-hidden z-[9999] transition-all h-[60vh]"
	>
		<!-- Header -->
		<div
			class="bg-primary-600 dark:bg-primary-700 text-white px-4 py-3 flex items-center justify-between cursor-pointer"
			on:click={() => isMinimized && (isMinimized = false)}
			on:keypress={(e) => e.key === 'Enter' && isMinimized && (isMinimized = false)}
			role="button"
			tabindex="0"
		>
			<div class="flex items-center gap-2">
				<div class="w-2 h-2 bg-green-400 rounded-full" />
				<span class="font-semibold">Beeline Assistant</span>
			</div>
			<div class="flex items-center gap-2">
				<button
					on:click|stopPropagation={minimizeChat}
					class="p-1 hover:bg-primary-700 dark:hover:bg-primary-600 rounded transition-colors"
					aria-label="Minimize chat"
				>
					<Minimize2 class="w-4 h-4" />
				</button>
				<button
					on:click|stopPropagation={toggleChat}
					class="p-1 hover:bg-primary-700 dark:hover:bg-primary-600 rounded transition-colors"
					aria-label="Close chat"
				>
					<X class="w-4 h-4" />
				</button>
			</div>
		</div>

		{#if !isMinimized}
			<!-- Messages -->
			<div
				bind:this={chatContainer}
				class="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50 dark:bg-gray-900"
			>
				{#each messages as msg}
					<div class="flex {msg.role === 'user' ? 'justify-end' : 'justify-start'} flex-col {msg.role === 'assistant' ? 'items-start' : 'items-end'} gap-2">
						<div
							class="max-w-[80%] rounded-2xl px-3 py-1.5 {msg.role === 'user'
								? 'bg-primary-600 text-white'
								: 'bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 border border-gray-200 dark:border-gray-700'}"
						>
							<p class="text-xs whitespace-pre-wrap">{msg.content}</p>
						</div>

						<!-- Action Button -->
						{#if msg.role === 'assistant' && msg.action}
							<button
								on:click={() => onExecuteAction(msg.action)}
								class="flex items-center gap-2 px-3 py-1.5 bg-primary-600 hover:bg-primary-700 text-white rounded-lg text-xs font-medium transition-colors shadow-sm"
							>
								<Search class="w-3 h-3" />
								Search with these criteria
							</button>
						{/if}
					</div>
				{/each}

				{#if isLoading}
					<div class="flex justify-start">
						<div
							class="max-w-[80%] rounded-2xl px-4 py-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700"
						>
							<div class="flex items-center gap-2">
								<div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
								<div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s" />
								<div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s" />
							</div>
						</div>
					</div>
				{/if}
			</div>

			<!-- Input -->
			<div class="p-3 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
				<div class="flex gap-2">
					<input
						type="text"
						bind:value={message}
						on:keypress={handleKeyPress}
						placeholder="Ask me anything..."
						class="flex-1 px-3 py-1.5 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 text-xs"
						disabled={isLoading}
					/>
					<button
						on:click={sendMessage}
						disabled={!message.trim() || isLoading}
						class="px-3 py-1.5 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-300 dark:disabled:bg-gray-600 text-white rounded-lg transition-colors flex items-center justify-center"
						aria-label="Send message"
					>
						<Send class="w-4 h-4" />
					</button>
				</div>
				<p class="text-xs text-gray-500 dark:text-gray-400 mt-2">
					Try: "Which route is fastest?" or "Compare the costs" or "What's the greenest option?"
				</p>
			</div>
		{/if}
	</div>
{/if}

<style>
	@keyframes bounce {
		0%,
		100% {
			transform: translateY(0);
		}
		50% {
			transform: translateY(-4px);
		}
	}

	.animate-bounce {
		animation: bounce 1s infinite;
	}
</style>
