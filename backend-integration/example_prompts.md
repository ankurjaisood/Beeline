# Claude Code Prompts for Backend Developer

This file contains ready-to-use prompts you can paste directly into Claude Code to build the Beeline backend planner service.

---

## Initial Setup Prompt

```
I'm building the backend planner service for Beeline, a Bay Area multi-modal transit routing app.

I need to create a Python FastAPI service that:
1. Receives structured JSON queries from an LLM service
2. Calculates optimized multi-modal routes combining driving, parking, and public transit
3. Integrates with Google Maps API for driving routes and traffic
4. Integrates with 511.org SF Bay Open Data Portal for real-time transit schedules
5. Returns 1-3 optimized route options with detailed journey legs

The full API contract is in backend-integration/BACKEND_INTEGRATION.md. Please:
1. Set up a Python FastAPI project structure
2. Create requirements.txt with necessary dependencies
3. Create .env.example with all required API keys
4. Create main.py with health check and placeholder /plan-route endpoint
5. Add CORS middleware to allow requests from http://localhost:5173
6. Create a README.md with setup instructions

Start by reading backend-integration/BACKEND_INTEGRATION.md to understand the full API specification.
```

---

## Google Maps Integration Prompt

```
I need to integrate Google Maps APIs into my Beeline backend service.

Requirements:
1. Create a google_maps.py module that wraps the Google Maps API
2. Implement functions for:
   - Geocoding addresses to coordinates
   - Getting driving directions between two points
   - Calculating drive time with current traffic
   - Getting distance matrix for multiple origin/destination pairs
   - Searching for parking lots near transit stations

3. Handle API errors gracefully
4. Add caching for repeated queries (use Redis or in-memory)
5. Respect rate limits

Use the googlemaps Python library. Store the API key in environment variables.

Example usage:
```python
drive_leg = await get_driving_route(
    origin="San Jose, CA",
    destination="Millbrae Caltrain Station",
    departure_time=datetime.now()
)
# Returns: distance, duration, polyline, traffic_level, toll_cost
```
```

---

## 511.org Transit Integration Prompt

```
I need to integrate real-time Bay Area transit data from 511.org into my Beeline backend.

Requirements:
1. Create a transit_data.py module for 511.org integration
2. Download and parse GTFS (General Transit Feed Specification) data for:
   - Caltrain
   - BART
   - Muni
   - VTA
   - AC Transit

3. Implement functions to:
   - Find next available train/bus from station A to station B
   - Get transit schedules for a specific time
   - Calculate transit fare
   - Get real-time service alerts and delays
   - Find nearest transit stations to a coordinate

4. Cache GTFS data (refresh every 5 minutes)
5. Handle service disruptions

Use the gtfs-realtime-bindings or transitfeed Python libraries.

Example usage:
```python
next_trains = await get_next_transit(
    from_station="Millbrae",
    to_station="San Francisco 4th & King",
    departure_after=datetime(2025, 10, 18, 9, 0),
    mode="Caltrain"
)
# Returns: list of train options with departure/arrival times, line names, stops
```

API documentation: https://511.org/open-data/transit
```

---

## Route Calculation Algorithm Prompt

```
I need to implement the core route calculation algorithm for Beeline.

The algorithm should:

1. **Identify Candidate Transit Hubs**
   - Given origin and destination, find all transit stations in the general corridor
   - Score stations based on:
     - Drive time from origin (prefer closer)
     - Transit frequency (prefer more frequent service)
     - Parking availability (prefer higher availability)
     - Parking cost (prefer cheaper)
   - Return top 5 candidate stations

2. **Calculate Complete Routes**
   For each candidate station, calculate:
   - Leg 1: Drive from origin to station (with traffic)
   - Leg 2: Park at station (5-min buffer + parking cost)
   - Leg 3: Transit from station to destination area
   - Leg 4: Last mile (walk, bike, or rideshare)

3. **Score and Rank Routes**
   Based on user's optimize_for preference:
   - time: Minimize total_duration
   - cost: Minimize total_cost
   - convenience: Minimize number of legs + duration
   - environmental: Maximize carbon_savings

4. **Apply Constraints**
   - Filter out routes that exceed max_walking_distance
   - Filter out routes that exceed max_cost
   - Remove routes with tolls if avoid_tolls is true

5. **Return Top 3 Routes**

Create a route_planner.py module with the main planning logic. Reference the full algorithm in backend-integration/BACKEND_INTEGRATION.md.

The function signature should be:
```python
async def plan_routes(
    origin: str,
    destination: str,
    arrival_time: datetime,
    preferences: TravelPreferences
) -> List[RouteOption]:
    # Implementation here
    pass
```
```

---

## Parking Data Integration Prompt

```
I need to add parking availability data to my Beeline backend.

Requirements:
1. Create a parking_data.py module
2. Integrate with available parking APIs:
   - SF MTA parking data (if available)
   - ParkMe API
   - Or create mock parking data for key transit stations

3. For each major transit station (Caltrain, BART), provide:
   - Parking lot name
   - Real-time availability (percentage)
   - Daily parking rate
   - Operating hours

4. Mock data structure:
```python
{
    "Millbrae Station": {
        "lots": [
            {
                "name": "Millbrae Station Lot A",
                "spaces_total": 200,
                "spaces_available": 130,
                "rate": 5.50,
                "rate_description": "$5.50/day"
            }
        ]
    }
}
```

5. Cache parking data (update every 10 minutes)

If real APIs aren't available for the hackathon, create realistic mock data based on typical parking availability patterns (fuller during commute hours).
```

---

## Route Optimization Prompt

```
I need to optimize the route calculation to handle different optimization preferences.

Create a route_optimizer.py module that:

1. **Calculate Carbon Savings**
```python
def calculate_carbon_savings(route: RouteOption) -> float:
    """
    Calculate kg CO2 saved compared to driving the entire route.
    - Driving: ~0.4 kg CO2 per mile
    - Transit: ~0.1 kg CO2 per mile
    - Walking/biking: 0 kg CO2
    """
    pass
```

2. **Calculate Time Savings**
```python
def calculate_time_savings(route: RouteOption, origin: str, destination: str) -> float:
    """
    Calculate minutes saved compared to driving the entire route in current traffic.
    """
    pass
```

3. **Calculate Confidence Score**
```python
def calculate_confidence(route: RouteOption) -> int:
    """
    Calculate route reliability (0-100) based on:
    - Traffic prediction accuracy (rush hour vs off-peak)
    - Transit on-time performance
    - Parking availability volatility
    - Weather conditions
    """
    pass
```

4. **Apply User Preferences**
```python
def score_route(route: RouteOption, optimize_for: str) -> float:
    """
    Score route based on optimization preference.
    Lower score = better route.
    """
    if optimize_for == "time":
        return route.total_duration
    elif optimize_for == "cost":
        return route.total_cost
    elif optimize_for == "convenience":
        return len(route.legs) * 20 + route.total_duration
    elif optimize_for == "environmental":
        return -route.carbon_savings  # Maximize savings
```

Reference the scoring algorithms in backend-integration/BACKEND_INTEGRATION.md.
```

---

## Testing & Mock Data Prompt

```
I need to add comprehensive testing to my Beeline backend service.

Requirements:

1. **Create test data** (tests/test_data.py):
   - Sample parsed queries
   - Expected route responses
   - Mock Google Maps responses
   - Mock transit schedule data

2. **Unit tests** (tests/test_route_planner.py):
   - Test route calculation with different preferences
   - Test constraint filtering
   - Test scoring algorithms
   - Test edge cases (no routes found, service unavailable)

3. **Integration tests** (tests/test_integration.py):
   - Test full /plan-route endpoint with sample queries
   - Test error handling
   - Test timeout scenarios

4. **Mock external services**:
   - Mock Google Maps API responses
   - Mock 511.org transit data
   - Mock parking availability data

5. Use pytest for testing framework

Create a comprehensive test suite that covers:
- Happy path (simple drive-and-ride)
- Transit-only routes
- Cost-constrained routes
- No routes found scenarios
- External service failures

Example test:
```python
def test_simple_drive_and_ride():
    query = {
        "origin": "San Jose, CA",
        "destination": "Salesforce Tower, San Francisco, CA",
        "arrival_time": "2025-10-18T10:00:00-07:00",
        "preferences": { ... }
    }

    response = client.post("/plan-route", json=query)
    assert response.status_code == 200
    assert len(response.json()["routes"]) >= 1
    assert response.json()["routes"][0]["total_duration"] < 120
```
```

---

## Deployment & Production Prompt

```
I need to prepare my Beeline backend service for deployment.

Requirements:

1. **Production configuration**:
   - Add environment-based config (dev, staging, prod)
   - Set up proper logging with structured logs
   - Add error tracking (Sentry or similar)
   - Configure timeout settings for external APIs

2. **Docker setup**:
   - Create Dockerfile for the service
   - Create docker-compose.yml for local development
   - Include Redis for caching if needed

3. **Performance optimizations**:
   - Add caching layer for repeated queries
   - Implement request batching for Google Maps API
   - Add connection pooling for external APIs
   - Optimize GTFS data loading

4. **Monitoring**:
   - Add metrics endpoints (Prometheus format)
   - Track API response times
   - Track external service health
   - Track cache hit rates

5. **Documentation**:
   - API documentation with OpenAPI/Swagger
   - Deployment guide
   - Runbook for common issues

Create production-ready configuration for deployment to Render.com, Railway.app, or similar Python hosting platforms.
```

---

## Quick Testing Prompt

```
Help me test my backend service locally.

1. Create a test_requests.sh script with curl commands for:
   - Health check
   - Simple drive-and-ride query
   - Transit-only query
   - Cost-constrained query
   - Query that should return no results

2. Create a load_test.py script using locust or similar to:
   - Test 100 concurrent requests
   - Measure average response time
   - Identify bottlenecks

3. Add logging to show:
   - Incoming requests
   - External API call times
   - Route calculation steps
   - Final response time

Example curl command:
```bash
curl -X POST http://localhost:8001/plan-route \
  -H "Content-Type: application/json" \
  -d @backend-integration/example-request.json
```

Make it easy to validate that the backend is working correctly before integrating with the frontend.
```

---

## How to Use These Prompts

1. **Copy the entire prompt** (including the triple backticks if shown)
2. **Paste into Claude Code**
3. **Let Claude Code implement the feature**
4. **Review the code** and iterate if needed

These prompts reference the full specifications in `BACKEND_INTEGRATION.md`, so make sure Claude Code has access to that file.

## Tips

- Start with the "Initial Setup Prompt" to get the basic structure
- Implement Google Maps and 511.org integrations in parallel
- Use mock data initially, then swap in real APIs
- Test each component independently before integration
- Use the testing prompt early to catch issues

Good luck with your hackathon! 🚀
