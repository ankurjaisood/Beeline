# 🚀 Beeline - No API Keys Required!

## Good News: Zero Setup Required for Maps!

I've updated Beeline to use **Leaflet + OpenStreetMap** instead of Mapbox, which means:

✅ **No credit card required**
✅ **No API keys needed for maps**
✅ **Completely free**
✅ **Perfect for hackathons**

---

## Quick Start (Under 1 Minute!)

### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

### Step 2: Create Environment File

```bash
cp .env.example .env
```

Your `.env` file should look like this:

```env
# LLM Service URL (local development)
PUBLIC_LLM_API_URL=http://localhost:8000

# Backend Planner Service URL
PUBLIC_PLANNER_API_URL=http://localhost:8001

# Enable mock mode to use sample data without backend services
PUBLIC_MOCK_MODE=true
```

**That's it! No API keys needed!**

### Step 3: Start the App

```bash
npm run dev
```

Open **http://localhost:5173** in your browser!

---

## Try These Queries

The app comes with pre-loaded demo data. Try these:

1. **Drive and Ride:**
   ```
   Get me from San Jose to Salesforce Tower by 10 am.
   I want to drive to a Caltrain station. Show me the fastest option.
   ```

2. **Transit Only:**
   ```
   Palo Alto to Oracle Park by 7pm. Don't want to pay for parking.
   ```

3. **Any Query (uses mock data):**
   ```
   From San Mateo to SF Ferry Building by 9am.
   ```

You'll see beautiful routes rendered on **OpenStreetMap** with colored segments for each mode of transport!

---

## What You'll See

- 🗺️ **Interactive map** with route visualization (no API key!)
- 🚗 **Drive segments** in blue
- 🅿️ **Parking** in purple
- 🚆 **Transit** in red
- 🚶 **Walking** in green
- 💰 **Cost and time breakdown** for each route
- 🌱 **Carbon savings** compared to driving

---

## Add LLM Service Later (Optional)

If you want natural language parsing with AI, you can add it later:

```bash
cd llm-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add OPENAI_API_KEY or ANTHROPIC_API_KEY to .env
python main.py
```

Then set `PUBLIC_MOCK_MODE=false` in `frontend/.env`

But for now, **you can demo everything with zero setup!**

---

## Map Features

The OpenStreetMap integration includes:

- ✅ **Route segments** with different colors for each mode
- ✅ **Markers** for start (green), stops (colored), and destination (red)
- ✅ **Popups** showing location details
- ✅ **Auto-zoom** to fit entire route
- ✅ **Pan and zoom** controls
- ✅ **Mobile responsive**

---

## Why OpenStreetMap?

| Feature | OpenStreetMap | Mapbox | Google Maps |
|---------|---------------|--------|-------------|
| Cost | 100% Free | Requires credit card | Requires credit card |
| API Key | None needed | Required | Required |
| Hackathon Ready | ✅ Yes | ❌ Setup required | ❌ Setup required |
| Route Visualization | ✅ Great | ✅ Excellent | ⚠️ Limited |
| Customization | ✅ Full control | ✅ Full control | ❌ Restricted |

**Perfect for hackathons where you just want to build and demo!**

---

## Troubleshooting

### "Cannot find module 'leaflet'"
```bash
cd frontend
rm -rf node_modules
npm install
```

### "Port 5173 already in use"
```bash
lsof -ti:5173 | xargs kill -9
npm run dev
```

### Map not showing
- Check browser console (F12) for errors
- Make sure `npm install` completed successfully
- Try refreshing the page

---

## Next Steps

1. ✅ **You're already done!** The app is working with maps
2. 🎨 **Customize the UI** if you want
3. 🔌 **Connect to backend** when your collaborator is ready
4. 🤖 **Add LLM service** if you want AI query parsing

---

## Project Structure

Everything works out of the box:

```
frontend/
├── src/
│   ├── routes/
│   │   ├── +page.svelte          # Landing page ✅
│   │   └── results/+page.svelte  # Results with map ✅
│   └── lib/
│       ├── components/
│       │   └── Map.svelte        # OpenStreetMap integration ✅
│       └── services/
│           └── mockData.ts       # Demo routes ✅
```

---

## Demo Ready in 3 Commands!

```bash
cd frontend
npm install
npm run dev
```

**That's it! Open http://localhost:5173 and you're demoing!** 🎉

---

## Comparison: Before vs After

### Before (Mapbox):
1. Sign up for Mapbox account
2. Add credit card
3. Get API token
4. Add to `.env`
5. Hope it works

### After (OpenStreetMap):
1. `npm install`
2. `npm run dev`
3. **Done!** ✨

---

**Happy hacking!** 🚀

No setup. No API keys. No credit cards. Just code and demo!
