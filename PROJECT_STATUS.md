# Beeline Project Status

Last Updated: 2025-10-18

## Current Implementation

Beeline is now a fully functional multi-modal route planner with LLM integration and MCP (Model Context Protocol) support.

### Architecture

```
┌──────────────┐
│   Frontend   │ ← SvelteKit (Optional - Not Yet Connected)
│  (Web App)   │
└──────────────┘
       │
       ↓
┌──────────────────────────────────────────┐
│     Multi-Model API Server (Port 8000)   │
│  - Supports Claude & Gemini              │
│  - Auto-selects best available model     │
└──────┬───────────────────────────────────┘
       │
       ├─→ Claude 3.5 Sonnet (Anthropic)
       │   - Model: claude-3-5-sonnet-20250219
       │   - Best for: Production, reliable JSON
       │
       ├─→ Gemini 2.5 Flash (Google)
       │   - Model: gemini-2.5-flash
       │   - Best for: Development, FREE tier
       │
       └─→ Google Maps APIs (via MCP)
           - Geocoding
           - Directions (Driving & Transit)
           - Real-time traffic
```

## What's Working

### ✅ Multi-Model LLM Support
- **Claude API**: claude-3-5-sonnet-20250219
- **Gemini API**: gemini-2.5-flash (FREE tier)
- **Auto-select mode**: Prefers Gemini, falls back to Claude
- **Manual selection**: Choose model via API parameter

### ✅ Route Planning
- Natural language query parsing
- Multi-modal route generation
- Drive + transit combinations
- Cost optimization
- Time optimization
- Carbon savings calculations
- Parking cost estimates

### ✅ Google Maps Integration
- Geocoding for addresses
- Driving directions with traffic
- Transit directions with schedules
- Real-time data

### ✅ MCP Server
- WebSocket-based MCP server
- Google Maps tool integration
- Address validation support

### ✅ Testing Infrastructure
- Interactive test script (`llm_service/test_planner.py`)
- Multiple test modes
- Formatted output with emojis
- JSON export capability

## Quick Start

### Prerequisites
```bash
# Ensure you have Python 3.9+
python3 --version

# Create virtual environment
cd /Users/jaisood/Git/Beeline
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Multi-Model Server

```bash
# Set environment variables
export GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
export GEMINI_API_KEY=your_gemini_key_here
export ANTHROPIC_API_KEY=your_anthropic_key_here  # Optional

# Activate virtual environment
source venv/bin/activate

# Start server
python llm_service/api_server_multimodel.py
```

Server runs on: `http://0.0.0.0:8000`

### Testing Routes

**Auto-select (uses Gemini):**
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Palo Alto to Oracle Park by 7pm"}'
```

**Explicitly use Gemini:**
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"San Jose to Salesforce Tower", "model":"gemini"}'
```

**Explicitly use Claude:**
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Palo Alto to SF", "model":"claude"}'
```

### Interactive Testing

```bash
source venv/bin/activate
python llm_service/test_planner.py
```

Features:
1. Custom Input - Enter your own route details
2. Predefined Scenarios - Test example queries
3. Test Prompt Template - See and test prompts

## API Endpoints

### POST /api/search

Process natural language query and return route options.

**Request:**
```json
{
  "query": "Palo Alto to Oracle Park by 7pm",
  "model": "auto"  // "auto", "claude", or "gemini"
}
```

**Response:**
```json
{
  "query": {
    "origin": "Palo Alto",
    "destination": "Oracle Park",
    "waypoints": [],
    "arrival_time": "19:00",
    "preferences": [],
    "constraints": ["arrive by 7pm"]
  },
  "routes": [
    {
      "id": "route_1",
      "summary": "Drive to Millbrae + Caltrain",
      "total_duration": 59,
      "total_cost": 13.0,
      "time_savings": 0,
      "carbon_savings": 10.0,
      "legs": [...]
    }
  ],
  "metadata": {
    "timestamp": "2025-10-18T13:25:12.973892",
    "query_text": "Palo Alto to Oracle Park by 7pm",
    "model_used": "gemini"
  }
}
```

### GET /

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "service": "Beeline API (Multi-Model)",
  "available_models": ["claude", "gemini"]
}
```

## Model Comparison

| Feature | Claude 3.5 Sonnet | Gemini 2.5 Flash |
|---------|-------------------|------------------|
| **Cost** | Paid ($) | **FREE** ✅ |
| **JSON Output** | Excellent | Good |
| **Speed** | Fast | **Very Fast** ✅ |
| **Prompt Following** | Excellent | Very Good |
| **Context Length** | 200k tokens | 1M tokens |
| **Best For** | Production | Development/Testing |

## Environment Variables

### Required
```bash
GOOGLE_MAPS_API_KEY=your_google_maps_key
```

### Optional (at least one LLM key recommended)
```bash
GEMINI_API_KEY=your_gemini_key        # FREE tier available
ANTHROPIC_API_KEY=your_anthropic_key  # Paid
```

## File Structure

```
Beeline/
├── llm_service/
│   ├── api_server.py              # Claude-only server
│   ├── api_server_multimodel.py   # Multi-model server (CURRENT)
│   ├── mcp_server.py              # MCP WebSocket server
│   ├── test_planner.py            # Interactive test script
│   └── test.py                    # Original MCP tests
├── requirements.txt               # Python dependencies
├── MULTI_MODEL_GUIDE.md          # Multi-model usage guide
├── TESTING_GUIDE.md              # Testing documentation
├── DEMO_SETUP.md                 # Demo setup instructions
└── PROJECT_STATUS.md             # This file
```

## Known Issues

### Claude API
- Low credit balance may trigger fallback routes
- Fallback routes use Google Maps data but are less optimized

### Gemini API
- Occasionally returns markdown-wrapped JSON (auto-stripped)
- Free tier: 60 requests/minute limit

## Next Steps

### Immediate
1. ✅ Multi-model support (COMPLETED)
2. ✅ Gemini integration (COMPLETED)
3. ✅ Testing infrastructure (COMPLETED)

### Future
1. Frontend integration
2. Real-time parking API integration
3. Calendar integration for scheduling
4. User preferences persistence
5. Historical route analytics

## Testing Status

### ✅ Tested & Working
- Multi-model API server
- Claude query parsing
- Claude route generation
- Gemini query parsing
- Gemini route generation
- Google Maps geocoding
- Google Maps directions (driving)
- Google Maps directions (transit)
- Auto-select model mode
- Manual model selection
- Fallback handling

### 🔄 Needs Testing
- Frontend integration
- Long-running sessions
- Rate limiting behavior
- Error recovery

## Resources

- **Multi-Model Guide**: `MULTI_MODEL_GUIDE.md`
- **Testing Guide**: `TESTING_GUIDE.md`
- **Demo Setup**: `DEMO_SETUP.md`
- **Claude Docs**: https://docs.anthropic.com/
- **Gemini Docs**: https://ai.google.dev/
- **Google Maps APIs**: https://developers.google.com/maps

## Support

For issues:
1. Check server logs
2. Verify API keys are set
3. Test with curl commands
4. Use interactive test script

---

**Status**: Production-ready backend API with multi-model support
**Last Tested**: 2025-10-18
**Version**: 2.0.0 (Multi-Model)
