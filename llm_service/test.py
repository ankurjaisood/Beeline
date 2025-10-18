import asyncio
import websockets
import json
from mcp import ClientSession

# MCP server configuration
MCP_SERVER_URL = "ws://localhost:3000/mcp"

async def get_location_info(session: ClientSession, address: str):
    """Get location information and analysis using the MCP server."""
    result = await session.call_tool(
        "geocode",
        {"address": address}
    )
    return result

async def get_directions_with_context(session: ClientSession, origin: str, destination: str, mode: str = "transit"):
    """Get directions and travel tips using the MCP server."""
    result = await session.call_tool(
        "get_directions",
        {
            "origin": origin,
            "destination": destination,
            "mode": mode
        }
    )
    return result

async def validate_address(session: ClientSession, address: str, region_code: str = "US", locality: str = ""):
    """Validate an address using the MCP server."""
    result = await session.call_tool(
        "validate_address",
        {
            "address": address,
            "region_code": region_code,
            "locality": locality
        }
    )
    return result

async def main():
    """Main function to test the MCP integration."""
    async with websockets.connect(MCP_SERVER_URL) as websocket:
        # Initialize the session
        await websocket.send(json.dumps({
            "type": "initialize"
        }))
        response = await websocket.recv()
        print("Session initialized:", response)
        
        # Test location analysis
        print("\nTesting location analysis...")
        await websocket.send(json.dumps({
            "type": "toolCall",
            "tool": "geocode",
            "params": {
                "address": "1600 Amphitheatre Parkway, Mountain View, CA"
            }
        }))
        location_info = json.loads(await websocket.recv())
        print("\nLocation Analysis:")
        if "error" in location_info:
            print("Error:", location_info["error"])
        else:
            geocode_result = location_info.get('geocode_result', [{}])[0]
            print("Formatted Address:", geocode_result.get('formatted_address'))
            geometry = geocode_result.get('geometry', {})
            location = geometry.get('location', {})
            print("Coordinates: Lat:", location.get('lat'), "Lng:", location.get('lng'))
            if 'analysis' in location_info:
                print("\nClaude's Analysis:", location_info['analysis'])
        
        # Test directions with context
        print("\nTesting directions...")
        await websocket.send(json.dumps({
            "type": "toolCall",
            "tool": "get_directions",
            "params": {
                "origin": "1600 Amphitheatre Parkway, Mountain View, CA",
                "destination": "San Francisco International Airport",
                "mode": "driving"  # Using driving mode for more reliable results
            }
        }))
        route_info = json.loads(await websocket.recv())
        print("\nRoute Information:")
        if "error" in route_info:
            print("Error:", route_info["error"])
        else:
            directions = route_info.get('directions', [{}])[0]
            if 'legs' in directions:
                leg = directions['legs'][0]
                print("Distance:", leg.get('distance', {}).get('text'))
                print("Duration:", leg.get('duration', {}).get('text'))
                if 'travel_tips' in route_info:
                    print("\nTravel Tips:", route_info['travel_tips'])
        
        # Test address validation
        print("\nTesting address validation...")
        await websocket.send(json.dumps({
            "type": "toolCall",
            "tool": "validate_address",
            "params": {
                "address": "1600 Amphitheatre Parkway, Mountain View, CA 94043",  # Using a more complete address
                "region_code": "US"
            }
        }))
        validation_info = json.loads(await websocket.recv())
        print("\nAddress Validation Result:")
        if "error" in validation_info:
            print("Error:", validation_info["error"])
        else:
            result = validation_info.get('result', {})
            address_info = result.get('address', {})
            print("Validated Address:", address_info)
            if 'suggestions' in validation_info:
                print("Suggestions:", validation_info['suggestions'])

if __name__ == "__main__":
    asyncio.run(main())