# main.py
import time
import random
import openai
from agents.director import DirectorAgent
from simulation.simulation_engine import SimulationEngine
from visualization.cli_feed import display_feed
from visualization.map_view import MapRecorder
import matplotlib.pyplot as plt

# Global debug flag
DEBUG_ENABLED = False

def setup_debug_mode():
    # Dummy client that returns a random decision string based on the prompt.
    def dummy_create(model, messages):
        responses = [
            "Advance to the next checkpoint.",
            "Hold the position.",
            "Engage the enemy lightly.",
            "Retreat and regroup.",
            "Scan for enemy movements."
        ]
        if DEBUG_ENABLED:
            print("LLM Input:", messages)
        chosen = random.choice(responses)
        if DEBUG_ENABLED:
            print("LLM Output:", chosen)
        # Create a dummy choice structure.
        class DummyChoice:
            def __init__(self, content):
                self.message = type("Message", (), {"content": content})()
        class DummyCompletion:
            def __init__(self, content):
                self.choices = [DummyChoice(content)]
        return DummyCompletion(chosen)
    
    class DummyLLM:
        def __init__(self):
            self.chat = self
        @property
        def completions(self):
            return self
        def create(self, model, messages):
            return dummy_create(model, messages)
    
    # Monkey patch OpenAI to use the dummy client.
    openai.OpenAI = lambda: DummyLLM()

def main():
    global DEBUG_ENABLED
    print("==============================================")
    print("  Generative AI Tactical Simulation Test")
    print("==============================================\n")
    
    debug_input = input("Enable debug mode? (y/N): ").strip().lower()
    if debug_input == "y":
        DEBUG_ENABLED = True
        setup_debug_mode()
        print("Debug mode enabled: OpenAI API calls will be simulated.\n")
    
    # Option to simulate test inputs
    simulate_mode = input("Enable simulated test inputs? (y/N): ").strip().lower() == "y"
    if simulate_mode:
        def get_input(prompt_text, test_value):
            print(prompt_text)
            print(test_value)
            return test_value
    else:
        def get_input(prompt_text, test_value=None):
            return input(prompt_text)
    
    # Get scenario inputs
    scenario_name = get_input("Enter scenario name: ", "Test conflict")
    location = get_input("Enter location (e.g., coordinates or city name): ", "Kyiv, Ukraine")
    situation = get_input("Enter initial situation description: ", "Blue force is flanked by red force unexpectedly")
    num_units_input = get_input("Enter number of units (default 4): ", "4")
    num_units = int(num_units_input.strip()) if num_units_input.strip() else 4

    # Initialize the Director Agent with scenario details
    director = DirectorAgent(
        scenario_name=scenario_name,
        location=location,
        situation=situation,
        num_units=num_units
    )
    
    # Initialize the simulation engine with the director agent
    sim_engine = SimulationEngine(director=director)
    
    # Create a MapRecorder instance to record frames.
    recorder = MapRecorder(xlim=(0, 150), ylim=(0, 150), output_dir="output", frame_subdir="frames")
    
    print("\nStarting simulation...\n")
    
    # Run the simulation loop for a fixed number of ticks.
    num_ticks = 10
    for tick in range(1, num_ticks + 1):
        print(f"--- Tick {tick} ---")
        sim_engine.update()  # Update simulation state (agents act, events are generated)
        
        # Record the current positions for later GIF and trajectory creation.
        positions = {}
        if hasattr(director, 'red_force'):
            for sub_agent in director.red_force.sub_agents:
                positions[sub_agent.id] = sub_agent.position
        if hasattr(director, 'blue_force'):
            for sub_agent in director.blue_force.sub_agents:
                positions[sub_agent.id] = sub_agent.position
        
        recorder.record_frame(positions, tick)
        
        # Get and display the latest event feed from the director.
        feed_text = director.get_latest_feed()
        display_feed(feed_text)
        
        # Pause to simulate real-time delay.
        time.sleep(2)
    
    print("\nSimulation completed.")
    
    # After simulation, create the GIF and trajectory plot.
    recorder.create_gif(gif_filename="simulation.gif", duration=0.5)
    recorder.create_trajectory_plot(png_filename="trajectories.png")

if __name__ == "__main__":
    main()
