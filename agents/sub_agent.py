# agents/sub_agent.py

"""
Sub Agent Module

This module defines the SubAgent class, representing a lower-level unit (e.g., a squad commander)
within a force. Each SubAgent:
  - Maintains an internal state (position, status, and decision history).
  - Processes each simulation tick by generating a decision via an LLM call (simulated here).
  - Updates its context with new messages (e.g., direct orders or simulation feedback).

The decisions generated here simulate what a real-world squad commander might do given the
current operational context.
"""

import random
import openai

class SubAgent:
    def __init__(self, id: str, role: str):
        """
        Initialize a SubAgent with a unique identifier and role.
        
        Args:
            id (str): Unique identifier for the agent (e.g., "Red_Squad_1").
            role (str): The role of the agent (e.g., "Squad Commander").
        """
        self.id = id
        self.role = role
        # Initialize internal state; for example, a starting position (x, y coordinates) on a simple grid.
        self.position = (random.randint(0, 100), random.randint(0, 100))
        self.status = "Ready"
        # Memory/context log for the agent, storing all incoming messages and past decisions.
        self.context = []
    
    def process_tick(self, local_state: dict):
        """
        Process one simulation tick.
        
        This function uses the agent's internal context, current state, and the provided local_state
        to generate a decision (via an OpenAI API call). The decision simulates an action (e.g., move,
        hold position, engage target) and updates the agent's internal state accordingly.
        
        Args:
            local_state (dict): The local state or environmental context relevant to this agent.
        
        Returns:
            str: A descriptive event string summarizing the decision and action.
        """
        # Update the context with current simulation info.
        prompt_context = f"Agent ID: {self.id}\n" \
                         f"Role: {self.role}\n" \
                         f"Current Position: {self.position}\n" \
                         f"Status: {self.status}\n" \
                         f"Local State: {local_state}\n" \
                         "Past Context:\n" + "\n".join(self.context[-5:])  # include last 5 messages
        
        # Construct a prompt asking the agent what its next action should be.
        prompt = (
            f"{prompt_context}\n"
            "Based on the above, decide on your next tactical action. "
            "Possible actions include: advancing to a new position, holding position, or engaging an enemy. "
            "Provide a concise description of the chosen action and update your position if applicable."
        )
        
        try:
            # Call the OpenAI API to generate the decision.
            client = openai.OpenAI()
            completion = client.chat.completions.create(
                model="gpt-4o",
                store=True,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            decision = completion.choices[0].message.get("content", "No decision generated.")
        except Exception as e:
            decision = f"Error generating decision: {str(e)}"
        
        # Simulate updating internal state based on decision.
        # For the sake of this MVP, we'll simulate movement if "advance" or "move" is in the decision.
        decision_lower = decision.lower()
        if "advance" in decision_lower or "move" in decision_lower:
            # Randomly update position to simulate movement.
            delta = random.randint(1, 10)
            new_x = self.position[0] + delta
            new_y = self.position[1] + delta
            old_position = self.position
            self.position = (new_x, new_y)
            decision += f" [Movement: position updated from {old_position} to {self.position}]."
        else:
            decision += " [No movement executed]."
        
        # Append the decision to the agent's context for future reference.
        self.context.append(decision)
        
        # Return a formatted event string.
        event = f"{self.id} decision: {decision}"
        return event

    def update_context(self, message: str):
        """
        Update the agent's internal context with a new message.
        
        Args:
            message (str): The message or order to add to the agent's context.
        """
        self.context.append(message)


# Simple test harness for the SubAgent module.
if __name__ == "__main__":
    # Create a test sub-agent.
    agent = SubAgent(id="Test_Squad_1", role="Squad Commander")
    
    # Define a simple local state for simulation.
    local_state = {"tick": 1, "weather": "clear", "enemy_presence": "low"}
    
    # Process a simulation tick and print the decision.
    event = agent.process_tick(local_state)
    print("Simulation Tick Event:")
    print(event)
    
    # Update context with a direct order and print the updated context.
    agent.update_context("Received direct order: Hold position at current coordinates.")
    print("\nUpdated Context:")
    for ctx in agent.context:
        print(ctx)
