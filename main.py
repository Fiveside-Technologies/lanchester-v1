# main.py
import time
from agents.director import DirectorAgent
from simulation.simulation_engine import SimulationEngine
from visualization.cli_feed import display_feed

def main():
    # Welcome message
    print("==============================================")
    print("  Generative AI Tactical Simulation Test")
    print("==============================================\n")
    
    # Get scenario inputs from the user
    scenario_name = input("Enter scenario name: ")
    location = input("Enter location (e.g., coordinates or city name): ")
    situation = input("Enter initial situation description: ")
    num_units_input = input("Enter number of units (default 4): ")
    num_units = int(num_units_input) if num_units_input.strip() else 4

    # Initialize the Director Agent with scenario details
    director = DirectorAgent(
        scenario_name=scenario_name,
        location=location,
        situation=situation,
        num_units=num_units
    )
    
    # Initialize the simulation engine with the director agent
    sim_engine = SimulationEngine(director=director)
    
    print("\nStarting simulation...\n")
    
    # Run a simulation loop for a fixed number of ticks (e.g., 10 ticks)
    num_ticks = 10
    for tick in range(num_ticks):
        print(f"--- Tick {tick + 1} ---")
        sim_engine.update()  # Update simulation state (agents act, events are generated)
        
        # Get the latest event feed from the director agent
        feed_text = director.get_latest_feed()
        display_feed(feed_text)  # Display the feed in the terminal
        
        # Pause to simulate real-time delay (2 seconds per tick)
        time.sleep(2)
    
    print("\nSimulation completed.")

if __name__ == "__main__":
    main()
