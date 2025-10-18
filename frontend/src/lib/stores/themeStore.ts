import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export type Theme = 'light' | 'dark';

// Get initial theme from localStorage or system preference
function getInitialTheme(): Theme {
	if (!browser) return 'light';

	const stored = localStorage.getItem('beeline-theme') as Theme | null;
	if (stored) return stored;

	// Check system preference
	if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
		return 'dark';
	}

	return 'light';
}

export const theme = writable<Theme>(getInitialTheme());

// Subscribe to theme changes and update localStorage + document class
if (browser) {
	theme.subscribe(value => {
		localStorage.setItem('beeline-theme', value);
		document.documentElement.classList.toggle('dark', value === 'dark');
	});
}

export function toggleTheme() {
	theme.update(current => current === 'light' ? 'dark' : 'light');
}
