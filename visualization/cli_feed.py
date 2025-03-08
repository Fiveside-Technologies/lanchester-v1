# visualization/cli_feed.py

"""
CLI Feed Visualization Module

This module provides functionality to display simulation event feeds in the terminal
with color and formatting using the Rich library. The display_feed() function formats
the feed text, applies color highlighting, and outputs it to the console.
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()

def display_feed(feed_text: str):
    """
    Display the given simulation event feed in a formatted and colored manner on the terminal.
    
    Args:
        feed_text (str): The multi-line string feed containing simulation events.
    
    Functionality:
        - Splits the feed into lines.
        - Applies color formatting based on keywords (e.g., "Tick", "decision", "Error").
        - Displays the formatted feed in a panel for better readability.
    """
    try:
        # Split feed into individual lines.
        lines = feed_text.split("\n")
        formatted_lines = []
        
        for line in lines:
            # Create a Rich Text object for each line.
            text = Text(line)
            
            # Apply different styles based on keywords.
            if line.startswith("--- Tick"):
                text.stylize("bold yellow")
            elif "Error" in line:
                text.stylize("bold red")
            elif "decision" in line.lower():
                text.stylize("green")
            elif "received" in line.lower():
                text.stylize("cyan")
            else:
                text.stylize("white")
                
            formatted_lines.append(text)
        
        # Combine all formatted lines into a single text object with newlines.
        combined_text = Text("\n").join(formatted_lines)
        
        # Display the feed within a styled panel.
        panel = Panel(combined_text, title="Simulation Feed", border_style="blue", box=box.ROUNDED)
        console.print(panel)
    except Exception as e:
        console.print(f"[bold red]Error displaying feed: {str(e)}[/bold red]")


# Simple test harness for the CLI Feed visualization module.
if __name__ == "__main__":
    sample_feed = (
        "--- Tick 1 ---\n"
        "Red_Squad_1 decision: Advance to position (10, 15).\n"
        "Blue_Squad_1 decision: Hold position at (20, 30).\n"
        "Red Leader Decision: Attack blue force at checkpoint.\n"
        "Blue Leader Decision: Request support and reposition.\n"
        "--- Tick 2 ---\n"
        "Red_Squad_1 decision: Engage enemy unit near (12, 18).\n"
        "Blue_Squad_1 decision: Fall back to defensive position.\n"
        "Red Leader Decision: Continue pressure on enemy flank.\n"
        "Blue Leader Decision: Reinforce frontline units.\n"
        "Error in processing: Communication timeout."
    )
    
    display_feed(sample_feed)
