# Backend Integration Guide

This document provides complete specifications for integrating the Beeline backend planner service with the frontend and LLM service.

## Architecture Overview

```
Frontend (SvelteKit)
    ↓ Natural language query
LLM Service (Python FastAPI)
    ↓ Structured JSON (ParsedQuery)
Backend Planner (Your Service)
    ↓ Optimized routes (RouteResponse)
Frontend displays results
```

## API Contract

### Backend Planner Endpoints

Your backend service should expose the following endpoints:

#### `POST /plan-route`

Calculate optimized multi-modal routes based on structured query.

**Request Body:**
```json
{
  "origin": "San Jose, CA",
  "destination": "Salesforce Tower, San Francisco, CA",
  "arrival_time": "2025-10-18T10:00:00-07:00",
  "preferences": {
    "modes": {
      "driving": true,
      "parking": true,
      "transit": ["Caltrain", "BART"],
      "rideshare": ["Uber", "Lyft"],
      "micromobility": ["walking", "bike"],
      "combinations": ["drive_and_ride", "transit_only"]
    },
    "optimize_for": "time",
    "constraints": {
      "max_walking_distance": 0.5,
      "max_cost": null,
      "avoid_tolls": false,
      "accessible": false
    }
  }
}
```

**Request Schema:**

| Field | Type | Description |
|-------|------|-------------|
| `origin` | string | Starting location address or "current_location" |
| `destination` | string | Destination address or landmark |
| `arrival_time` | string | ISO 8601 timestamp in Pacific Time |
| `preferences.modes.driving` | boolean | Allow personal driving |
| `preferences.modes.parking` | boolean | Allow parking at transit hubs |
| `preferences.modes.transit` | array | Allowed transit systems (BART, Caltrain, Muni, VTA, AC Transit) |
| `preferences.modes.rideshare` | array | Allowed rideshare services (Uber, Lyft, Waymo) |
| `preferences.modes.micromobility` | array | Allowed micro-mobility (bike, scooter, walking) |
| `preferences.modes.combinations` | array | Route types (drive_and_ride, rideshare_to_transit, transit_only, drive_only) |
| `preferences.optimize_for` | string | Optimization goal: "time", "cost", "convenience", or "environmental" |
| `preferences.constraints.max_walking_distance` | number | Maximum walking distance in miles |
| `preferences.constraints.max_cost` | number\|null | Maximum total cost in dollars (null = no limit) |
| `preferences.constraints.avoid_tolls` | boolean | Avoid toll roads |
| `preferences.constraints.accessible` | boolean | Require wheelchair accessible routes |

**Response Body:**
```json
{
  "query": { /* Original query echoed back */ },
  "routes": [
    {
      "id": "route-1",
      "summary": "Drive to Millbrae, Caltrain to SF",
      "total_duration": 75,
      "total_cost": 18.5,
      "departure_time": "2025-10-18T08:45:00-07:00",
      "arrival_time": "2025-10-18T10:00:00-07:00",
      "confidence": 92,
      "carbon_savings": 8.5,
      "time_savings": 15,
      "legs": [
        {
          "mode": "drive",
          "from": "San Jose, CA",
          "to": "Millbrae Station Parking",
          "from_coords": { "lat": 37.3382, "lng": -121.8863 },
          "to_coords": { "lat": 37.5996, "lng": -122.3869 },
          "duration": 35,
          "distance": 28.5,
          "cost": 0,
          "details": {
            "traffic_level": "moderate",
            "toll_cost": 0
          }
        },
        {
          "mode": "park",
          "from": "Millbrae Station Parking",
          "to": "Millbrae Station Platform",
          "from_coords": { "lat": 37.5996, "lng": -122.3869 },
          "to_coords": { "lat": 37.5996, "lng": -122.3869 },
          "duration": 5,
          "distance": 0.1,
          "cost": 5.5,
          "details": {
            "parking_lot": "Millbrae Station Lot A",
            "parking_availability": 65,
            "parking_rate": "$5.50/day"
          }
        },
        {
          "mode": "transit",
          "from": "Millbrae Station",
          "to": "San Francisco 4th & King",
          "from_coords": { "lat": 37.5996, "lng": -122.3869 },
          "to_coords": { "lat": 37.7766, "lng": -122.3943 },
          "duration": 28,
          "distance": 15.2,
          "cost": 8.75,
          "details": {
            "line": "Caltrain Local 232",
            "departure_time": "2025-10-18T09:20:00-07:00",
            "arrival_time": "2025-10-18T09:48:00-07:00",
            "stops": 5
          }
        },
        {
          "mode": "walk",
          "from": "San Francisco 4th & King",
          "to": "Salesforce Tower",
          "from_coords": { "lat": 37.7766, "lng": -122.3943 },
          "to_coords": { "lat": 37.7897, "lng": -122.3972 },
          "duration": 12,
          "distance": 0.6,
          "cost": 0
        }
      ]
    }
  ],
  "generated_at": "2025-10-18T08:00:00-07:00"
}
```

**Response Schema:**

| Field | Type | Description |
|-------|------|-------------|
| `query` | object | Original parsed query (echoed back) |
| `routes` | array | 1-3 optimized route options |
| `routes[].id` | string | Unique route identifier |
| `routes[].summary` | string | Human-readable route summary |
| `routes[].total_duration` | number | Total travel time in minutes |
| `routes[].total_cost` | number | Total cost in dollars |
| `routes[].departure_time` | string | When to leave (ISO 8601) |
| `routes[].arrival_time` | string | When you'll arrive (ISO 8601) |
| `routes[].confidence` | number | Route reliability score (0-100) |
| `routes[].carbon_savings` | number | kg CO₂ saved vs driving (optional) |
| `routes[].time_savings` | number | Minutes saved vs driving only (optional) |
| `routes[].legs` | array | Individual journey segments |
| `legs[].mode` | string | Transport mode: drive, park, walk, transit, rideshare, bike, scooter |
| `legs[].from` | string | Starting location name |
| `legs[].to` | string | Ending location name |
| `legs[].from_coords` | object | Starting coordinates |
| `legs[].to_coords` | object | Ending coordinates |
| `legs[].duration` | number | Leg duration in minutes |
| `legs[].distance` | number | Leg distance in miles |
| `legs[].cost` | number | Leg cost in dollars |
| `legs[].details` | object | Mode-specific details (see below) |

**Leg Details by Mode:**

**Drive:**
```json
{
  "traffic_level": "light|moderate|heavy",
  "toll_cost": 0
}
```

**Park:**
```json
{
  "parking_lot": "Lot name",
  "parking_availability": 65,  // percentage
  "parking_rate": "$5.50/day"
}
```

**Transit:**
```json
{
  "line": "Caltrain Local 232",
  "departure_time": "2025-10-18T09:20:00-07:00",
  "arrival_time": "2025-10-18T09:48:00-07:00",
  "stops": 5
}
```

**Rideshare:**
```json
{
  "provider": "Uber",
  "wait_time": 5  // minutes
}
```

**Response Status Codes:**

| Code | Meaning |
|------|---------|
| 200 | Success - routes calculated |
| 400 | Bad request - invalid query parameters |
| 404 | No routes found for given constraints |
| 500 | Internal server error |
| 503 | External service unavailable (Google Maps, 511.org) |

#### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "beeline-planner",
  "version": "1.0.0",
  "external_services": {
    "google_maps": true,
    "transit_511": true,
    "weather": true
  }
}
```

## Data Sources

### Required External APIs

1. **511.org SF Bay Open Data Portal**
   - URL: https://511.org/open-data
   - Purpose: Real-time transit schedules, delays, and service alerts
   - Data: BART, Caltrain, Muni, VTA, AC Transit schedules
   - Format: GTFS (General Transit Feed Specification)

2. **Google Maps API**
   - Purpose: Driving routes, traffic data, geocoding
   - Endpoints needed:
     - Directions API (driving routes)
     - Distance Matrix API (travel times)
     - Geocoding API (address → coordinates)
     - Places API (parking lots, transit stations)

3. **Parking Data** (Optional but recommended)
   - SF MTA Parking: https://www.sfmta.com/projects/sfpark
   - Real-time parking availability at transit stations
   - Parking rates and restrictions

## Implementation Guide

### Core Algorithm Steps

1. **Parse and Validate Input**
   - Geocode origin and destination
   - Validate arrival/departure times
   - Parse mode preferences

2. **Identify Transit Hubs**
   - Find all transit stations along general route corridor
   - Filter by allowed transit modes (BART, Caltrain, etc.)
   - Score based on:
     - Parking availability
     - Parking cost
     - Transit frequency
     - Distance from origin

3. **Calculate Route Legs**

   For each promising transit hub:

   **Leg 1: Drive to station**
   - Use Google Maps Directions API
   - Factor in traffic (departure time matters!)
   - Calculate gas cost (~$0.15/mile)

   **Leg 2: Park**
   - Check parking availability
   - Get parking rate
   - Add 5-minute buffer for parking

   **Leg 3: Transit to destination area**
   - Use 511.org GTFS data
   - Find next available train/bus
   - Calculate fare

   **Leg 4: Last mile (walk/bike/rideshare)**
   - Walking: Google Maps Pedestrian API
   - Bike: Check bike share availability
   - Rideshare: Estimate based on distance

4. **Score and Rank Routes**

   Based on `optimize_for` preference:

   **Time optimization:**
   ```python
   score = total_duration + (transfers * 10)
   ```

   **Cost optimization:**
   ```python
   score = total_cost
   ```

   **Convenience optimization:**
   ```python
   score = (num_legs * 20) + total_duration
   ```

   **Environmental optimization:**
   ```python
   score = -carbon_savings  # Maximize savings
   ```

5. **Apply Constraints**
   - Filter routes exceeding `max_walking_distance`
   - Filter routes exceeding `max_cost`
   - Remove routes with tolls if `avoid_tolls` is true
   - Ensure accessibility if required

6. **Calculate Metadata**
   - `confidence`: Based on data freshness, traffic prediction accuracy
   - `carbon_savings`: Compare to driving entire route
   - `time_savings`: Compare to driving entire route (with traffic)

7. **Return Top 1-3 Routes**
   - Return best route plus 1-2 alternatives
   - Ensure variety (different stations, different transit lines)

### Key Transit Stations (Bay Area)

**Caltrain Stations with Parking:**
- San Jose Diridon
- Mountain View
- Palo Alto
- Menlo Park
- Redwood City
- San Carlos
- Belmont
- San Mateo
- Millbrae

**BART Stations with Parking:**
- Warm Springs
- Fremont
- Union City
- South Hayward
- Coliseum
- Daly City
- Dublin/Pleasanton
- El Cerrito del Norte

### Example Calculation

**Query:** "San Jose to Salesforce Tower by 10am, drive and ride"

**Step 1:** Geocode
- Origin: 37.3382, -121.8863 (San Jose downtown)
- Destination: 37.7897, -122.3972 (Salesforce Tower)

**Step 2:** Identify candidate stations
- Mountain View Caltrain (22 min drive)
- Millbrae Caltrain (35 min drive, but fewer stops to SF)
- Daly City BART (48 min drive, but BART is faster)

**Step 3:** Calculate routes for each

**Route Option 1: Millbrae Caltrain**
1. Drive: San Jose → Millbrae (35 min, 28.5 mi, $4.28 gas)
2. Park: Millbrae Lot A (5 min, $5.50)
3. Caltrain: Millbrae → SF 4th&King (28 min, $8.75)
4. Walk: 4th&King → Salesforce (12 min, 0.6 mi)
- **Total:** 80 min, $18.53
- **Depart:** 8:40am to arrive 10:00am

**Route Option 2: Mountain View Caltrain**
1. Drive: San Jose → Mountain View (22 min, 15.8 mi, $2.37 gas)
2. Park: MV Station Lot B (5 min, $3.00)
3. Caltrain Express: MV → SF 4th&King (43 min, $11.25)
4. Walk: 4th&King → Salesforce (12 min, 0.6 mi)
- **Total:** 82 min, $16.62
- **Depart:** 8:38am to arrive 10:00am

**Step 4:** Score
- Optimize for time: Route 1 wins (80 min)
- Optimize for cost: Route 2 wins ($16.62)

## Error Handling

### No Routes Found

If no routes satisfy all constraints:

```json
{
  "query": { /* original query */ },
  "routes": [],
  "error": {
    "code": "NO_ROUTES_FOUND",
    "message": "No routes found matching your preferences",
    "suggestions": [
      "Try increasing max_walking_distance to 1.0 miles",
      "Allow additional transit modes like BART",
      "Consider rideshare for the last mile"
    ]
  },
  "generated_at": "2025-10-18T08:00:00-07:00"
}
```

### External Service Failure

If Google Maps or 511.org is unavailable:

```json
{
  "error": {
    "code": "EXTERNAL_SERVICE_ERROR",
    "message": "Unable to fetch transit schedules from 511.org",
    "details": "Service temporarily unavailable"
  }
}
```

## Testing

### Sample Test Cases

**Test 1: Simple drive-and-ride**
```json
{
  "origin": "San Jose, CA",
  "destination": "Salesforce Tower, San Francisco, CA",
  "arrival_time": "2025-10-18T10:00:00-07:00",
  "preferences": {
    "modes": {
      "driving": true,
      "parking": true,
      "transit": ["Caltrain"],
      "rideshare": [],
      "micromobility": [],
      "combinations": ["drive_and_ride"]
    },
    "optimize_for": "time",
    "constraints": {
      "max_walking_distance": 0.5,
      "max_cost": null,
      "avoid_tolls": false,
      "accessible": false
    }
  }
}
```
Expected: 2-3 routes with Caltrain stations (Millbrae, Mountain View, etc.)

**Test 2: Transit-only**
```json
{
  "origin": "Palo Alto, CA",
  "destination": "Oracle Park, San Francisco, CA",
  "arrival_time": "2025-10-18T19:00:00-07:00",
  "preferences": {
    "modes": {
      "driving": false,
      "parking": false,
      "transit": ["Caltrain", "Muni"],
      "rideshare": [],
      "micromobility": ["walking"],
      "combinations": ["transit_only"]
    },
    "optimize_for": "cost",
    "constraints": {
      "max_walking_distance": 0.75,
      "max_cost": null,
      "avoid_tolls": false,
      "accessible": false
    }
  }
}
```
Expected: Caltrain routes with Muni connections

**Test 3: Cost-constrained**
```json
{
  "origin": "Milpitas, CA",
  "destination": "Moscone Center, San Francisco, CA",
  "arrival_time": "2025-10-18T11:00:00-07:00",
  "preferences": {
    "modes": {
      "driving": true,
      "parking": true,
      "transit": ["BART"],
      "rideshare": ["Uber", "Lyft"],
      "micromobility": [],
      "combinations": ["drive_and_ride", "rideshare_to_transit"]
    },
    "optimize_for": "cost",
    "constraints": {
      "max_walking_distance": 0.5,
      "max_cost": 20.0,
      "avoid_tolls": true,
      "accessible": false
    }
  }
}
```
Expected: Routes under $20, no tolls, may include BART + rideshare combinations

### Manual Testing with curl

```bash
curl -X POST http://localhost:8001/plan-route \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "San Jose, CA",
    "destination": "Salesforce Tower, San Francisco, CA",
    "arrival_time": "2025-10-18T10:00:00-07:00",
    "preferences": {
      "modes": {
        "driving": true,
        "parking": true,
        "transit": ["Caltrain"],
        "rideshare": [],
        "micromobility": [],
        "combinations": ["drive_and_ride"]
      },
      "optimize_for": "time",
      "constraints": {
        "max_walking_distance": 0.5,
        "max_cost": null,
        "avoid_tolls": false,
        "accessible": false
      }
    }
  }'
```

## Performance Requirements

- **Response time:** < 10 seconds for typical queries
- **Cache:** Consider caching transit schedules (update every 5 minutes)
- **Timeout:** Set 8-second timeout for external API calls
- **Rate limiting:** Handle Google Maps API rate limits gracefully

## Deployment Checklist

- [ ] Set up 511.org API credentials
- [ ] Set up Google Maps API key with required APIs enabled
- [ ] Configure CORS to allow frontend origin
- [ ] Set up error logging and monitoring
- [ ] Test with real-time transit data
- [ ] Implement caching for repeated queries
- [ ] Load test with 100 concurrent requests
- [ ] Set up health checks
- [ ] Document any additional endpoints

## Questions?

If you have questions about the API contract or need clarification:

1. Check the example requests/responses in this document
2. Review the frontend mock data in `frontend/src/lib/services/mockData.ts`
3. Test your endpoints with the provided curl commands
4. Check the example prompts in `backend-integration/example_prompts.md`

Happy coding! 🚗🚆
