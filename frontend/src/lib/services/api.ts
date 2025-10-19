import { env } from '$env/dynamic/public';
import type { ParsedQuery, RouteResponse } from '$lib/types';
import { generateMockRoutes } from './mockData';

const LLM_API_URL = env.PUBLIC_LLM_API_URL || 'http://localhost:8000';
const PLANNER_API_URL = env.PUBLIC_PLANNER_API_URL || 'http://localhost:8001';
const MOCK_MODE = env.PUBLIC_MOCK_MODE === 'true';

/**
 * Search for routes using natural language query
 * This calls the combined /api/search endpoint that handles both parsing and route planning
 */
export async function searchRoutes(query: string): Promise<RouteResponse> {
	if (MOCK_MODE) {
		// Simulate API delay
		await new Promise((resolve) => setTimeout(resolve, 1500));
		return generateMockRoutes(query);
	}

	try {
		const response = await fetch(`${LLM_API_URL}/api/search`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ query })
		});

		if (!response.ok) {
			const errorData = await response.text();
			console.error('API error:', errorData);
			throw new Error(`API service error: ${response.statusText}`);
		}

		return await response.json();
	} catch (error) {
		console.error('Failed to search routes:', error);
		throw new Error('Unable to parse your query. Please try again.');
	}
}

/**
 * Chat with the LLM assistant about routes and preferences
 */
export async function chatWithAssistant(message: string, context?: any): Promise<{ response: string; action?: any }> {
	if (MOCK_MODE) {
		// Mock response
		await new Promise((resolve) => setTimeout(resolve, 500));
		return { response: "I can help you with that! (Mock mode - connect to real API for actual assistance)" };
	}

	try {
		const response = await fetch(`${LLM_API_URL}/api/chat`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ message, context: context || {} })
		});

		if (!response.ok) {
			const errorData = await response.text();
			console.error('Chat API error:', errorData);
			throw new Error(`Chat API error: ${response.statusText}`);
		}

		const data = await response.json();
		return {
			response: data.response,
			action: data.action
		};
	} catch (error) {
		console.error('Failed to chat with assistant:', error);
		throw new Error('Unable to reach the assistant. Please try again.');
	}
}

/**
 * Health check for backend API service
 */
export async function checkAPIHealth(): Promise<boolean> {
	if (MOCK_MODE) return true;

	try {
		const response = await fetch(`${LLM_API_URL}/`);
		return response.ok;
	} catch {
		return false;
	}
}
