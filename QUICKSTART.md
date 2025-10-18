# Beeline - Quick Start Guide

Get Beeline running in 5 minutes for your hackathon demo!

## Option 1: Frontend Only (Mock Mode) - Fastest!

Perfect for UI/UX development and demos without API keys.

### 1. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 2. Create Environment File

```bash
cp .env.example .env
```

Edit `frontend/.env` and set:
```env
PUBLIC_MOCK_MODE=true
PUBLIC_MAPBOX_TOKEN=pk.your_token_here
```

Get a free Mapbox token at https://account.mapbox.com/

### 3. Run Frontend

```bash
npm run dev
```

Open http://localhost:5173 and try the example queries!

**No backend needed in mock mode!** ✨

---

## Option 2: Full Stack (With LLM Service)

Adds natural language parsing with AI.

### 1. Setup Frontend (Same as Option 1)

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env:
# - Set PUBLIC_MOCK_MODE=false
# - Set PUBLIC_MAPBOX_TOKEN=your_token
```

### 2. Setup LLM Service

```bash
cd llm-service
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env:
# - Set OPENAI_API_KEY=your_key or ANTHROPIC_API_KEY=your_key
```

Get API keys:
- OpenAI: https://platform.openai.com/
- Anthropic: https://console.anthropic.com/

### 3. Run Both Services

**Terminal 1:**
```bash
cd frontend
npm run dev
```

**Terminal 2:**
```bash
cd llm-service
source venv/bin/activate
python main.py
```

Open http://localhost:5173

---

## Option 3: Full Stack with Backend

Complete integration with your collaborator's backend planner.

Same as Option 2, plus:

**Terminal 3:**
```bash
cd backend  # Your collaborator's service
python main.py
```

---

## Demo Queries

Try these in the frontend:

1. **Drive and Ride:**
   ```
   Get me from San Jose to Salesforce Tower by 10 am.
   I want to drive to a Caltrain station. Show me the fastest option.
   ```

2. **Transit Only:**
   ```
   Palo Alto to Oracle Park by 7pm. Don't want to pay for parking.
   ```

3. **Cost Optimized:**
   ```
   From San Mateo to SF Ferry Building by 9am. Optimize for cost.
   ```

4. **With Constraints:**
   ```
   Milpitas to Moscone Center by 11am. I'm okay with ride-sharing.
   Avoid tolls and keep it under $20.
   ```

---

## Troubleshooting

### "Cannot find module 'mapbox-gl'"
```bash
cd frontend
npm install
```

### "Port 5173 already in use"
```bash
lsof -ti:5173 | xargs kill -9
```

### "Map not displaying"
- Check that PUBLIC_MAPBOX_TOKEN is set in `frontend/.env`
- Make sure it's a valid token from https://account.mapbox.com/

### "OpenAI API key not found"
- Check that OPENAI_API_KEY is set in `llm-service/.env`
- Or use mock mode: set PUBLIC_MOCK_MODE=true in `frontend/.env`

---

## What's Included

- ✅ Modern SvelteKit frontend with Tailwind CSS
- ✅ Interactive Mapbox GL JS mapping
- ✅ Natural language query parsing (LLM service)
- ✅ Mock data for demos without backend
- ✅ Filter panel for mode preferences
- ✅ Beautiful route visualization
- ✅ Responsive mobile-friendly design
- ✅ Complete backend integration docs

---

## Next Steps

1. **Customize the UI:** Edit files in `frontend/src/routes/` and `frontend/src/lib/components/`

2. **Add More Mock Routes:** Edit `frontend/src/lib/services/mockData.ts`

3. **Integrate Real Backend:** Follow `backend-integration/BACKEND_INTEGRATION.md`

4. **Deploy:**
   - Frontend: Vercel, Netlify
   - LLM Service: Render.com, Railway.app

---

## Project Structure Quick Reference

```
Beeline/
├── frontend/               # SvelteKit app
│   ├── src/
│   │   ├── routes/
│   │   │   ├── +page.svelte        # Landing page
│   │   │   └── results/
│   │   │       └── +page.svelte    # Results page
│   │   └── lib/
│   │       ├── components/         # Map, RouteCard, FilterPanel
│   │       ├── services/           # API calls, mock data
│   │       └── stores/             # Svelte stores
│   └── package.json
│
├── llm-service/            # Python FastAPI
│   ├── main.py             # LLM query parser
│   └── requirements.txt
│
├── backend-integration/    # Docs for your collaborator
│   ├── BACKEND_INTEGRATION.md
│   └── example_prompts.md
│
└── README.md              # Full documentation
```

---

## Getting Help

- Check `README.md` for detailed setup instructions
- See `backend-integration/BACKEND_INTEGRATION.md` for API specs
- Review `backend-integration/example_prompts.md` for Claude Code prompts

**Ready to demo!** 🚗🚆🗺️
