# Beeline Quick Start Guide

Get Beeline running in under 5 minutes!

## Fastest Path to Running Demo

### 1. Get API Keys (2 minutes)

#### Gemini (FREE - Recommended!)
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your key

#### Claude (Optional - Paid)
Get from: https://console.anthropic.com/

### 2. Install & Run (3 minutes)

```bash
# Navigate to project
cd /Users/jaisood/Git/Beeline

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export GOOGLE_MAPS_API_KEY=your_maps_key_here
export GEMINI_API_KEY=your_gemini_key_here

# Start server
python llm_service/api_server_multimodel.py
```

Server starts on `http://localhost:8000`

### 3. Test It (30 seconds)

```bash
# In a new terminal
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Palo Alto to Oracle Park by 7pm"}'
```

You should see 2-3 route options with drive+transit combinations!

## What You Get

✅ **Natural Language Queries**
```
"Palo Alto to Oracle Park by 7pm"
"San Jose to Salesforce Tower by 10am"
"Sunnyvale to SF Ferry Building"
```

✅ **Multi-Modal Routes**
- Drive to transit hub
- Park-and-ride options
- Full transit routes
- Cost comparisons
- Time savings
- Carbon impact

✅ **FREE Tier with Gemini**
- 60 requests/minute
- Fast responses
- High-quality routes

## Model Selection

**Default (Auto):**
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Your query here"}'
```
Uses Gemini (free) if available, falls back to Claude.

**Explicit Gemini:**
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Your query here", "model":"gemini"}'
```

**Explicit Claude:**
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Your query here", "model":"claude"}'
```

## Interactive Testing

```bash
source venv/bin/activate
python llm_service/test_planner.py
```

Features:
1. Custom queries
2. Predefined scenarios
3. Prompt template testing

## Example Routes

Query: **"Palo Alto to Oracle Park by 7pm"**

**Route 1: Direct Drive**
- Duration: 37 min
- Cost: $25 (parking)
- Fastest option

**Route 2: Park-and-Ride**
- Duration: 59 min
- Cost: $13 (parking + Caltrain)
- Drive to Millbrae, take Caltrain

**Route 3: Full Transit**
- Duration: 59 min
- Cost: $9.75 (Caltrain only)
- Walk to station, take Caltrain

## Health Check

```bash
curl http://localhost:8000/
```

Response shows available models:
```json
{
  "status": "ok",
  "service": "Beeline API (Multi-Model)",
  "available_models": ["claude", "gemini"]
}
```

## Troubleshooting

**Server won't start:**
```bash
# Check environment variables
echo $GOOGLE_MAPS_API_KEY
echo $GEMINI_API_KEY

# Check virtual environment
which python  # Should show venv path
```

**No routes generated:**
```bash
# Check server logs for errors
# Try different model: add "model":"gemini" or "model":"claude"
```

**Gemini API errors:**
- Verify key: https://makersuite.google.com/app/apikey
- Check rate limit: 60 req/min on free tier

## Next Steps

1. **Read Full Docs:**
   - `PROJECT_STATUS.md` - Current state
   - `MULTI_MODEL_GUIDE.md` - Model comparison
   - `TESTING_GUIDE.md` - Testing details
   - `DEMO_SETUP.md` - Complete setup

2. **Try Frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   # Visit http://localhost:5173
   ```

3. **Explore Code:**
   - `llm_service/api_server_multimodel.py` - Multi-model server
   - `llm_service/test_planner.py` - Interactive testing

## Success Criteria

You know it's working when:
- ✅ Server starts without errors
- ✅ Health check returns "ok"
- ✅ Test query returns 2-3 routes
- ✅ Routes have realistic times/costs
- ✅ Response includes `"model_used": "gemini"`

## Support

- Check logs in terminal where server is running
- Review `TROUBLESHOOTING.md`
- Test with interactive script: `python llm_service/test_planner.py`

---

**You're ready! Start planning multi-modal routes!** 🚀
