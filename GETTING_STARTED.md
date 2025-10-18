# Getting Started with Beeline

Welcome to Beeline! This guide will help you get your hackathon project up and running.

## What You've Got

I've created a complete full-stack application for you:

### ✅ Frontend (SvelteKit + TypeScript)
- **Landing page** with natural language input
- **Results page** with interactive map (Mapbox GL JS)
- **Route cards** showing optimized multi-modal journeys
- **Filter panel** for customizing route preferences
- **Mock data** so you can demo without a backend
- **Responsive design** with Tailwind CSS

### ✅ LLM Service (Python FastAPI)
- Parses natural language queries like "Get me from San Jose to SF by 10am"
- Works with OpenAI GPT-4 or Anthropic Claude
- Returns structured JSON for the backend planner
- CORS-enabled for local development

### ✅ Documentation
- **README.md** - Complete project documentation
- **QUICKSTART.md** - 5-minute setup guide
- **BACKEND_INTEGRATION.md** - Full API specs for your collaborator
- **example_prompts.md** - Ready-to-use Claude Code prompts for backend dev

## Quick Start (Choose Your Path)

### Path 1: Just Want to See It Work? (30 seconds)

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env and set:
#   PUBLIC_MOCK_MODE=true
#   PUBLIC_MAPBOX_TOKEN=pk.your_token_here (get from mapbox.com)
npm run dev
```

Open http://localhost:5173 and try a query!

### Path 2: Want AI Query Parsing? (2 minutes)

Follow Path 1, plus:

```bash
cd llm-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set OPENAI_API_KEY or ANTHROPIC_API_KEY
python main.py
```

In `frontend/.env`, set `PUBLIC_MOCK_MODE=false`

### Path 3: Full Integration with Backend? (5 minutes)

Follow Path 2, then share these files with your backend collaborator:
- `backend-integration/BACKEND_INTEGRATION.md`
- `backend-integration/example_prompts.md`

They can paste the prompts into Claude Code to build the backend!

## File Structure Explained

```
Beeline/
├── frontend/                    # Your frontend app
│   ├── src/
│   │   ├── routes/
│   │   │   ├── +page.svelte            # Landing page
│   │   │   └── results/+page.svelte    # Results with map
│   │   └── lib/
│   │       ├── components/
│   │       │   ├── Map.svelte          # Mapbox integration
│   │       │   ├── RouteCard.svelte    # Route display
│   │       │   └── FilterPanel.svelte  # Mode filters
│   │       ├── services/
│   │       │   ├── api.ts              # API calls
│   │       │   └── mockData.ts         # Demo data
│   │       ├── stores/
│   │       │   └── routeStore.ts       # State management
│   │       └── types/
│   │           └── index.ts            # TypeScript types
│   └── package.json
│
├── llm-service/                 # Query parser
│   ├── main.py                  # FastAPI server
│   ├── requirements.txt
│   └── .env.example
│
├── backend-integration/         # For your collaborator
│   ├── BACKEND_INTEGRATION.md   # Complete API specs
│   ├── example_prompts.md       # Claude Code prompts
│   └── example-request.json     # Sample request
│
├── README.md                    # Full documentation
├── QUICKSTART.md               # Quick setup
└── GETTING_STARTED.md          # This file
```

## API Keys You Need

### 1. Mapbox Token (Required for maps)
- Sign up at https://account.mapbox.com/
- Create a token (free tier works!)
- Add to `frontend/.env` as `PUBLIC_MAPBOX_TOKEN`

### 2. OpenAI or Anthropic API Key (Optional, for LLM service)
- OpenAI: https://platform.openai.com/
- Anthropic: https://console.anthropic.com/
- Add to `llm-service/.env`

**Tip:** You can demo without the LLM service by using mock mode!

## Testing Your Setup

### Test Frontend Only (Mock Mode)
1. Set `PUBLIC_MOCK_MODE=true` in `frontend/.env`
2. Run `cd frontend && npm run dev`
3. Open http://localhost:5173
4. Try: "Get me from San Jose to Salesforce Tower by 10 am"
5. You should see 3 route options with a map

### Test LLM Service
```bash
# Terminal 1
cd llm-service
source venv/bin/activate
python main.py

# Terminal 2 - Test health
curl http://localhost:8000/health

# Terminal 3 - Test query parsing
curl -X POST http://localhost:8000/parse-query \
  -H "Content-Type: application/json" \
  -d '{"query": "Get me from San Jose to SF by 10am"}'
```

### Test Full Stack
1. Run frontend (Terminal 1)
2. Run LLM service (Terminal 2)
3. Set `PUBLIC_MOCK_MODE=false` in `frontend/.env`
4. Open http://localhost:5173
5. Enter a query and see it get parsed by AI!

## Common Issues & Fixes

### "Cannot find module"
```bash
cd frontend
rm -rf node_modules
npm install
```

### "Port already in use"
```bash
# For port 5173
lsof -ti:5173 | xargs kill -9

# For port 8000
lsof -ti:8000 | xargs kill -9
```

### Map not showing
- Check `PUBLIC_MAPBOX_TOKEN` is set in `frontend/.env`
- Verify token is valid at https://account.mapbox.com/
- Look for errors in browser console (F12)

### LLM service not parsing queries
- Check API key is set in `llm-service/.env`
- Verify the service is running on port 8000
- Check `PUBLIC_LLM_API_URL` in `frontend/.env`

## Customizing for Your Demo

### Change Example Queries
Edit `frontend/src/routes/+page.svelte`, find `exampleQueries` array

### Add More Mock Routes
Edit `frontend/src/lib/services/mockData.ts`

### Change Colors/Styling
Edit `frontend/tailwind.config.js` and `frontend/src/app.css`

### Modify Map Appearance
Edit `frontend/src/lib/components/Map.svelte`

## Sharing with Your Backend Developer

Send them:
1. `backend-integration/BACKEND_INTEGRATION.md` - Complete API specs
2. `backend-integration/example_prompts.md` - Claude Code prompts they can paste
3. `backend-integration/example-request.json` - Sample request to test with

They can literally copy-paste the prompts into Claude Code and get a working backend!

## Demo Tips

### For a 3-Minute Demo:

**Minute 1 - The Problem:**
- Show Google Maps multi-step process (drive → park → transit)
- Explain the fragmentation pain point

**Minute 2 - The Solution:**
- Open Beeline
- Type natural language query
- Show 3 optimized routes instantly
- Highlight the visual journey synthesis

**Minute 3 - The Features:**
- Show filter panel (mode preferences)
- Explain optimization options (time/cost/environmental)
- Show route details (parking availability, transit schedules)
- Emphasize real-time data integration

### Sample Demo Queries:

1. **Suburban Commuter:**
   "Get me from San Jose to Salesforce Tower by 10 am. I want to drive to a Caltrain station."

2. **Budget Conscious:**
   "Palo Alto to Oracle Park by 7pm. Don't want to pay for parking. Optimize for cost."

3. **Environmental:**
   "From San Mateo to Ferry Building by 9am. Show me the greenest option."

4. **Accessible:**
   "Milpitas to Moscone by 11am. I need wheelchair accessible routes."

## Next Steps

1. **Get it running:** Follow the quick start above
2. **Customize:** Tweak colors, add your logo
3. **Test:** Try different queries
4. **Integrate:** Connect with backend when ready
5. **Deploy:** Push to Vercel/Netlify (frontend) and Render/Railway (LLM service)

## Resources

- **SvelteKit:** https://kit.svelte.dev/docs
- **Mapbox GL JS:** https://docs.mapbox.com/mapbox-gl-js/
- **FastAPI:** https://fastapi.tiangolo.com/
- **Tailwind CSS:** https://tailwindcss.com/docs

## Questions?

- Check `README.md` for detailed documentation
- See `QUICKSTART.md` for troubleshooting
- Review example code in `frontend/src/`

## Architecture Diagram

```
┌──────────────┐
│   Frontend   │ ← SvelteKit app (you can see/edit)
│  (Browser)   │   Location: frontend/src/
└──────┬───────┘
       │ User types: "San Jose to SF by 10am"
       ↓
┌──────────────┐
│ LLM Service  │ ← Parses natural language
│  (Port 8000) │   Location: llm-service/main.py
└──────┬───────┘
       │ Returns: { origin, destination, preferences }
       ↓
┌──────────────┐
│   Backend    │ ← Your collaborator's service
│  (Port 8001) │   See: backend-integration/
└──────┬───────┘
       │ Returns: [{ route1 }, { route2 }, { route3 }]
       ↓
┌──────────────┐
│   Frontend   │ ← Displays routes on map
│    (Map)     │
└──────────────┘
```

---

**You're all set! Time to build something awesome!** 🚀

Good luck with your hackathon! 🏆
