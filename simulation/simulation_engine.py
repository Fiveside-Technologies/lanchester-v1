# simulation/simulation_engine.py

"""
Simulation Engine Module

This module defines the SimulationEngine class that:
  - Maintains the simulation clock.
  - Invokes the DirectorAgent's orchestrate_simulation() method each tick.
  - Retrieves the raw event feed and passes it through the DDIL emulation module.
  - Returns both the raw and DDIL-modified feeds for further consumption (e.g., visualization or API endpoints).

The simulation loop is designed to simulate real-time progression by incorporating a fixed delay between ticks.
"""

import time
from simulation.ddil_emulation import process_feed

class SimulationEngine:
    def __init__(self, director):
        """
        Initialize the SimulationEngine with the DirectorAgent instance.
        
        Args:
            director: An instance of the DirectorAgent class.
        """
        self.director = director
        self.tick_duration = 2  # Duration per simulation tick in seconds (can be made configurable)
        self.current_tick = 0

    def update(self):
        """
        Process one simulation tick:
          - Increment the simulation clock.
          - Invoke the DirectorAgent's orchestrate_simulation() to update the state and generate events.
          - Concatenate the raw events into a feed.
          - Process the raw feed through the DDIL emulation module.
        
        Returns:
            tuple: A pair (raw_feed, ddil_feed) containing both the unmodified and modified event feeds.
        """
        # Increment simulation clock.
        self.current_tick += 1

        # Run one tick of simulation via the DirectorAgent.
        raw_events = self.director.orchestrate_simulation()  # Returns a list of event strings.
        raw_feed = "\n".join(raw_events)  # Concatenate list into a single string feed.

        # Process raw feed to simulate network disruptions using DDIL emulation.
        ddil_feed = process_feed(raw_feed)
        
        return raw_feed, ddil_feed

    def run(self, num_ticks=10):
        """
        Run the simulation loop for a specified number of ticks.
        
        Args:
            num_ticks (int): The total number of simulation ticks to run.
        """
        for tick in range(num_ticks):
            print(f"Simulation Tick: {self.current_tick + 1}")
            raw_feed, ddil_feed = self.update()
            
            # For now, simply print the feeds.
            print("Raw Feed:")
            print(raw_feed)
            print("\nDDIL Modified Feed:")
            print(ddil_feed)
            print("-" * 40)
            
            # Delay between ticks to simulate real time.
            time.sleep(self.tick_duration)


# Test harness for the SimulationEngine module.
if __name__ == "__main__":
    # For testing, create a DirectorAgent instance.
    from agents.director import DirectorAgent

    # Instantiate DirectorAgent with sample scenario parameters.
    director = DirectorAgent(scenario_name="Test Scenario",
                             location="Test Location",
                             situation="Initial Situation Description",
                             num_units=2)
    
    # Create and run the simulation engine.
    sim_engine = SimulationEngine(director=director)
    sim_engine.run(num_ticks=5)
