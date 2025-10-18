import { env } from '$env/dynamic/public';
import type { ParsedQuery, RouteResponse } from '$lib/types';
import { generateMockRoutes } from './mockData';

const LLM_API_URL = env.PUBLIC_LLM_API_URL || 'http://localhost:8000';
const PLANNER_API_URL = env.PUBLIC_PLANNER_API_URL || 'http://localhost:8001';
const MOCK_MODE = env.PUBLIC_MOCK_MODE === 'true';

/**
 * Parse a natural language query using the LLM service
 */
export async function parseQuery(query: string): Promise<ParsedQuery> {
	if (MOCK_MODE) {
		// Simulate API delay
		await new Promise((resolve) => setTimeout(resolve, 800));
		return generateMockRoutes(query).query;
	}

	try {
		const response = await fetch(`${LLM_API_URL}/parse-query`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ query })
		});

		if (!response.ok) {
			throw new Error(`LLM service error: ${response.statusText}`);
		}

		return await response.json();
	} catch (error) {
		console.error('Failed to parse query:', error);
		throw new Error('Unable to parse your query. Please try again.');
	}
}

/**
 * Get route options from the backend planner
 */
export async function getRoutes(parsedQuery: ParsedQuery): Promise<RouteResponse> {
	if (MOCK_MODE) {
		// Simulate API delay for route calculation
		await new Promise((resolve) => setTimeout(resolve, 1500));
		// Use the origin/destination to determine which mock to return
		const mockQuery = `${parsedQuery.origin} to ${parsedQuery.destination}`;
		return generateMockRoutes(mockQuery);
	}

	try {
		const response = await fetch(`${PLANNER_API_URL}/plan-route`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(parsedQuery)
		});

		if (!response.ok) {
			throw new Error(`Backend planner error: ${response.statusText}`);
		}

		return await response.json();
	} catch (error) {
		console.error('Failed to get routes:', error);
		throw new Error('Unable to calculate routes. Please try again.');
	}
}

/**
 * Combined query: parse natural language and get routes
 */
export async function searchRoutes(query: string): Promise<RouteResponse> {
	const parsedQuery = await parseQuery(query);
	return await getRoutes(parsedQuery);
}

/**
 * Health check for LLM service
 */
export async function checkLLMHealth(): Promise<boolean> {
	if (MOCK_MODE) return true;

	try {
		const response = await fetch(`${LLM_API_URL}/health`);
		return response.ok;
	} catch {
		return false;
	}
}

/**
 * Health check for backend planner
 */
export async function checkPlannerHealth(): Promise<boolean> {
	if (MOCK_MODE) return true;

	try {
		const response = await fetch(`${PLANNER_API_URL}/health`);
		return response.ok;
	} catch {
		return false;
	}
}
