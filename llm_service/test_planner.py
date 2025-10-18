#!/usr/bin/env python3
"""
Interactive test script for the Beeline Route Planner.
Tests the LLM + MCP integration without the frontend.
"""

import os
import sys
import json
import asyncio
from datetime import datetime
import anthropic
import googlemaps

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api_server import RoutePlanner


def print_separator(char="=", length=80):
    """Print a separator line."""
    print(char * length)


def print_header(title):
    """Print a formatted header."""
    print_separator()
    print(f"  {title}")
    print_separator()


def print_route_summary(routes):
    """Pretty print route summaries."""
    print(f"\n✅ Generated {len(routes)} route option(s):\n")

    for i, route in enumerate(routes, 1):
        print(f"\n🚗 Route {i}: {route['summary']}")
        print(f"   ⏱️  Duration: {route['total_duration']} min")
        print(f"   💰 Cost: ${route['total_cost']:.2f}")

        if route.get('time_savings'):
            print(f"   ⚡ Time saved vs driving: {route['time_savings']} min")
        if route.get('carbon_savings'):
            print(f"   🌱 Carbon saved: {route['carbon_savings']:.1f} kg CO₂")

        print(f"\n   Legs:")
        for j, leg in enumerate(route['legs'], 1):
            mode_emoji = {"drive": "🚗", "transit": "🚇", "walk": "🚶", "rideshare": "🚕", "bikeshare": "🚲"}.get(leg['mode'], "🚌")
            print(f"   {j}. {mode_emoji} {leg['mode'].upper()}: {leg['from']} → {leg['to']}")
            print(f"      ⏱️  {leg['duration']} min | 📏 {leg['distance']:.1f} mi | 💰 ${leg['cost']:.2f}")

            if leg.get('details'):
                details = leg['details']
                if details.get('traffic_level'):
                    print(f"      🚦 Traffic: {details['traffic_level']}")
                if details.get('parking_cost'):
                    print(f"      🅿️  Parking: ${details['parking_cost']:.2f} ({details.get('parking_availability', 0)}% available)")
                if details.get('line'):
                    print(f"      🚇 Line: {details['line']} ({details.get('stops', 0)} stops)")


async def test_with_custom_input():
    """Test with custom user input."""
    print_header("Beeline Route Planner - Interactive Test")

    print("\n📝 Enter your route planning details:\n")

    # Get user input
    origin = input("Start address (e.g., 'Palo Alto'): ").strip()
    destination = input("End address (e.g., 'Oracle Park'): ").strip()

    waypoints_input = input("Waypoints (comma-separated, or press Enter to skip): ").strip()
    waypoints = [w.strip() for w in waypoints_input.split(',')] if waypoints_input else []

    arrival_time = input("Arrival time (e.g., '7:00 PM', or press Enter to skip): ").strip()

    preferences_input = input("Preferences (comma-separated, e.g., 'no parking fees, prefer BART'): ").strip()
    preferences = [p.strip() for p in preferences_input.split(',')] if preferences_input else []

    modes = ["drive", "transit", "walk", "rideshare", "bikeshare"]

    print_separator("-")
    print("\n🔍 Planning your route...\n")

    # Build query
    query = {
        "origin": origin or "Palo Alto",
        "destination": destination or "Oracle Park",
        "waypoints": waypoints,
        "arrival_time": arrival_time,
        "preferences": preferences,
        "constraints": []
    }

    print(f"📍 From: {query['origin']}")
    print(f"📍 To: {query['destination']}")
    if waypoints:
        print(f"📍 Via: {', '.join(waypoints)}")
    if arrival_time:
        print(f"⏰ Arrive by: {arrival_time}")
    if preferences:
        print(f"⚙️  Preferences: {', '.join(preferences)}")

    # Initialize planner
    try:
        gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))
        claude_client = anthropic.Client(api_key=os.getenv('ANTHROPIC_API_KEY'))
        planner = RoutePlanner(claude_client, gmaps)

        # Plan routes
        result = await planner.plan_routes(
            f"Get me from {query['origin']} to {query['destination']}" +
            (f" via {', '.join(waypoints)}" if waypoints else "") +
            (f" by {arrival_time}" if arrival_time else "") +
            (f". Preferences: {', '.join(preferences)}" if preferences else "")
        )

        # Display results
        print_route_summary(result['routes'])

        # Show full JSON
        save_json = input("\n💾 Save full JSON response to file? (y/n): ").strip().lower()
        if save_json == 'y':
            filename = f"route_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"✅ Saved to {filename}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


async def test_with_predefined_scenarios():
    """Test with predefined scenarios."""
    print_header("Beeline Route Planner - Predefined Scenarios")

    scenarios = [
        {
            "name": "Morning Commute to SF",
            "query": "Get me from San Jose to Salesforce Tower by 10am. I want to drive to a Caltrain station.",
            "origin": "San Jose",
            "destination": "Salesforce Tower",
            "preferences": ["drive to Caltrain station"],
        },
        {
            "name": "Evening Game at Oracle Park",
            "query": "I'm at Palo Alto downtown. Need to get to Oracle Park by 7pm. Don't want to pay for parking.",
            "origin": "Palo Alto",
            "destination": "Oracle Park",
            "preferences": ["no parking fees"],
        },
        {
            "name": "Morning Ferry Building Trip",
            "query": "From San Mateo to SF Ferry Building by 9am. I prefer BART over Caltrain.",
            "origin": "San Mateo",
            "destination": "SF Ferry Building",
            "preferences": ["prefer BART"],
        },
    ]

    print("\n📋 Available scenarios:\n")
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario['name']}")
        print(f"   Query: {scenario['query']}\n")

    choice = input("Select scenario (1-3) or press Enter for all: ").strip()

    if choice and choice.isdigit():
        selected = [scenarios[int(choice) - 1]]
    else:
        selected = scenarios

    # Initialize planner
    try:
        gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))
        claude_client = anthropic.Client(api_key=os.getenv('ANTHROPIC_API_KEY'))
        planner = RoutePlanner(claude_client, gmaps)

        for scenario in selected:
            print_header(f"Testing: {scenario['name']}")
            print(f"\n📝 Query: {scenario['query']}\n")

            result = await planner.plan_routes(scenario['query'])
            print_route_summary(result['routes'])

            if len(selected) > 1:
                input("\nPress Enter to continue to next scenario...")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


async def test_prompt_template():
    """Test the prompt template directly."""
    print_header("Beeline Route Planner - Test Prompt Template")

    print("\n📝 Enter details to generate the prompt:\n")

    start_address = input("Start address: ").strip() or "Palo Alto"
    end_address = input("End address: ").strip() or "Oracle Park"
    waypoints_input = input("Waypoints (comma-separated): ").strip()
    waypoints = [w.strip() for w in waypoints_input.split(',')] if waypoints_input else []
    modes = ["drive", "transit", "walk", "rideshare", "bikeshare"]

    preferences_input = input("User preferences: ").strip()
    preferences = preferences_input if preferences_input else "none specified"

    # Generate the prompt using the template
    prompt = f"""You are an AI assistant that helps users navigate multi-modally.
You can split the trip into legs where each leg uses a dedicated mode.

Optimize:
1. Reduce the number of transfers
2. Reduce the overall walking time
3. Reduce the overall trip time
4. Use transit to go as far as possible without transfers
5. Consider ride sharing or bike sharing for first/last mile
6. When driving suggest the best and lowest cost parking options. Only suggest driving if it is the first leg of a trip.

The user's ask is to plan a path using the following information:

start_address={start_address}
end_address={end_address}
waypoint_addresses={waypoints if waypoints else []}
modes={modes}

Available route data:
- Full driving route: 45 min, 30.0 miles
- Full transit route: 60 min, 25.0 miles
- User preferences: {preferences}

Generate 2-3 optimal multi-modal route options. Return ONLY a JSON array (no markdown, no explanation) with this structure:
[
  {{
    "id": "route_1",
    "summary": "Brief description of the route",
    "total_duration": 65,
    "total_cost": 12.50,
    "time_savings": 15,
    "carbon_savings": 8.5,
    "legs": [...]
  }}
]

Remember: Only use driving as the first leg. Optimize for fewer transfers and minimal walking."""

    print_separator("-")
    print("\n📋 Generated Prompt Template:\n")
    print(prompt)
    print_separator("-")

    test_with_llm = input("\n🤖 Send this to Claude API? (y/n): ").strip().lower()

    if test_with_llm == 'y':
        try:
            claude_client = anthropic.Client(api_key=os.getenv('ANTHROPIC_API_KEY'))

            print("\n⏳ Calling Claude API...\n")

            response = claude_client.messages.create(
                model="claude-3-5-sonnet-20250219",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text.strip()

            # Remove markdown if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]

            print("✅ Claude Response:\n")
            print(content)

            # Try to parse as JSON
            try:
                routes = json.loads(content)
                print_route_summary(routes)
            except json.JSONDecodeError:
                print("\n⚠️  Response is not valid JSON, but here it is:")
                print(content)

        except Exception as e:
            print(f"\n❌ Error calling Claude API: {e}")


async def main():
    """Main entry point."""
    # Check environment variables
    if not os.getenv('GOOGLE_MAPS_API_KEY'):
        print("❌ Error: GOOGLE_MAPS_API_KEY environment variable not set")
        print("Run: export GOOGLE_MAPS_API_KEY=your_key")
        sys.exit(1)

    if not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("Run: export ANTHROPIC_API_KEY=your_key")
        sys.exit(1)

    while True:
        print_header("Beeline Route Planner Test Suite")
        print("\nChoose a test mode:\n")
        print("1. Custom Input - Enter your own route details")
        print("2. Predefined Scenarios - Test with example queries")
        print("3. Test Prompt Template - See and test the prompt template")
        print("4. Exit")

        choice = input("\nSelect option (1-4): ").strip()

        if choice == "1":
            await test_with_custom_input()
        elif choice == "2":
            await test_with_predefined_scenarios()
        elif choice == "3":
            await test_prompt_template()
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please select 1-4.")

        print("\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
        sys.exit(0)
