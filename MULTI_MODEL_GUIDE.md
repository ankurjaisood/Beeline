# Beeline Multi-Model Support

Beeline now supports multiple LLM providers! You can use **Claude**, **Gemini**, or both.

## Supported Models

### 1. **Claude (Anthropic)** 🤖
- Model: `claude-3-5-sonnet-20250219`
- Pros: Excellent at structured output, great function calling
- Cons: Requires paid API credits
- Best for: Production use

### 2. **Gemini (Google)** ⚡
- Model: `gemini-2.5-flash`
- Pros: **FREE tier available!**, fast, good performance
- Cons: Slightly less reliable JSON output
- Best for: Development, testing, free tier

## Setup

### Install Dependencies

```bash
cd /Users/jaisood/Git/Beeline
source venv/bin/activate
pip install google-generativeai
```

### Get API Keys

#### Gemini API Key (FREE!)
1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your key

#### Set Environment Variables

```bash
# Required
export GOOGLE_MAPS_API_KEY=your_google_maps_key

# At least ONE of these (or both!)
export ANTHROPIC_API_KEY=your_anthropic_key  # Claude
export GEMINI_API_KEY=your_gemini_key        # Gemini (recommended!)
```

## Running the Multi-Model Server

```bash
# Stop the old server first (if running)
# Then start the new multi-model server:

export GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
export GEMINI_API_KEY=your_gemini_key_here
# Optional: export ANTHROPIC_API_KEY=your_key

source venv/bin/activate
python llm_service/api_server_multimodel.py
```

## Using Different Models

### Option 1: Auto-Select (Default)
The server automatically picks the best available model:
- Prefers Gemini (free!)
- Falls back to Claude if Gemini unavailable

```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Palo Alto to Oracle Park"}'
```

### Option 2: Specify Model
Choose which model to use:

**Use Gemini:**
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Palo Alto to Oracle Park", "model":"gemini"}'
```

**Use Claude:**
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Palo Alto to Oracle Park", "model":"claude"}'
```

## Frontend Integration

The frontend automatically uses the multi-model endpoint. No changes needed!

To specify a model from the frontend, update `frontend/src/lib/services/api.ts`:

```typescript
export async function searchRoutes(query: string, model: string = "auto"): Promise<SearchResponse> {
  const response = await fetch(`${API_URL}/api/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, model })  // Add model parameter
  });
  return response.json();
}
```

## Comparison

| Feature | Claude | Gemini |
|---------|--------|--------|
| **Cost** | Paid ($) | **FREE** ✅ |
| **JSON Output** | Excellent | Good |
| **Speed** | Fast | **Very Fast** ✅ |
| **Prompt Following** | Excellent | Very Good |
| **Context Length** | 200k tokens | 32k tokens |
| **Best For** | Production | Development/Testing |

## Testing with Different Models

### Test Script with Model Selection

You can modify the test script to test different models:

```python
# In test_planner.py, modify the planner initialization:

# For Gemini:
import google.generativeai as genai
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
gemini_model = genai.GenerativeModel('gemini-2.5-flash')
planner = RoutePlanner(gemini_model, gmaps, model_type="gemini")

# For Claude:
claude_client = anthropic.Client(api_key=os.getenv('ANTHROPIC_API_KEY'))
planner = RoutePlanner(claude_client, gmaps, model_type="claude")
```

## Quick Start with Gemini (FREE!)

1. **Get Gemini API Key** (takes 1 minute):
   ```
   Visit: https://makersuite.google.com/app/apikey
   Click: Create API Key
   Copy the key
   ```

2. **Set environment variable**:
   ```bash
   export GEMINI_API_KEY=your_key_here
   ```

3. **Install dependency**:
   ```bash
   pip install google-generativeai
   ```

4. **Run multi-model server**:
   ```bash
   python llm_service/api_server_multimodel.py
   ```

5. **Test it**:
   ```bash
   curl -X POST http://localhost:8000/api/search \
     -H "Content-Type: application/json" \
     -d '{"query":"San Jose to SF by 10am", "model":"gemini"}'
   ```

## Architecture

```
Frontend → Multi-Model API Server → [Claude OR Gemini] → MCP Tools → Google Maps
                                              ↓
                                          Planner
```

The `RoutePlanner` class is model-agnostic and works with both LLMs!

## Troubleshooting

### "No LLM models available"
- Make sure you set at least one API key: `ANTHROPIC_API_KEY` or `GEMINI_API_KEY`

### Gemini returning malformed JSON
- Gemini sometimes adds markdown. The server automatically strips it.
- If issues persist, try Claude for more reliable output

### Rate limits
- **Gemini Free Tier**: 60 requests/minute
- **Claude**: Depends on your plan

## Recommendations

### For Development/Testing
✅ Use **Gemini** - it's FREE and fast!

### For Production
✅ Use **Claude** - more reliable, better JSON output

### Best of Both Worlds
✅ Set both API keys, use `model: "auto"`:
- Gemini for most requests (free!)
- Claude as fallback or for critical operations

---

**Ready to try Gemini?** It's free and takes just 1 minute to set up! 🚀
