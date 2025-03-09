# visualization/map_view.py

"""
Map View Visualization and Recorder Module

This module collects the positions of agents at each simulation tick and, at the end
of the simulation, produces:
  - A GIF animation that replays the simulation (frame-by-frame).
  - A PNG image that shows the trajectory (paths) taken by each agent over time.

All outputs (frames, GIF, PNG) are saved in a main output directory. Within that directory,
frames are stored in a subdirectory (e.g., "output/frames"), and the GIF and PNG are saved
directly in the main output folder.

Usage:
  1. Create a MapRecorder instance at the beginning of the simulation.
  2. At each tick, call record_frame(positions, tick) to record the current positions.
  3. After the simulation is complete, call create_gif() and create_trajectory_plot().
"""

import os
import shutil
import matplotlib.pyplot as plt
import imageio

class MapRecorder:
    def __init__(self, xlim=(0, 150), ylim=(0, 150), output_dir="output", frame_subdir="frames"):
        """
        Initialize the MapRecorder.
        
        Args:
            xlim (tuple): The x-axis limits for the map.
            ylim (tuple): The y-axis limits for the map.
            output_dir (str): The main directory where all outputs will be saved.
            frame_subdir (str): The subdirectory (within output_dir) for frame images.
        """
        self.xlim = xlim
        self.ylim = ylim
        self.output_dir = output_dir
        self.frame_dir = os.path.join(output_dir, frame_subdir)
        self.frames = []  # List to store the filenames of each recorded frame.
        self.all_positions = {}  # Dictionary to store trajectories: {agent_id: [(x,y), ...]}
        
        # Clear or create the main output directory.
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)
        
        # Create the frames subdirectory within the main output directory.
        os.makedirs(self.frame_dir)

    def record_frame(self, positions: dict, tick: int):
        """
        Record the current positions and save a frame image.
        
        Args:
            positions (dict): A dictionary where keys are agent IDs and values are (x, y) tuples.
            tick (int): The current simulation tick.
        """
        # Update each agent's trajectory.
        for agent_id, pos in positions.items():
            if agent_id not in self.all_positions:
                self.all_positions[agent_id] = []
            self.all_positions[agent_id].append(pos)
        
        # Create and configure a new figure for this tick.
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_title(f"Simulation Map View - Tick {tick}")
        ax.set_xlabel("X Position")
        ax.set_ylabel("Y Position")
        ax.set_xlim(*self.xlim)
        ax.set_ylim(*self.ylim)
        
        # Plot current positions.
        for agent_id, pos in positions.items():
            if agent_id.startswith("Red_"):
                color = "red"
            elif agent_id.startswith("Blue_"):
                color = "blue"
            else:
                color = "green"
            marker = "^" if "Leader" in agent_id else "o"
            size = 150 if "Leader" in agent_id else 100
            ax.scatter(pos[0], pos[1], color=color, marker=marker, s=size)
            ax.text(pos[0] + 1, pos[1] + 1, agent_id, fontsize=9, color=color)
        
        # Save the figure to the frames subdirectory.
        frame_filename = os.path.join(self.frame_dir, f"frame_{tick:03d}.png")
        plt.savefig(frame_filename)
        plt.close(fig)
        self.frames.append(frame_filename)
    
    def create_gif(self, gif_filename="simulation.gif", duration=0.5):
        """
        Create a GIF animation from the recorded frames.
        
        Args:
            gif_filename (str): The filename for the output GIF (saved in the main output directory).
            duration (float): Duration (in seconds) between frames in the GIF.
        """
        images = []
        for frame_file in self.frames:
            images.append(imageio.imread(frame_file))
        gif_path = os.path.join(self.output_dir, gif_filename)
        imageio.mimsave(gif_path, images, duration=duration)
        print(f"GIF saved as {gif_path}")
    
    def create_trajectory_plot(self, png_filename="trajectories.png"):
        """
        Create a static plot showing the trajectories taken by each agent.
        
        Args:
            png_filename (str): The filename for the output PNG image (saved in the main output directory).
        """
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_title("Agent Trajectories")
        ax.set_xlabel("X Position")
        ax.set_ylabel("Y Position")
        ax.set_xlim(*self.xlim)
        ax.set_ylim(*self.ylim)
        
        for agent_id, pos_list in self.all_positions.items():
            xs = [p[0] for p in pos_list]
            ys = [p[1] for p in pos_list]
            if agent_id.startswith("Red_"):
                color = "red"
            elif agent_id.startswith("Blue_"):
                color = "blue"
            else:
                color = "green"
            ax.plot(xs, ys, marker="o", color=color, label=agent_id)
            ax.text(xs[-1] + 1, ys[-1] + 1, agent_id, fontsize=9, color=color)
        
        ax.legend()
        trajectory_path = os.path.join(self.output_dir, png_filename)
        plt.savefig(trajectory_path)
        plt.close(fig)
        print(f"Trajectory plot saved as {trajectory_path}")

# Test harness for MapRecorder.
if __name__ == "__main__":
    import time
    recorder = MapRecorder()
    
    # Simulate positions for 5 agents over 20 ticks.
    positions = {
        "Red_Squad_1": (10, 20),
        "Red_Squad_Leader": (15, 25),
        "Blue_Squad_1": (50, 60),
        "Blue_Squad_Leader": (55, 65),
        "Blue_Squad_3": (90, 100)
    }
    
    for tick in range(1, 21):
        # Update positions (simulate movement).
        for key in positions:
            x, y = positions[key]
            positions[key] = (x + 2, y + 2)  # Simple movement update.
        recorder.record_frame(positions, tick)
        time.sleep(0.1)
    
    recorder.create_gif(duration=0.3)
    recorder.create_trajectory_plot()
