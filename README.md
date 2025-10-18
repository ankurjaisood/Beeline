# Beeline - Hyper-Local Multi-Modal Transit App

Beeline is an AI-powered transit routing application that combines driving, parking, and public transit to provide optimized "drive-and-ride" routes in the San Francisco Bay Area. It fills a critical gap in existing navigation apps by seamlessly integrating multiple transportation modes.

## Project Overview

**The Problem:** Getting from suburban areas to downtown SF/Bay Area destinations often requires driving to a transit hub, then taking public transit. Current solutions (like Google Maps) require manually checking multiple routes and don't provide integrated planning.

**Our Solution:** Beeline uses AI to automatically identify optimal park-and-ride locations, combining real-time traffic, parking availability, and transit schedules into a single, optimized route.

## Architecture

```
┌─────────────┐
│   WebApp    │ ← SvelteKit Frontend (This repo)
│  (Frontend) │
└──────┬──────┘
       │ Natural language queries
       ↓
┌─────────────┐
│     LLM     │ ← Query parsing service (Python FastAPI)
│   Service   │
└──────┬──────┘
       │ Structured JSON
       ↓
┌─────────────┐
│   Planner   │ ← Backend route optimization (Your collaborator's Python service)
│  (Backend)  │
└──────┬──────┘
       │
       ├─→ MCP: Google Maps
       ├─→ MCP: Google Calendar
       └─→ MCP: Transit Info (511.org)
```

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** 18.x or higher ([Download](https://nodejs.org/))
- **npm** 9.x or higher (comes with Node.js)
- **Python** 3.9+ ([Download](https://www.python.org/))
- **pip** (comes with Python)
- **Git**

Check your versions:
```bash
node --version  # Should be v18.x.x or higher
npm --version   # Should be 9.x.x or higher
python3 --version  # Should be 3.9.x or higher
```

## Project Structure

```
beeline/
├── frontend/               # SvelteKit application
│   ├── src/
│   │   ├── routes/        # SvelteKit routes
│   │   │   ├── +page.svelte          # Landing page
│   │   │   └── results/
│   │   │       └── +page.svelte      # Results page
│   │   └── lib/
│   │       ├── components/  # Reusable UI components
│   │       ├── services/    # API communication
│   │       ├── stores/      # Svelte stores for state
│   │       └── types/       # TypeScript types
│   ├── static/            # Static assets
│   ├── package.json
│   └── .env.example
│
├── llm-service/           # Python FastAPI service
│   ├── main.py           # LLM query parser
│   ├── requirements.txt
│   └── .env.example
│
├── backend-integration/   # Backend developer docs
│   ├── BACKEND_INTEGRATION.md
│   └── example_prompts.md
│
└── README.md             # This file
```

## Quick Start (5 minutes to demo-ready)

### 1. Clone and Setup

```bash
# Navigate to project directory
cd Beeline

# Install frontend dependencies
cd frontend
npm install

# Setup frontend environment
cp .env.example .env
# Edit .env and add your Mapbox token (or use the demo key provided)

# Install LLM service dependencies
cd ../llm-service
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup LLM service environment
cp .env.example .env
# Edit .env and add your OpenAI or Anthropic API key
```

### 2. Run the Application

**Terminal 1 - Frontend:**
```bash
cd frontend
npm run dev
```
Frontend will be available at `http://localhost:5173`

**Terminal 2 - LLM Service:**
```bash
cd llm-service
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```
LLM service will be available at `http://localhost:8000`

**Terminal 3 - Backend (Your Collaborator's Service):**
```bash
# This will be provided by your backend developer
# See backend-integration/BACKEND_INTEGRATION.md for specs
cd backend
python main.py
```
Backend will be available at `http://localhost:8001`

### 3. Test the Application

1. Open `http://localhost:5173` in your browser
2. Try a sample query:
   ```
   Get me from San Jose to Salesforce Tower by 10 am.
   I want to drive to a Caltrain station. Show me the fastest option.
   ```
3. View the optimized routes with visual journey breakdown

## Detailed Setup Instructions

### Frontend Setup (SvelteKit)

#### 1. Install Dependencies

```bash
cd frontend
npm install
```

This installs:
- SvelteKit framework
- TypeScript for type safety
- Tailwind CSS for styling
- Mapbox GL JS for mapping
- Date-fns for time handling
- Lucide Svelte for icons

#### 2. Configure Environment Variables

Create `.env` file from template:
```bash
cp .env.example .env
```

Edit `.env` with your API keys:
```env
# Mapbox API Key (get from https://www.mapbox.com/)
PUBLIC_MAPBOX_TOKEN=pk.your_token_here

# LLM Service URL (default for local development)
PUBLIC_LLM_API_URL=http://localhost:8000

# Backend Planner Service URL
PUBLIC_PLANNER_API_URL=http://localhost:8001

# Optional: Enable mock mode for demo without backend
PUBLIC_MOCK_MODE=false
```

#### 3. Development Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run type checking
npm run check

# Format code
npm run format
```

### LLM Service Setup (Python FastAPI)

#### 1. Create Virtual Environment

```bash
cd llm-service
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI web framework
- Uvicorn ASGI server
- OpenAI Python SDK (or Anthropic)
- Pydantic for data validation
- Python-dotenv for environment variables
- HTTPX for async HTTP requests

#### 3. Configure Environment Variables

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env`:
```env
# OpenAI API Key (get from https://platform.openai.com/)
OPENAI_API_KEY=sk-your-key-here

# Or use Anthropic Claude
# ANTHROPIC_API_KEY=sk-ant-your-key-here

# Backend Planner Service URL
PLANNER_API_URL=http://localhost:8001

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:5173,http://localhost:5174

# Server Port
PORT=8000
```

#### 4. Run the Service

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run with auto-reload for development
python main.py

# Or use uvicorn directly
uvicorn main:app --reload --port 8000
```

The service will be available at `http://localhost:8000`

Test the API:
```bash
# Health check
curl http://localhost:8000/health

# Parse a query
curl -X POST http://localhost:8000/parse-query \
  -H "Content-Type: application/json" \
  -d '{"query": "Get me from San Jose to Salesforce Tower by 10 am"}'
```

## API Documentation

### LLM Service Endpoints

#### `POST /parse-query`

Parses natural language queries into structured JSON.

**Request:**
```json
{
  "query": "Get me from San Jose to Salesforce Tower by 10 am. I want to drive to a Caltrain station."
}
```

**Response:**
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

#### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "beeline-llm-service",
  "version": "1.0.0"
}
```

### Backend Planner Endpoints (Your Collaborator)

See `backend-integration/BACKEND_INTEGRATION.md` for complete API specifications.

## Environment Variables

### Frontend (.env)

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `PUBLIC_MAPBOX_TOKEN` | Mapbox GL JS API token | Yes | - |
| `PUBLIC_LLM_API_URL` | LLM service URL | No | `http://localhost:8000` |
| `PUBLIC_PLANNER_API_URL` | Backend planner URL | No | `http://localhost:8001` |
| `PUBLIC_MOCK_MODE` | Use mock data instead of real APIs | No | `false` |

### LLM Service (.env)

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Yes* | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | Yes* | - |
| `PLANNER_API_URL` | Backend planner URL | No | `http://localhost:8001` |
| `CORS_ORIGINS` | Allowed CORS origins | No | `http://localhost:5173` |
| `PORT` | Service port | No | `8000` |

*Either OpenAI or Anthropic API key required

## Mock Mode for Development

You can run the frontend with mock data without setting up the LLM or backend services:

1. Set `PUBLIC_MOCK_MODE=true` in `frontend/.env`
2. Run only the frontend: `cd frontend && npm run dev`
3. The app will use pre-generated sample routes

This is perfect for:
- UI/UX development
- Frontend testing
- Demo preparation without API keys
- Working offline

## Testing

### Frontend Tests

```bash
cd frontend
npm run test          # Run tests
npm run test:watch    # Run tests in watch mode
```

### LLM Service Tests

```bash
cd llm-service
source venv/bin/activate
pytest
```

### Integration Testing

Test the full flow with curl:

```bash
# 1. Test LLM service
curl -X POST http://localhost:8000/parse-query \
  -H "Content-Type: application/json" \
  -d '{"query": "Get me from Palo Alto to SFMOMA by 2pm"}'

# 2. Test backend planner (once your collaborator has it running)
curl -X POST http://localhost:8001/plan-route \
  -H "Content-Type: application/json" \
  -d @backend-integration/example-request.json

# 3. Test from frontend
# Open http://localhost:5173 and enter a query
```

## Troubleshooting

### Frontend Issues

**Issue:** `Cannot find module 'mapbox-gl'`
```bash
cd frontend
npm install mapbox-gl
```

**Issue:** Port 5173 already in use
```bash
# Kill the process using the port
lsof -ti:5173 | xargs kill -9
# Or specify a different port
npm run dev -- --port 5174
```

**Issue:** Map not displaying
- Check that `PUBLIC_MAPBOX_TOKEN` is set in `.env`
- Verify the token is valid at https://account.mapbox.com/
- Check browser console for errors

### LLM Service Issues

**Issue:** `ModuleNotFoundError: No module named 'fastapi'`
```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Issue:** `OpenAI API key not found`
- Verify `OPENAI_API_KEY` is set in `llm-service/.env`
- Check the key is valid at https://platform.openai.com/

**Issue:** CORS errors in browser
- Add your frontend URL to `CORS_ORIGINS` in `llm-service/.env`
- Restart the LLM service

**Issue:** Port 8000 already in use
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9
# Or change the port in .env
PORT=8080 python main.py
```

### Backend Integration Issues

**Issue:** Cannot connect to backend service
- Verify backend is running on the correct port
- Check `PUBLIC_PLANNER_API_URL` in frontend `.env`
- Check `PLANNER_API_URL` in LLM service `.env`

**Issue:** 504 Gateway Timeout from backend
- Backend routing calculations may take 10-15 seconds
- This is normal for complex multi-modal routes
- Frontend shows loading indicators during this time

## Demo Flow

### Suburban Sarah Persona

**Scenario:** Sarah lives in San Jose and needs to get to Salesforce Tower in SF by 10 AM for a meeting.

**Traditional Flow (Fragmented):**
1. Check Google Maps for driving time
2. Search for parking near Caltrain stations
3. Check Caltrain schedule separately
4. Calculate total time manually
5. Repeat for alternate routes

**Beeline Flow (Integrated):**
1. Enter: "Get me from San Jose to Salesforce Tower by 10 am. I want to drive to a Caltrain station."
2. Get 3 optimized options instantly
3. Visual map shows entire journey
4. Real-time updates for parking and transit

### Sample Queries for Demo

```
1. "Get me from San Jose to Salesforce Tower by 10 am. I want to drive to a Caltrain station. Show me the fastest option."

2. "I'm at Palo Alto downtown. Need to get to Oracle Park by 7pm. Don't want to pay for parking. Show me transit options."

3. "From San Mateo to SF Ferry Building by 9am. I prefer BART over Caltrain. Optimize for cost."

4. "Get me from Milpitas to Moscone Center by 11am. I'm okay with ride-sharing to transit. Avoid tolls."
```

### Demo Highlights

1. **Natural Language Input** - No need to understand transit systems
2. **Visual Synthesis** - See the entire multi-modal journey on one map
3. **Real-time Data** - Parking availability, transit delays, traffic
4. **Smart Optimization** - AI picks the best park-and-ride locations
5. **Time Savings** - Comparison shows minutes saved vs manual planning

## Development Workflow

### For Hackathon Development

1. **Frontend Developer (You):**
   ```bash
   cd frontend
   npm run dev
   # Work on UI/UX, add features, iterate on design
   ```

2. **Backend Developer (Your Collaborator):**
   - Follow `backend-integration/BACKEND_INTEGRATION.md`
   - Use the Claude Code prompts provided
   - Test with example requests

3. **Integration:**
   - Frontend calls LLM service with natural language
   - LLM service parses to structured JSON
   - Backend receives structured request
   - Backend returns optimized routes
   - Frontend visualizes results

### Best Practices

- **Use Mock Mode** during initial frontend development
- **Test with real APIs** before the demo
- **Keep backend integration docs updated** as APIs change
- **Use TypeScript** for type safety
- **Commit often** during the hackathon

## Deployment (Optional)

### Frontend (Vercel)

```bash
cd frontend
npm run build
# Deploy to Vercel, Netlify, or any static host
```

### LLM Service (Render/Railway)

```bash
cd llm-service
# Deploy to Render.com, Railway.app, or any Python host
# Set environment variables in the hosting platform
```

## Resources

- **SvelteKit Docs:** https://kit.svelte.dev/docs
- **Mapbox GL JS:** https://docs.mapbox.com/mapbox-gl-js/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **OpenAI API:** https://platform.openai.com/docs
- **Tailwind CSS:** https://tailwindcss.com/docs

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review `backend-integration/BACKEND_INTEGRATION.md`
3. Check the example prompts in `backend-integration/example_prompts.md`

## License

MIT License - Hackathon Project

## Acknowledgments

Built for [Hackathon Name] by:
- Frontend: [Your Name]
- Backend: [Collaborator Name]
- Powered by Claude AI, Mapbox, and 511.org

---

**Ready to revolutionize Bay Area commuting!**
