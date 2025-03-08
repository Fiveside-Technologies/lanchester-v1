# visualization/map_view.py

"""
Map View Visualization Module

This module uses matplotlib to provide a simple, real-time map view of the simulation.
It plots markers for agents based on their (x, y) positions and updates the display on each call.

Functions:
    - update_map(positions): Accepts a dictionary of agent positions and updates the plot.
    
Usage:
    This module is intended to be imported and called by the simulation engine to update the map.
    A test harness is included to simulate agent movement.
"""

import matplotlib.pyplot as plt
import time

# Initialize matplotlib interactive mode so the figure updates dynamically.
plt.ion()

def update_map(positions: dict):
    """
    Update the map view with the current agent positions.
    
    Args:
        positions (dict): A dictionary where keys are agent IDs (str) and values are (x, y) tuples.
        
    Functionality:
        - Clears the current figure.
        - Plots each agent's position as a scatter point.
        - Annotates each marker with the agent's ID.
        - Sets appropriate axis labels and title.
        - Calls plt.pause() to force the GUI to update.
    """
    plt.clf()  # Clear current figure
    # Extract x and y coordinates along with labels
    x_coords = [pos[0] for pos in positions.values()]
    y_coords = [pos[1] for pos in positions.values()]
    labels = list(positions.keys())
    
    # Plot markers for each agent
    plt.scatter(x_coords, y_coords, color='blue')
    
    # Annotate each marker with its agent ID.
    for agent_id, pos in positions.items():
        plt.text(pos[0] + 1, pos[1] + 1, agent_id, fontsize=9, color='darkred')
    
    # Set plot title and labels.
    plt.title("Simulation Map View")
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    
    # Set fixed axis limits (adjust as needed)
    plt.xlim(0, 150)
    plt.ylim(0, 150)
    
    # Force the figure to update.
    plt.draw()
    plt.pause(0.1)

# Test harness to simulate map view updates.
if __name__ == "__main__":
    # Example: simulate 5 agents with starting positions.
    positions = {
        "Red_Squad_1": (10, 20),
        "Red_Squad_2": (30, 40),
        "Blue_Squad_1": (50, 60),
        "Blue_Squad_2": (70, 80),
        "Blue_Squad_3": (90, 100)
    }
    
    # Create a figure for the map view.
    plt.figure(figsize=(6, 6))
    
    # Simulate movement over 20 iterations.
    for i in range(20):
        # Update positions with a small random movement.
        for key in positions:
            x, y = positions[key]
            # Simple simulation: move each unit a small step randomly in x and y.
            positions[key] = (x + (i % 3) * 2, y + ((i + 1) % 3) * 2)
        
        update_map(positions)
        time.sleep(0.5)
    
    # Keep the window open until manually closed.
    plt.ioff()
    plt.show()
