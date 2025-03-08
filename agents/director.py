# agents/director.py

"""
Director Agent Module

This module defines the DirectorAgent class, which is responsible for:
  - Storing the simulation scenario parameters.
  - Initializing the force leader agents (Red and Blue).
  - Orchestrating the simulation by triggering a tick update on each force leader.
  - Aggregating and formatting event logs for display.
  - Handling user commands to adjust simulation parameters.
"""

from agents.force_leader import ForceLeader

class DirectorAgent:
    def __init__(self, scenario_name: str, location: str, situation: str, num_units: int):
        """
        Initialize the DirectorAgent with scenario details.
        
        Args:
            scenario_name (str): The name/identifier of the scenario.
            location (str): The geographical location or coordinates.
            situation (str): A description of the initial situation.
            num_units (int): Number of units per force (applied equally to both forces).
        """
        self.scenario_name = scenario_name
        self.location = location
        self.situation = situation
        self.num_units = num_units
        
        # Event log to store simulation events.
        self.event_logs = []  # Each event is stored as a string.
        
        # Initialize force leader agents for both forces.
        # The ForceLeader class (imported from agents.force_leader) is assumed to handle
        # creating subordinate agents and processing simulation ticks.
        self.red_force = ForceLeader(team_color="Red", num_units=self.num_units, objective="Engage Blue")
        self.blue_force = ForceLeader(team_color="Blue", num_units=self.num_units, objective="Defend Position")
        
        # Global simulation state dictionary.
        self.global_state = {
            "scenario": self.scenario_name,
            "location": self.location,
            "situation": self.situation,
            "tick": 0  # Initial simulation tick.
        }

    def orchestrate_simulation(self):
        """
        Orchestrate one simulation tick:
          - Increment the tick count.
          - Invoke the process_tick method on each force leader.
          - Collect and log all events from the current tick.
        
        Returns:
            list[str]: A list of event strings generated during this tick.
        """
        self.global_state["tick"] += 1
        tick = self.global_state["tick"]
        events_this_tick = []

        # Mark the beginning of a new tick.
        events_this_tick.append(f"--- Tick {tick} ---")

        # Process Red Force tick.
        try:
            red_events = self.red_force.process_tick(self.global_state)
            if isinstance(red_events, list):
                events_this_tick.extend(red_events)
            elif red_events:
                events_this_tick.append(red_events)
        except Exception as e:
            events_this_tick.append(f"Error in Red Force tick processing: {e}")

        # Process Blue Force tick.
        try:
            blue_events = self.blue_force.process_tick(self.global_state)
            if isinstance(blue_events, list):
                events_this_tick.extend(blue_events)
            elif blue_events:
                events_this_tick.append(blue_events)
        except Exception as e:
            events_this_tick.append(f"Error in Blue Force tick processing: {e}")

        # Append events from this tick to the global event log.
        self.event_logs.extend(events_this_tick)
        return events_this_tick

    def get_latest_feed(self) -> str:
        """
        Retrieve the most recent events as a formatted string.
        
        Returns:
            str: The concatenated string of events from the latest simulation tick.
        """
        if not self.event_logs:
            return "No events logged yet."

        # Find the start index of the most recent tick by looking for the last tick marker.
        last_tick_index = None
        for i in range(len(self.event_logs) - 1, -1, -1):
            if self.event_logs[i].startswith("--- Tick"):
                last_tick_index = i
                break

        if last_tick_index is not None:
            latest_events = self.event_logs[last_tick_index:]
            return "\n".join(latest_events)
        else:
            return "\n".join(self.event_logs)

    def receive_user_command(self, command: str):
        """
        Process a user command that modifies the simulation.
        
        This can include commands such as:
          - "pause", "rewind", "fast forward"
          - Redirecting orders (e.g., "redirect red force: move to point A")
        
        Args:
            command (str): The command input by the user.
        """
        cmd_lower = command.lower()
        if cmd_lower == "pause":
            self.event_logs.append("Simulation paused by user command.")
            # Additional logic to pause the simulation would be implemented here.
        elif cmd_lower == "rewind":
            self.event_logs.append("Simulation rewound by user command.")
            # Implement rewind logic as needed.
        elif cmd_lower == "fast forward":
            self.event_logs.append("Simulation fast-forwarded by user command.")
            # Adjust simulation speed accordingly.
        elif "redirect" in cmd_lower:
            # Example: "redirect red force: move to point A"
            if "red" in cmd_lower:
                self.red_force.receive_direct_order(command)
                self.event_logs.append(f"Red Force received command: {command}")
            elif "blue" in cmd_lower:
                self.blue_force.receive_direct_order(command)
                self.event_logs.append(f"Blue Force received command: {command}")
            else:
                self.event_logs.append(f"Unrecognized redirection command: {command}")
        else:
            self.event_logs.append(f"Command not recognized: {command}")

# Simple test harness for module debugging.
if __name__ == "__main__":
    # Initialize a DirectorAgent for testing.
    director = DirectorAgent("Test Scenario", "Testville", "Initial situation details", 3)
    print("Initial Feed:")
    print(director.get_latest_feed())
    
    # Run a few simulation ticks.
    for i in range(3):
        events = director.orchestrate_simulation()
        print("\n".join(events))
    
    # Test receiving a user command.
    director.receive_user_command("redirect red force: move to north sector")
    print("\nLatest Feed After Command:")
    print(director.get_latest_feed())
