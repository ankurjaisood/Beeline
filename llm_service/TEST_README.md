# Beeline Route Planner - Test Script

This interactive test script allows you to test the LLM + MCP integration directly without needing the frontend.

## Prerequisites

1. **Environment Variables Set:**
   ```bash
   export GOOGLE_MAPS_API_KEY=your_google_maps_key
   export ANTHROPIC_API_KEY=your_anthropic_key
   ```

2. **Virtual Environment Activated:**
   ```bash
   source ../venv/bin/activate
   ```

## Running the Test Script

```bash
cd llm_service
python test_planner.py
```

## Test Modes

### 1. Custom Input Mode
Enter your own route planning details interactively:
- Start address
- End address
- Waypoints (optional)
- Arrival time (optional)
- Preferences (optional)

The script will:
- Call the Route Planner
- Show formatted route results
- Optionally save full JSON response

**Example:**
```
Start address: Palo Alto
End address: Oracle Park
Waypoints: (press Enter)
Arrival time: 7:00 PM
Preferences: no parking fees, prefer BART
```

### 2. Predefined Scenarios
Test with pre-built example queries:

1. **Morning Commute to SF**
   - Query: "Get me from San Jose to Salesforce Tower by 10am. I want to drive to a Caltrain station."

2. **Evening Game at Oracle Park**
   - Query: "I'm at Palo Alto downtown. Need to get to Oracle Park by 7pm. Don't want to pay for parking."

3. **Morning Ferry Building Trip**
   - Query: "From San Mateo to SF Ferry Building by 9am. I prefer BART over Caltrain."

You can run individual scenarios or all of them sequentially.

### 3. Test Prompt Template
This mode lets you:
1. Enter route details
2. See the exact prompt that will be sent to Claude
3. Optionally send it to Claude API and see the response
4. View parsed JSON results

This is perfect for:
- Debugging the prompt template
- Testing Claude API responses
- Understanding how the prompt is structured

## Output Format

The script displays results in a readable format:

```
✅ Generated 1 route option(s):

🚗 Route 1: Drive to Millbrae BART, take BART to downtown SF
   ⏱️  Duration: 65 min
   💰 Cost: $12.50
   ⚡ Time saved vs driving: 15 min
   🌱 Carbon saved: 8.5 kg CO₂

   Legs:
   1. 🚗 DRIVE: San Jose → Millbrae BART Station
      ⏱️  25 min | 📏 15.0 mi | 💰 $0.00
      🚦 Traffic: moderate
      🅿️  Parking: $5.50 (75% available)

   2. 🚇 TRANSIT: Millbrae BART Station → Salesforce Tower
      ⏱️  35 min | 📏 18.0 mi | 💰 $7.00
      🚇 Line: BART Red Line (8 stops)
```

## Features

- ✅ **Interactive menus** - Easy to navigate
- ✅ **Formatted output** - Readable route summaries with emojis
- ✅ **JSON export** - Save full API responses
- ✅ **Error handling** - Clear error messages
- ✅ **Multiple test modes** - Flexible testing options
- ✅ **Prompt inspection** - See exact prompts sent to Claude

## Testing the Prompt Template

The script uses the exact same prompt template as the API server:

```
You are an AI assistant that helps users navigate multi-modally.
You can split the trip into legs where each leg uses a dedicated mode.

Optimize:
1. Reduce the number of transfers
2. Reduce the overall walking time
3. Reduce the overall trip time
4. Use transit to go as far as possible without transfers
5. Consider ride sharing or bike sharing for first/last mile
6. When driving suggest the best and lowest cost parking options.
   Only suggest driving if it is the first leg of a trip.

The user's ask is to plan a path using the following information:

start_address=<your input>
end_address=<your input>
waypoint_addresses=<your input>
modes=[drive, transit, walk, rideshare, bikeshare]
```

## Troubleshooting

### Error: Environment variables not set
```bash
export GOOGLE_MAPS_API_KEY=your_key
export ANTHROPIC_API_KEY=your_key
```

### Error: Module not found
```bash
source ../venv/bin/activate
pip install -r ../requirements.txt
```

### Claude API credits low
The script will use fallback routes based on Google Maps data. Routes will still be realistic but may not be as optimized as when Claude is working.

### Google Maps API errors
- Check that your API key is valid
- Verify the Geocoding and Directions APIs are enabled
- Check your API quota

## Quick Test Command

For a quick test without the menu:

```bash
# Test with predefined scenario
cd llm_service
python test_planner.py << EOF
2
1
EOF
```

This will run the first predefined scenario automatically.

## Example Session

```
================================================================================
  Beeline Route Planner Test Suite
================================================================================

Choose a test mode:

1. Custom Input - Enter your own route details
2. Predefined Scenarios - Test with example queries
3. Test Prompt Template - See and test the prompt template
4. Exit

Select option (1-4): 2

================================================================================
  Beeline Route Planner - Predefined Scenarios
================================================================================

📋 Available scenarios:

1. Morning Commute to SF
   Query: Get me from San Jose to Salesforce Tower by 10am...

Select scenario (1-3) or press Enter for all: 1

================================================================================
  Testing: Morning Commute to SF
================================================================================

📝 Query: Get me from San Jose to Salesforce Tower by 10am...

🔍 Planning your route...

✅ Generated 1 route option(s):
...
```

## Integration with Main API

This test script uses the same `RoutePlanner` class as the main API server (`api_server.py`), so:
- Any changes to the planner logic are automatically tested
- The prompt template is exactly the same
- Google Maps and Claude integrations are identical

This ensures your tests accurately reflect production behavior!
