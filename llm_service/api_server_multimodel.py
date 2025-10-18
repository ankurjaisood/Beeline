import os
import logging
from typing import Optional
from datetime import datetime
import anthropic
import google.generativeai as genai
import googlemaps
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Beeline API (Multi-Model)", version="2.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))

# Initialize LLM clients
claude_client = None
gemini_model = None

if os.getenv('ANTHROPIC_API_KEY'):
    claude_client = anthropic.Client(api_key=os.getenv('ANTHROPIC_API_KEY'))
    logger.info("Claude API initialized")

if os.getenv('GEMINI_API_KEY'):
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    # Using gemini-2.5-flash-lite for ultra-fast responses (optimized for low latency)
    # Alternatives: 'gemini-2.5-flash' (balanced) or 'gemini-2.0-flash-exp' (experimental)
    gemini_model = genai.GenerativeModel('gemini-2.5-flash-lite')
    logger.info("Gemini API initialized with gemini-2.5-flash-lite")

class SearchRequest(BaseModel):
    query: str
    model: str = "auto"  # "claude", "gemini", or "auto"

class SearchResponse(BaseModel):
    query: dict
    routes: list
    metadata: dict

@app.get("/")
async def root():
    """Health check endpoint."""
    available_models = []
    if claude_client:
        available_models.append("claude")
    if gemini_model:
        available_models.append("gemini")

    return {
        "status": "ok",
        "service": "Beeline API (Multi-Model)",
        "available_models": available_models
    }

@app.post("/api/search", response_model=SearchResponse)
async def search_routes(request: SearchRequest):
    """
    Process a natural language query and return route options.
    Supports multiple LLM models.
    """
    try:
        logger.info(f"Processing query with model={request.model}: {request.query}")

        # Determine which model to use
        model_choice = request.model
        if model_choice == "auto":
            # Prefer Gemini (free), fallback to Claude
            if gemini_model:
                model_choice = "gemini"
            elif claude_client:
                model_choice = "claude"
            else:
                raise HTTPException(status_code=503, detail="No LLM models available")

        # Create planner with selected model
        if model_choice == "gemini":
            if not gemini_model:
                raise HTTPException(status_code=503, detail="Gemini not available")
            planner = RoutePlanner(gemini_model, gmaps, model_type="gemini")
        elif model_choice == "claude":
            if not claude_client:
                raise HTTPException(status_code=503, detail="Claude not available")
            planner = RoutePlanner(claude_client, gmaps, model_type="claude")
        else:
            raise HTTPException(status_code=400, detail=f"Unknown model: {model_choice}")

        # Plan routes
        result = await planner.plan_routes(request.query)
        result['metadata']['model_used'] = model_choice

        logger.info(f"Generated {len(result['routes'])} routes using {model_choice}")
        return SearchResponse(**result)

    except Exception as e:
        logger.exception(f"Error processing search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class RoutePlanner:
    """Plans multi-modal routes using LLM (Claude or Gemini) and Google Maps."""

    def __init__(self, llm_client, gmaps_client, model_type="claude"):
        self.llm = llm_client
        self.gmaps = gmaps_client
        self.model_type = model_type

    async def plan_routes(self, query: str) -> dict:
        """Use LLM to parse query, get map data, and generate route options."""
        # Parse query
        parsed_query = await self._parse_query_with_llm(query)

        # Get Google Maps data
        maps_data = await self._get_maps_data(parsed_query)

        # Generate routes
        routes = await self._generate_routes_with_llm(parsed_query, maps_data)

        # Enrich routes with coordinates from Google Maps
        enriched_routes = await self._enrich_routes_with_coords(routes, maps_data)

        # Log to verify coordinates are added
        if enriched_routes and len(enriched_routes) > 0:
            first_route = enriched_routes[0]
            if "legs" in first_route and len(first_route["legs"]) > 0:
                first_leg = first_route["legs"][0]
                has_coords = "from_coords" in first_leg and "to_coords" in first_leg
                logger.info(f"Route enrichment: First leg has coordinates: {has_coords}")
                if has_coords:
                    logger.info(f"Sample coords: from={first_leg['from_coords']}, to={first_leg['to_coords']}")

        return {
            "query": parsed_query,
            "routes": enriched_routes,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "query_text": query
            }
        }

    async def _call_llm(self, prompt: str) -> str:
        """Call the appropriate LLM based on model_type."""
        try:
            if self.model_type == "claude":
                response = self.llm.messages.create(
                    model="claude-3-5-sonnet-20250219",
                    max_tokens=2000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()

            elif self.model_type == "gemini":
                response = self.llm.generate_content(prompt)
                return response.text.strip()

            else:
                raise ValueError(f"Unknown model type: {self.model_type}")

        except Exception as e:
            logger.warning(f"{self.model_type} call failed: {e}")
            raise

    async def _parse_query_with_llm(self, query: str) -> dict:
        """Use LLM to extract structured information from natural language query."""

        prompt = f"""Parse this transit query and extract the key information as JSON.

Query: "{query}"

Extract and return ONLY a JSON object (no markdown, no explanation) with these fields:
- origin: starting location (REQUIRED - must be a valid location name as a string, NEVER use null/None)
- destination: ending location (REQUIRED - must be a valid location name as a string, NEVER use null/None)
- waypoints: array of intermediate stops (empty array [] if none mentioned)
- arrival_time: target arrival time (string in 24h format like "10:00", or empty string "" if not mentioned)
- preferences: array of user preferences (empty array [] if none)
- constraints: array of constraints (empty array [] if none)

CRITICAL RULES:
1. origin MUST be a non-empty string (e.g., "San Jose", "Current location", "Palo Alto")
2. destination MUST be a non-empty string (e.g., "San Francisco", "Salesforce Tower")
3. If origin is not stated, use "Current location" or infer from context
4. If destination is not clear, use the most prominent location mentioned
5. NEVER use null, None, or empty string for origin or destination

Example 1:
Query: "Get me from San Jose to Salesforce Tower by 10 am"
Output: {{"origin": "San Jose", "destination": "Salesforce Tower", "waypoints": [], "arrival_time": "10:00", "preferences": [], "constraints": ["arrive by 10am"]}}

Example 2:
Query: "I need to get to Oracle Park by 7pm"
Output: {{"origin": "Current location", "destination": "Oracle Park", "waypoints": [], "arrival_time": "19:00", "preferences": [], "constraints": ["arrive by 7pm"]}}

Return only the JSON object, nothing else."""

        try:
            content = await self._call_llm(prompt)

            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()

            parsed = json.loads(content)

            # Validate required fields
            if not parsed.get("origin") or parsed.get("origin") in [None, "None", "null"]:
                logger.warning(f"Invalid origin in parsed query: {parsed.get('origin')}")
                raise ValueError("Origin is required but was not found in query")

            if not parsed.get("destination") or parsed.get("destination") in [None, "None", "null"]:
                logger.warning(f"Invalid destination in parsed query: {parsed.get('destination')}")
                raise ValueError("Destination is required but was not found in query")

            logger.info(f"Parsed query with {self.model_type}: {parsed}")
            return parsed

        except Exception as e:
            logger.warning(f"LLM parsing failed: {e}")
            # Try to extract basic info from query
            query_lower = query.lower()

            # Return error if we can't parse
            raise ValueError(f"Unable to parse query. Please specify both origin and destination clearly. Error: {e}")

    async def _get_maps_data(self, parsed_query: dict) -> dict:
        """Get route data from Google Maps APIs."""
        try:
            origin = parsed_query.get("origin", "")
            destination = parsed_query.get("destination", "")

            # Geocode
            origin_geocode = self.gmaps.geocode(origin)
            dest_geocode = self.gmaps.geocode(destination)

            if not origin_geocode or not dest_geocode:
                raise ValueError("Could not geocode origin or destination")

            # Get directions
            now = datetime.now()
            driving_directions = self.gmaps.directions(origin, destination, mode="driving", departure_time=now)
            transit_directions = self.gmaps.directions(origin, destination, mode="transit", departure_time=now)

            return {
                "origin_geocode": origin_geocode[0],
                "destination_geocode": dest_geocode[0],
                "driving_route": driving_directions[0] if driving_directions else None,
                "transit_route": transit_directions[0] if transit_directions else None
            }

        except Exception as e:
            logger.exception(f"Error getting maps data: {e}")
            return {}

    async def _generate_routes_with_llm(self, parsed_query: dict, maps_data: dict) -> list:
        """Use LLM to generate optimal route options based on maps data."""

        origin = parsed_query.get("origin", "Unknown")
        destination = parsed_query.get("destination", "Unknown")
        waypoints = parsed_query.get("waypoints", [])
        preferences = parsed_query.get("preferences", [])

        driving_route = maps_data.get("driving_route", {})
        transit_route = maps_data.get("transit_route", {})

        # Extract route details
        if driving_route and "legs" in driving_route:
            drive_leg = driving_route["legs"][0]
            drive_duration = drive_leg.get("duration", {}).get("value", 0) // 60
            drive_distance = drive_leg.get("distance", {}).get("value", 0) / 1609.34
        else:
            drive_duration = 30
            drive_distance = 20.0

        if transit_route and "legs" in transit_route:
            transit_leg = transit_route["legs"][0]
            transit_duration = transit_leg.get("duration", {}).get("value", 0) // 60
            transit_distance = transit_leg.get("distance", {}).get("value", 0) / 1609.34
        else:
            transit_duration = 45
            transit_distance = 15.0

        available_modes = ["drive", "transit", "walk", "rideshare", "bikeshare"]

        prompt = f"""You are an AI assistant that helps users navigate multi-modally.
You can split the trip into legs where each leg uses a dedicated mode.

Optimize:
1. Reduce the number of transfers
2. Reduce the overall walking time
3. Reduce the overall trip time
4. Use transit to go as far as possible without transfers
5. Consider ride sharing or bike sharing for first/last mile
6. When driving suggest the best and lowest cost parking options. Only suggest driving if it is the first leg of a trip.

The user's ask is to plan a path using the following information:

start_address={origin}
end_address={destination}
waypoint_addresses={waypoints if waypoints else []}
modes={available_modes}

Available route data:
- Full driving route: {drive_duration} min, {drive_distance:.1f} miles
- Full transit route: {transit_duration} min, {transit_distance:.1f} miles
- User preferences: {', '.join(preferences) if preferences else 'none specified'}

Generate 2-3 optimal multi-modal route options. Return ONLY a JSON array (no markdown, no explanation) with this structure:
[
  {{
    "id": "route_1",
    "summary": "Brief description of the route",
    "total_duration": 65,
    "total_cost": 12.50,
    "time_savings": 15,
    "carbon_savings": 8.5,
    "legs": [
      {{
        "mode": "drive",
        "from": "{origin}",
        "to": "Transit Station Name",
        "duration": 25,
        "distance": 15.0,
        "cost": 0,
        "details": {{
          "traffic_level": "moderate",
          "parking_cost": 5.50,
          "parking_availability": 75
        }}
      }},
      {{
        "mode": "transit",
        "from": "Transit Station Name",
        "to": "{destination}",
        "duration": 35,
        "distance": 18.0,
        "cost": 7.00,
        "details": {{
          "line": "Transit Line Name",
          "stops": 8
        }}
      }}
    ]
  }}
]

Remember: Only use driving as the first leg. Optimize for fewer transfers and minimal walking."""

        try:
            content = await self._call_llm(prompt)

            # Remove markdown if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()

            routes = json.loads(content)
            logger.info(f"Generated {len(routes)} routes with {self.model_type}")
            return routes

        except Exception as e:
            logger.warning(f"Route generation failed: {e}, using fallback")
            return self._create_fallback_routes(origin, destination, drive_duration, drive_distance)

    def _create_fallback_routes(self, origin: str, destination: str, drive_duration: int, drive_distance: float) -> list:
        """Create sample routes if LLM fails."""
        return [
            {
                "id": "route_1",
                "summary": f"Drive to nearest transit hub, then take transit to {destination}",
                "total_duration": int(drive_duration * 0.6 + 35),
                "total_cost": 12.50,
                "time_savings": 10,
                "carbon_savings": 6.5,
                "legs": [
                    {
                        "mode": "drive",
                        "from": origin,
                        "to": "Transit Hub",
                        "duration": int(drive_duration * 0.6),
                        "distance": drive_distance * 0.6,
                        "cost": 0,
                        "details": {
                            "traffic_level": "light",
                            "parking_cost": 5.00,
                            "parking_availability": 80
                        }
                    },
                    {
                        "mode": "transit",
                        "from": "Transit Hub",
                        "to": destination,
                        "duration": 35,
                        "distance": drive_distance * 0.4,
                        "cost": 7.50,
                        "details": {
                            "line": "Express Transit",
                            "stops": 5
                        }
                    }
                ]
            }
        ]

    async def _enrich_routes_with_coords(self, routes: list, maps_data: dict) -> list:
        """Add coordinates to route legs by geocoding the locations."""
        enriched_routes = []

        # Cache to avoid redundant geocoding calls
        geocode_cache = {}

        for route in routes:
            enriched_route = route.copy()
            enriched_legs = []

            for leg in route.get("legs", []):
                enriched_leg = leg.copy()

                # Geocode the from and to locations
                try:
                    from_location = leg.get("from", "")
                    to_location = leg.get("to", "")

                    # Use cache to avoid duplicate API calls
                    if from_location not in geocode_cache:
                        from_geocode = self.gmaps.geocode(from_location)
                        geocode_cache[from_location] = from_geocode
                    else:
                        from_geocode = geocode_cache[from_location]

                    if to_location not in geocode_cache:
                        to_geocode = self.gmaps.geocode(to_location)
                        geocode_cache[to_location] = to_geocode
                    else:
                        to_geocode = geocode_cache[to_location]

                    if from_geocode and len(from_geocode) > 0:
                        from_coords = from_geocode[0]["geometry"]["location"]
                        enriched_leg["from_coords"] = {
                            "lat": from_coords["lat"],
                            "lng": from_coords["lng"]
                        }

                    if to_geocode and len(to_geocode) > 0:
                        to_coords = to_geocode[0]["geometry"]["location"]
                        enriched_leg["to_coords"] = {
                            "lat": to_coords["lat"],
                            "lng": to_coords["lng"]
                        }

                    # Skip polyline fetching to speed up response
                    # Frontend can draw straight lines between coordinates
                    # Uncomment below if you need actual route polylines
                    """
                    if "from_coords" in enriched_leg and "to_coords" in enriched_leg:
                        try:
                            directions = self.gmaps.directions(
                                from_location,
                                to_location,
                                mode="driving" if leg.get("mode") == "drive" else "transit"
                            )
                            if directions and len(directions) > 0:
                                polyline = directions[0].get("overview_polyline", {}).get("points", "")
                                if polyline:
                                    enriched_leg["polyline"] = polyline
                        except Exception as e:
                            logger.warning(f"Could not get polyline for leg: {e}")
                    """

                except Exception as e:
                    logger.warning(f"Could not geocode locations for leg {leg.get('from')} -> {leg.get('to')}: {e}")

                enriched_legs.append(enriched_leg)

            enriched_route["legs"] = enriched_legs
            enriched_routes.append(enriched_route)

        return enriched_routes

def main():
    """Main function to run the API server."""
    try:
        # Check required environment variables
        if not os.getenv('GOOGLE_MAPS_API_KEY'):
            raise ValueError("Missing GOOGLE_MAPS_API_KEY environment variable")

        # Check for at least one LLM API key
        has_llm = False
        if os.getenv('ANTHROPIC_API_KEY'):
            logger.info("✓ Claude API available")
            has_llm = True
        if os.getenv('GEMINI_API_KEY'):
            logger.info("✓ Gemini API available")
            has_llm = True

        if not has_llm:
            logger.warning("⚠️  No LLM API keys found. Set ANTHROPIC_API_KEY or GEMINI_API_KEY")
            logger.warning("⚠️  Server will start but LLM features will be unavailable")

        logger.info("Starting Beeline Multi-Model API Server")
        logger.info("Endpoints: POST /api/search")

        # Start the FastAPI server
        uvicorn.run(app, host="0.0.0.0", port=8000)
        return 0

    except Exception as e:
        logger.exception("Server error: %s", e)
        return 1

if __name__ == "__main__":
    exit(main())
