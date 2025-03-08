# api/api_server.py

"""
API Server Module

This module defines a simple API server that exposes endpoints to:
  - Retrieve the current simulation feed (raw or DDIL-modified).
  - Submit commands to the simulation (e.g., pause, rewind, or direct orders).
  - Retrieve the current simulation status.

For this MVP, we maintain global instances of the DirectorAgent and SimulationEngine.
The simulation is updated with each GET request to /feed for demonstration purposes.

Usage:
    Run the server with: uvicorn api.api_server:app --reload
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Import our simulation components.
from agents.director import DirectorAgent
from simulation.simulation_engine import SimulationEngine

# Create global simulation instances for this MVP.
director = DirectorAgent(
    scenario_name="API Test Scenario",
    location="API Test Location",
    situation="API Test Situation",
    num_units=2
)
sim_engine = SimulationEngine(director=director)

# Create the FastAPI app.
app = FastAPI(title="Generative AI Tactical Simulation API", version="1.0")

class CommandRequest(BaseModel):
    command: str

@app.get("/feed")
def get_feed(feed_type: Optional[str] = "raw"):
    """
    Retrieve the current simulation feed.

    Query Parameters:
        feed_type (str): 'raw' returns the unmodified simulation feed; 'ddil' returns the feed
                         modified by the DDIL emulation module.
    
    Returns:
        dict: A dictionary containing the feed type and feed content.
    """
    try:
        # For demonstration, update the simulation on each GET.
        raw_feed, ddil_feed = sim_engine.update()
        if feed_type.lower() == "raw":
            return {"feed_type": "raw", "feed": raw_feed}
        elif feed_type.lower() == "ddil":
            return {"feed_type": "ddil", "feed": ddil_feed}
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid feed_type parameter. Use 'raw' or 'ddil'."
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving feed: {str(e)}")

@app.post("/command")
def post_command(cmd_request: CommandRequest):
    """
    Submit a command to the simulation.

    Request Body:
        command (str): The command string to be processed (e.g., 'pause', 'rewind', 
                       'redirect red force: move to point A').
    
    Returns:
        dict: A confirmation message with the submitted command.
    """
    try:
        director.receive_user_command(cmd_request.command)
        return {"status": "Command received", "command": cmd_request.command}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing command: {str(e)}")

@app.get("/status")
def get_status():
    """
    Retrieve the current simulation status.

    Returns:
        dict: Information about the current simulation state including scenario details and tick count.
    """
    status = {
        "scenario_name": director.scenario_name,
        "location": director.location,
        "situation": director.situation,
        "current_tick": sim_engine.current_tick,
    }
    return status

# To run the API server directly from this script.
if __name__ == "__main__":
    uvicorn.run("api.api_server:app", host="0.0.0.0", port=5000, reload=True)
