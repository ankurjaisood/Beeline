import os
import logging
from typing import Any, Optional
from datetime import datetime
import googlemaps
import anthropic
import uvicorn
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI()

# Initialize clients
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))
claude = anthropic.Client(api_key=os.getenv('ANTHROPIC_API_KEY'))

class GeocodingInput(BaseModel):
    address: str

class DirectionsInput(BaseModel):
    origin: str
    destination: str
    mode: str = "transit"

class AddressValidationInput(BaseModel):
    address: str
    region_code: str = "US"
    locality: str = ""

class MCPTools:
    """Class to handle MCP tool implementations."""
    
    def __init__(self):
        """Initialize the tools."""
        self.tools = {}
        self.setup_tools()
    
    def get_claude_analysis(self, prompt: str) -> Optional[str]:
        """Get analysis from Claude with error handling."""
        try:
            analysis = claude.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            return analysis.content
        except Exception as e:
            logger.warning("Claude analysis failed: %s", e)
            return None
        
    def setup_tools(self):
        """Set up all the tool implementations."""
        async def geocode(params: GeocodingInput) -> dict:
            """Geocode an address and get Claude's analysis."""
            try:
                # Get geocoding result
                geocode_result = gmaps.geocode(params.address)
                
                if not geocode_result:
                    return {"error": "No results found for the address"}
                    
                location = geocode_result[0]
                formatted_address = location["formatted_address"]
                
                # Get optional Claude analysis
                analysis = self.get_claude_analysis(
                    f"Analyze this location and provide interesting facts about it: {formatted_address}"
                )
                
                return {
                    "geocode_result": geocode_result,
                    "analysis": analysis if analysis else "Analysis unavailable"
                }
                
            except Exception as e:
                logger.exception("Geocoding error: %s", e)
                return {"error": f"Geocoding failed: {str(e)}"}

        async def get_directions(params: DirectionsInput) -> dict:
            """Get directions between two locations and Claude's travel tips."""
            try:
                now = datetime.now()
                directions_result = gmaps.directions(
                    params.origin,
                    params.destination,
                    mode=params.mode,
                    departure_time=now
                )
                
                if not directions_result:
                    return {"error": "No route found between the specified locations"}
                    
                route = directions_result[0]['legs'][0]
                distance = route['distance']['text']
                duration = route['duration']['text']
                
                # Get optional Claude analysis
                tips = self.get_claude_analysis(
                    f"Provide travel tips for a journey from {params.origin} to {params.destination}. "
                    f"The distance is {distance} and it takes {duration} by {params.mode}. "
                    f"Consider the mode of transport, distance, and duration in your tips."
                )
                
                return {
                    "directions": directions_result,
                    "travel_tips": tips if tips else "Travel tips unavailable"
                }
                
            except Exception as e:
                logger.exception("Directions error: %s", e)
                return {"error": f"Failed to get directions: {str(e)}"}

        async def validate_address(params: AddressValidationInput) -> dict:
            """Validate an address and get Claude's suggestions for improvement if needed."""
            try:
                validation_result = gmaps.addressvalidation(
                    [params.address],
                    regionCode=params.region_code,
                    locality=params.locality if params.locality else None,
                    enableUspsCass=True
                )
                
                if not validation_result or 'result' not in validation_result:
                    return {
                        "error": "Address validation failed: Invalid or incomplete response from Google Maps API",
                        "validation_result": validation_result
                    }
                    
                result = validation_result.get('result', {})
                address_data = result.get('address', {})
                
                # If address has issues, get optional Claude suggestions
                if address_data.get('missingComponentTypes') or address_data.get('unresolvedTokens'):
                    suggestions = self.get_claude_analysis(
                        f"This address has some issues. Please suggest improvements for: {params.address}\n"
                        f"Missing components: {address_data.get('missingComponentTypes', [])}\n"
                        f"Unresolved parts: {address_data.get('unresolvedTokens', [])}"
                    )
                    if suggestions:
                        validation_result['suggestions'] = suggestions
                
                return validation_result
                
            except Exception as e:
                logger.exception("Address validation error: %s", e)
                return {"error": f"Address validation failed: {str(e)}"}
            
        # Register the tools
        self.tools = {
            "geocode": geocode,
            "get_directions": get_directions,
            "validate_address": validate_address
        }

@app.websocket("/mcp")
async def mcp_endpoint(websocket: WebSocket):
    """WebSocket endpoint for MCP communication."""
    await websocket.accept()
    mcp_tools = MCPTools()
    
    try:
        while True:
            try:
                data = await websocket.receive_json()
                logger.info("Received request: %s", data.get('type'))
                
                if data["type"] == "initialize":
                    # Initialize session
                    await websocket.send_json({"status": "initialized"})
                    continue
                    
                elif data["type"] == "toolCall":
                    tool = data["tool"]
                    if tool not in mcp_tools.tools:
                        await websocket.send_json({"error": f"Unknown tool: {tool}"})
                        continue
                    
                    if "params" not in data:
                        await websocket.send_json({"error": "Missing required parameters"})
                        continue
                        
                    try:
                        # Parse parameters based on tool type
                        params = None
                        try:
                            if tool == "geocode":
                                params = GeocodingInput(**data["params"])
                            elif tool == "get_directions":
                                params = DirectionsInput(**data["params"])
                            elif tool == "validate_address":
                                params = AddressValidationInput(**data["params"])
                        except Exception as e:
                            await websocket.send_json({
                                "error": f"Invalid parameters: {str(e)}"
                            })
                            continue
                            
                        logger.info("Executing tool: %s", tool)
                        result = await mcp_tools.tools[tool](params)
                        logger.info("Tool execution completed")
                        await websocket.send_json(result)
                        
                    except Exception as e:
                        logger.exception("Tool execution error: %s", e)
                        await websocket.send_json({
                            "error": f"Tool execution failed: {str(e)}"
                        })
                    
            except Exception as e:
                logger.exception("Error processing message: %s", e)
                await websocket.send_json({"error": str(e)})
                
    except Exception as e:
        logger.exception("WebSocket error: %s", e)
    finally:
        try:
            await websocket.close()
        except Exception:
            pass

def main():
    """Main function to run the FastAPI server."""
    try:
        # Check required environment variables
        missing_vars = []
        for var in ['ANTHROPIC_API_KEY', 'GOOGLE_MAPS_API_KEY']:
            if not os.getenv(var):
                missing_vars.append(var)
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        logger.info("Starting MCP Server with Google Maps and Claude integration")
        logger.info("Available tools: geocode, get_directions, validate_address")
        
        # Start the FastAPI server
        uvicorn.run(app, host="0.0.0.0", port=3000)
        return 0
        
    except Exception as e:
        logger.exception("Server error: %s", e)
        return 1

if __name__ == "__main__":
    exit(main())