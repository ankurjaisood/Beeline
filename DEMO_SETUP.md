# Beeline Demo Setup Guide

This guide will help you run the Beeline multi-modal transit app demo on localhost.

## Architecture Overview

```
WebApp (Frontend) → LLM Service (Backend API) → Claude + MCP Tools → Google Maps
                                              ↓
                                           Planner
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- Google Maps API Key (Required)
- Anthropic API Key (Optional - for Claude)
- Gemini API Key (Optional - for Gemini, **FREE tier available**)

## Setup Instructions

### 1. Backend Setup (llm_service)

```bash
cd llm_service

# Create virtual environment (if not exists)
python3 -m venv ../venv
source ../venv/bin/activate

# Install dependencies
pip install -r ../requirements.txt

# Set environment variables
export GOOGLE_MAPS_API_KEY=your_google_maps_api_key

# For multi-model support (recommended):
export GEMINI_API_KEY=your_gemini_api_key        # FREE tier available!
export ANTHROPIC_API_KEY=your_anthropic_api_key  # Optional

# Start the multi-model API server (runs on port 8000)
python api_server_multimodel.py

# Or start Claude-only server:
# python api_server.py
```

The backend will be available at: `http://localhost:8000`

API Endpoints:
- `GET /` - Health check
- `POST /api/search` - Search for routes

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server (runs on port 5173)
npm run dev
```

The frontend will be available at: `http://localhost:5173`

## Testing the Demo

1. **Start the backend** (Terminal 1):
   ```bash
   cd llm_service
   source ../venv/bin/activate
   export GOOGLE_MAPS_API_KEY=your_key
   export ANTHROPIC_API_KEY=your_key
   python api_server.py
   ```

2. **Start the frontend** (Terminal 2):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open browser** and navigate to `http://localhost:5173`

4. **Try example queries**:
   - "Get me from San Jose to Salesforce Tower by 10 am. I want to drive to a Caltrain station."
   - "I'm at Palo Alto downtown. Need to get to Oracle Park by 7pm. Don't want to pay for parking."
   - "From San Mateo to SF Ferry Building by 9am. I prefer BART over Caltrain."

## How It Works

1. **User enters query** in natural language on the frontend
2. **Frontend sends** POST request to `/api/search` endpoint
3. **Backend LLM Service**:
   - Uses LLM (Claude or Gemini) to parse the query and extract origin, destination, preferences
   - Calls Google Maps APIs to get geocoding, directions, and traffic data
   - Uses LLM again to generate 2-3 optimal multi-modal route options
4. **Planner component** structures the routes with drive+transit combinations
5. **Frontend displays** route options with map visualization

### Multi-Model Support

The multi-model server (`api_server_multimodel.py`) supports:
- **Gemini 2.5 Flash** - Google's LLM with FREE tier (60 requests/min)
- **Claude 3.5 Sonnet** - Anthropic's LLM (paid, more reliable)

Auto-select mode (default) prefers Gemini for cost savings, falls back to Claude if unavailable.

## API Response Format

```json
{
  "query": {
    "origin": "San Jose",
    "destination": "Salesforce Tower",
    "arrival_time": "10:00",
    "preferences": ["drive to transit station"],
    "constraints": ["arrive by 10am"]
  },
  "routes": [
    {
      "id": "route_1",
      "summary": "Drive to Millbrae BART, take BART to downtown SF",
      "total_duration": 65,
      "total_cost": 12.50,
      "time_savings": 15,
      "carbon_savings": 8.5,
      "legs": [
        {
          "mode": "drive",
          "from": "San Jose",
          "to": "Millbrae BART Station",
          "duration": 25,
          "distance": 15.0,
          "cost": 0,
          "details": {
            "traffic_level": "moderate",
            "parking_cost": 5.50,
            "parking_availability": 75
          }
        },
        {
          "mode": "transit",
          "from": "Millbrae BART Station",
          "to": "Salesforce Tower",
          "duration": 35,
          "distance": 18.0,
          "cost": 7.00,
          "details": {
            "line": "BART Red Line",
            "stops": 8
          }
        }
      ]
    }
  ],
  "metadata": {
    "timestamp": "2025-10-18T19:30:00",
    "query_text": "Get me from San Jose to Salesforce Tower by 10 am...",
    "model_used": "gemini"
  }
}
```

## Troubleshooting

### Backend won't start
- Check that environment variables are set: `echo $GOOGLE_MAPS_API_KEY`
- Verify Python dependencies are installed: `pip list | grep anthropic`

### Frontend can't connect to backend
- Check backend is running: `curl http://localhost:8000/`
- Verify CORS is allowed (already configured for localhost:5173)

### No routes generated
- Check backend logs for LLM API errors
- If using Claude: Verify Anthropic API key has sufficient credits
- If using Gemini: Verify API key is valid (get free key at https://makersuite.google.com/app/apikey)
- Check Google Maps API quota
- Try switching models: add `"model":"gemini"` or `"model":"claude"` to the request

### Map not displaying
- Frontend uses Leaflet + OpenStreetMap (no API key needed)
- Check browser console for errors
- Ensure `leaflet` npm package is installed

## Next Steps

- Add real-time transit data integration
- Implement actual parking availability APIs
- Add user preferences persistence
- Enhance route optimization algorithms
- Add mobile responsive design improvements
