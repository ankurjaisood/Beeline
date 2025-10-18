<script lang="ts">
	import { SlidersHorizontal, X } from 'lucide-svelte';
	import { filters } from '$lib/stores/routeStore';
	import type { OptimizationPreference } from '$lib/types';

	export let isOpen: boolean = false;

	function toggleOpen() {
		isOpen = !isOpen;
	}

	function updateOptimization(value: OptimizationPreference) {
		filters.update(f => ({ ...f, optimize: value }));
	}
</script>

<div class="bg-white border border-gray-200 rounded-lg shadow-sm">
	<!-- Header -->
	<button
		on:click={toggleOpen}
		class="w-full flex items-center justify-between p-4 hover:bg-gray-50 transition-colors"
	>
		<div class="flex items-center gap-2">
			<SlidersHorizontal class="w-5 h-5 text-gray-600" />
			<span class="font-semibold text-gray-900">Filters & Preferences</span>
		</div>
		<div class="transform transition-transform {isOpen ? 'rotate-180' : ''}">
			<svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
			</svg>
		</div>
	</button>

	{#if isOpen}
		<div class="p-4 pt-0 space-y-4 border-t border-gray-200">
			<!-- Optimization Preference -->
			<div>
				<label class="block text-sm font-medium text-gray-700 mb-2">Optimize for:</label>
				<div class="grid grid-cols-2 gap-2">
					{#each ['time', 'cost', 'convenience', 'environmental'] as opt}
						<button
							on:click={() => updateOptimization(opt)}
							class="px-3 py-2 text-sm rounded-lg border-2 transition-all {$filters.optimize === opt
								? 'border-primary-500 bg-primary-50 text-primary-700 font-semibold'
								: 'border-gray-200 hover:border-gray-300 text-gray-700'}"
						>
							{opt.charAt(0).toUpperCase() + opt.slice(1)}
						</button>
					{/each}
				</div>
			</div>

			<!-- Transportation Modes -->
			<div>
				<label class="block text-sm font-medium text-gray-700 mb-2">Transportation modes:</label>
				<div class="space-y-2">
					<label class="flex items-center gap-2 cursor-pointer">
						<input
							type="checkbox"
							bind:checked={$filters.modes.driving}
							class="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
						/>
						<span class="text-sm text-gray-700">Driving</span>
					</label>
					<label class="flex items-center gap-2 cursor-pointer">
						<input
							type="checkbox"
							bind:checked={$filters.modes.transit}
							class="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
						/>
						<span class="text-sm text-gray-700">Public Transit</span>
					</label>
					<label class="flex items-center gap-2 cursor-pointer">
						<input
							type="checkbox"
							bind:checked={$filters.modes.rideshare}
							class="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
						/>
						<span class="text-sm text-gray-700">Rideshare (Uber, Lyft, Waymo)</span>
					</label>
					<label class="flex items-center gap-2 cursor-pointer">
						<input
							type="checkbox"
							bind:checked={$filters.modes.micromobility}
							class="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
						/>
						<span class="text-sm text-gray-700">Walking / Biking</span>
					</label>
				</div>
			</div>

			<!-- Constraints -->
			<div>
				<label class="block text-sm font-medium text-gray-700 mb-2">
					Max walking distance: {$filters.maxWalkingDistance} mi
				</label>
				<input
					type="range"
					min="0.25"
					max="2"
					step="0.25"
					bind:value={$filters.maxWalkingDistance}
					class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
				/>
			</div>

			<div>
				<label class="flex items-center gap-2 cursor-pointer">
					<input
						type="checkbox"
						bind:checked={$filters.avoidTolls}
						class="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
					/>
					<span class="text-sm text-gray-700">Avoid tolls</span>
				</label>
			</div>

			<div>
				<label class="flex items-center gap-2 cursor-pointer">
					<input
						type="checkbox"
						bind:checked={$filters.accessible}
						class="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
					/>
					<span class="text-sm text-gray-700">Wheelchair accessible routes only</span>
				</label>
			</div>
		</div>
	{/if}
</div>
