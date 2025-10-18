import os
import logging
from typing import Optional
from datetime import datetime
import anthropic
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
app = FastAPI(title="Beeline API", version="1.0.0")

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))
claude_client = anthropic.Client(api_key=os.getenv('ANTHROPIC_API_KEY'))

class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    query: dict
    routes: list
    metadata: dict

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "Beeline API"}

@app.post("/api/search", response_model=SearchResponse)
async def search_routes(request: SearchRequest):
    """
    Process a natural language query and return route options.

    This endpoint:
    1. Uses Claude to parse the query and extract trip details
    2. Uses Google Maps APIs via MCP-style tools for route data
    3. Plans optimal drive+transit combinations
    4. Returns structured route options for the frontend
    """
    try:
        logger.info(f"Processing query: {request.query}")

        # Step 1: Use Claude to understand the query and plan routes
        planner = RoutePlanner(claude_client, gmaps)
        result = await planner.plan_routes(request.query)

        logger.info(f"Generated {len(result['routes'])} route options")
        return SearchResponse(**result)

    except Exception as e:
        logger.exception(f"Error processing search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class RoutePlanner:
    """Plans multi-modal routes using Claude LLM and Google Maps."""

    def __init__(self, claude_client: anthropic.Client, gmaps_client: googlemaps.Client):
        self.claude = claude_client
        self.gmaps = gmaps_client

    async def plan_routes(self, query: str) -> dict:
        """
        Use Claude to parse query, get map data, and generate route options.
        """
        # Step 1: Parse query with Claude
        parsed_query = await self._parse_query_with_claude(query)

        # Step 2: Get Google Maps data for the route
        maps_data = await self._get_maps_data(parsed_query)

        # Step 3: Generate route options with Claude
        routes = await self._generate_routes_with_claude(parsed_query, maps_data)

        return {
            "query": parsed_query,
            "routes": routes,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "query_text": query
            }
        }

    async def _parse_query_with_claude(self, query: str) -> dict:
        """Use Claude to extract structured information from natural language query."""

        prompt = f"""Parse this transit query and extract the key information as JSON.

Query: "{query}"

Extract and return ONLY a JSON object (no markdown, no explanation) with these fields:
- origin: starting location
- destination: ending location
- waypoints: array of intermediate stops (if mentioned)
- arrival_time: target arrival time (if mentioned, in 24h format like "10:00")
- preferences: array of user preferences (e.g., "no parking fees", "prefer BART", "willing to drive")
- constraints: array of constraints (e.g., "must arrive by 10am")

Example output:
{{
  "origin": "San Jose",
  "destination": "Salesforce Tower",
  "waypoints": [],
  "arrival_time": "10:00",
  "preferences": ["drive to transit station"],
  "constraints": ["arrive by 10am"]
}}

Return only the JSON, nothing else."""

        try:
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20250219",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text.strip()
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]

            parsed = json.loads(content)
            logger.info(f"Parsed query: {parsed}")
            return parsed

        except Exception as e:
            logger.warning(f"Claude parsing failed: {e}, using fallback")
            # Fallback: simple extraction
            return {
                "origin": "San Jose",
                "destination": "San Francisco",
                "waypoints": [],
                "arrival_time": None,
                "preferences": [],
                "constraints": []
            }

    async def _get_maps_data(self, parsed_query: dict) -> dict:
        """Get route data from Google Maps APIs."""
        try:
            origin = parsed_query.get("origin", "")
            destination = parsed_query.get("destination", "")

            # Geocode origin and destination
            origin_geocode = self.gmaps.geocode(origin)
            dest_geocode = self.gmaps.geocode(destination)

            if not origin_geocode or not dest_geocode:
                raise ValueError("Could not geocode origin or destination")

            # Get driving directions
            now = datetime.now()
            driving_directions = self.gmaps.directions(
                origin,
                destination,
                mode="driving",
                departure_time=now
            )

            # Get transit directions
            transit_directions = self.gmaps.directions(
                origin,
                destination,
                mode="transit",
                departure_time=now
            )

            return {
                "origin_geocode": origin_geocode[0],
                "destination_geocode": dest_geocode[0],
                "driving_route": driving_directions[0] if driving_directions else None,
                "transit_route": transit_directions[0] if transit_directions else None
            }

        except Exception as e:
            logger.exception(f"Error getting maps data: {e}")
            return {}

    async def _generate_routes_with_claude(self, parsed_query: dict, maps_data: dict) -> list:
        """Use Claude to generate optimal route options based on maps data."""

        # Extract key info from maps data
        origin = parsed_query.get("origin", "Unknown")
        destination = parsed_query.get("destination", "Unknown")
        waypoints = parsed_query.get("waypoints", [])
        preferences = parsed_query.get("preferences", [])

        driving_route = maps_data.get("driving_route", {})
        transit_route = maps_data.get("transit_route", {})

        # Get route details
        if driving_route and "legs" in driving_route:
            drive_leg = driving_route["legs"][0]
            drive_duration = drive_leg.get("duration", {}).get("value", 0) // 60  # minutes
            drive_distance = drive_leg.get("distance", {}).get("value", 0) / 1609.34  # miles
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

        # Determine available modes from preferences
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
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20250219",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text.strip()
            # Remove markdown if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]

            routes = json.loads(content)
            logger.info(f"Generated {len(routes)} routes")
            return routes

        except Exception as e:
            logger.warning(f"Route generation failed: {e}, using fallback")
            # Fallback: create sample routes
            return self._create_fallback_routes(origin, destination, drive_duration, drive_distance)

    def _create_fallback_routes(self, origin: str, destination: str, drive_duration: int, drive_distance: float) -> list:
        """Create sample routes if Claude fails."""
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

def main():
    """Main function to run the API server."""
    try:
        # Check required environment variables
        missing_vars = []
        for var in ['ANTHROPIC_API_KEY', 'GOOGLE_MAPS_API_KEY']:
            if not os.getenv(var):
                missing_vars.append(var)
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

        logger.info("Starting Beeline API Server")
        logger.info("Endpoints: POST /api/search")

        # Start the FastAPI server
        uvicorn.run(app, host="0.0.0.0", port=8000)
        return 0

    except Exception as e:
        logger.exception("Server error: %s", e)
        return 1

if __name__ == "__main__":
    exit(main())
