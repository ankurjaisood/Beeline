"""
Beeline LLM Service
Parses natural language transit queries into structured JSON for the backend planner.
"""

import os
import json
from datetime import datetime, timedelta
from typing import Optional, List
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Configuration
PORT = int(os.getenv("PORT", "8000"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4-turbo-preview")

# Initialize LLM clients
openai_client = None
anthropic_client = None

if LLM_PROVIDER == "openai":
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        openai_client = openai.OpenAI(api_key=openai_api_key)
elif LLM_PROVIDER == "anthropic":
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_api_key:
        anthropic_client = Anthropic(api_key=anthropic_api_key)

# FastAPI app
app = FastAPI(title="Beeline LLM Service", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class QueryRequest(BaseModel):
    query: str

class TravelModes(BaseModel):
    driving: bool = True
    parking: bool = True
    transit: List[str] = []
    rideshare: List[str] = []
    micromobility: List[str] = []
    combinations: List[str] = ["drive_and_ride"]

class TravelConstraints(BaseModel):
    max_walking_distance: float = 0.5
    max_cost: Optional[float] = None
    avoid_tolls: bool = False
    accessible: bool = False

class TravelPreferences(BaseModel):
    modes: TravelModes
    optimize_for: str = "time"
    constraints: TravelConstraints

class ParsedQuery(BaseModel):
    origin: str
    destination: str
    arrival_time: str
    preferences: TravelPreferences

# System prompt for LLM
SYSTEM_PROMPT = """You are a transit query parser for Beeline, a Bay Area multi-modal transit app.

Your job is to parse natural language queries into structured JSON. Extract:
1. Origin location (use "current_location" if not specified)
2. Destination location
3. Arrival time (or departure time if specified)
4. Transportation preferences

Transportation modes:
- driving: Personal car
- parking: Parking at transit hubs
- transit: BART, Caltrain, Muni, VTA, AC Transit
- rideshare: Uber, Lyft, Waymo
- micromobility: bike, scooter, walking

Route combinations:
- drive_and_ride: Drive to transit station, then take transit
- rideshare_to_transit: Rideshare to transit, then take transit
- transit_only: Only public transit
- drive_only: Only driving

Optimization preferences:
- time: Fastest route
- cost: Cheapest route
- convenience: Fewest transfers
- environmental: Lowest carbon footprint

Parse the query and return ONLY valid JSON matching this schema:
{
  "origin": "string (location or 'current_location')",
  "destination": "string (specific address or landmark)",
  "arrival_time": "ISO 8601 timestamp (infer reasonable time if not specified)",
  "preferences": {
    "modes": {
      "driving": boolean,
      "parking": boolean,
      "transit": ["string"],
      "rideshare": ["string"],
      "micromobility": ["string"],
      "combinations": ["string"]
    },
    "optimize_for": "time|cost|convenience|environmental",
    "constraints": {
      "max_walking_distance": number (in miles),
      "max_cost": number or null,
      "avoid_tolls": boolean,
      "accessible": boolean
    }
  }
}

Examples:
Query: "Get me from San Jose to Salesforce Tower by 10 am. I want to drive to a Caltrain station."
Response: {
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

Query: "Palo Alto to Oracle Park by 7pm. Transit only, avoid parking costs."
Response: {
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

Always use Pacific Time (PT/PDT) for timestamps.
Return ONLY the JSON, no additional text or explanation.
"""

def parse_with_openai(query: str) -> dict:
    """Parse query using OpenAI"""
    if not openai_client:
        raise HTTPException(status_code=500, detail="OpenAI client not initialized")

    try:
        response = openai_client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")

def parse_with_anthropic(query: str) -> dict:
    """Parse query using Anthropic Claude"""
    if not anthropic_client:
        raise HTTPException(status_code=500, detail="Anthropic client not initialized")

    try:
        message = anthropic_client.messages.create(
            model=LLM_MODEL,
            max_tokens=1024,
            temperature=0.3,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": query}
            ]
        )

        content = message.content[0].text
        return json.loads(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Anthropic error: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "beeline-llm-service",
        "version": "1.0.0",
        "provider": LLM_PROVIDER,
        "model": LLM_MODEL
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "beeline-llm-service",
        "version": "1.0.0",
        "provider": LLM_PROVIDER,
        "llm_configured": openai_client is not None or anthropic_client is not None
    }

@app.post("/parse-query", response_model=ParsedQuery)
async def parse_query(request: QueryRequest):
    """Parse natural language query into structured format"""

    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # Check if LLM is configured
    if not openai_client and not anthropic_client:
        raise HTTPException(
            status_code=503,
            detail="LLM service not configured. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY"
        )

    try:
        # Parse using configured provider
        if LLM_PROVIDER == "openai":
            parsed_data = parse_with_openai(request.query)
        else:
            parsed_data = parse_with_anthropic(request.query)

        # Validate and return
        return ParsedQuery(**parsed_data)

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse LLM response: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing query: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print(f"🐝 Starting Beeline LLM Service on port {PORT}")
    print(f"   Provider: {LLM_PROVIDER}")
    print(f"   Model: {LLM_MODEL}")
    print(f"   CORS: {CORS_ORIGINS}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
