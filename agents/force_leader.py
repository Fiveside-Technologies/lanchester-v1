# agents/force_leader.py

"""
Force Leader Agent Module

This module defines the ForceLeader class, responsible for:
  - Initializing subordinate agents (e.g., squad commanders).
  - Processing each simulation tick by calling subordinate agents' process_tick.
  - Aggregating their events and generating a high-level decision summary via an LLM call.
  - Receiving direct orders and propagating them to subordinate agents.
"""

import openai
from agents.sub_agent import SubAgent

class ForceLeader:
    def __init__(self, team_color: str, num_units: int, objective: str):
        """
        Initialize a ForceLeader with a given team color, number of units, and mission objective.
        
        Args:
            team_color (str): The team identifier (e.g., "Red" or "Blue").
            num_units (int): Number of subordinate agents to create.
            objective (str): The mission objective for this force.
        """
        self.team_color = team_color
        self.num_units = num_units
        self.objective = objective
        self.sub_agents = []  # List to hold subordinate agents
        self.event_logs = []  # Force-level event log

        # Create subordinate agents (for example, one per unit)
        for i in range(1, self.num_units + 1):
            agent_id = f"{self.team_color}_Squad_{i}"
            agent = SubAgent(id=agent_id, role="Squad Commander")
            self.sub_agents.append(agent)

    def process_tick(self, global_state: dict):
        """
        Process a simulation tick for this force leader.
        
        Iterates over subordinate agents to gather their events,
        and then generates a high-level decision summary based on these events.
        
        Args:
            global_state (dict): The overall simulation state (includes current tick).
        
        Returns:
            list[str]: A list of event strings for this tick.
        """
        tick_events = []

        # Process each subordinate agent
        for agent in self.sub_agents:
            try:
                # Each agent returns its events (either a list or a string)
                agent_events = agent.process_tick(global_state)
                if isinstance(agent_events, list):
                    tick_events.extend(agent_events)
                elif agent_events:
                    tick_events.append(agent_events)
            except Exception as e:
                tick_events.append(f"Error processing tick for {agent.id}: {str(e)}")
        
        # Generate a high-level decision summary using an LLM call.
        summary = self.generate_decision_summary(tick_events, global_state)
        tick_events.append(summary)
        
        # Record all events for later retrieval
        self.event_logs.extend(tick_events)
        return tick_events

    def generate_decision_summary(self, subordinate_events, global_state):
        """
        Generate a high-level decision summary using the OpenAI API.
        
        Constructs a prompt from subordinate events and the global state,
        then calls the API to simulate what the force leader would decide next.
        
        Args:
            subordinate_events (list[str]): Events collected from subordinate agents.
            global_state (dict): The global simulation state.
        
        Returns:
            str: A decision summary string from the force leader.
        """
        prompt = f"As the {self.team_color} Force Leader with objective '{self.objective}', " \
                 "review the following events:\n"
        for event in subordinate_events:
            prompt += f"- {event}\n"
        prompt += f"Current simulation tick: {global_state.get('tick')}\n" \
                  "Based on these events, what is the most reasonable next action for your force? " \
                  "Provide a concise summary."

        try:
            # Instantiate the OpenAI client and make the API call.
            client = openai.OpenAI()  # Using our simple OpenAI client interface
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            summary = completion.choices[0].message.content
        except Exception as e:
            summary = f"Error generating decision summary: {str(e)}"
        return f"{self.team_color} Leader Decision: {summary}"

    def receive_direct_order(self, order: str):
        """
        Process a direct order for the force leader.
        
        The order is logged and then broadcast to all subordinate agents.
        
        Args:
            order (str): The direct order to process.
        """
        self.event_logs.append(f"{self.team_color} Leader received direct order: {order}")
        for agent in self.sub_agents:
            # Forward the order to each subordinate agent
            agent.update_context(f"Received direct order: {order}")


# Test harness for the ForceLeader module.
if __name__ == "__main__":
    # Define a simple global state with tick information
    global_state = {"tick": 0}
    # Initialize a ForceLeader for the "Red" team with 2 subordinate agents.
    force_leader = ForceLeader(team_color="Red", num_units=2, objective="Engage Blue")
    
    # Simulate 3 ticks of the simulation.
    for tick in range(3):
        global_state["tick"] = tick + 1
        events = force_leader.process_tick(global_state)
        print(f"\nTick {tick+1} events:")
        for event in events:
            print(event)
    
    # Simulate receiving a direct order.
    force_leader.receive_direct_order("Move to checkpoint Alpha")
    print("\nForce Leader event logs after direct order:")
    for event in force_leader.event_logs:
        print(event)
