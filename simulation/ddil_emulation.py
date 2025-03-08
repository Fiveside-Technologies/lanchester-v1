# simulation/ddil_emulation.py

"""
DDIL Emulation Module

This module defines functionality to emulate Denied, Disrupted, Intermittent, and Limited (DDIL)
communication environments. The process_feed() function takes a raw event feed and applies modifications 
(such as randomly dropping events or obfuscating details) based on a configurable DDIL level.

The DDIL level is retrieved from the configuration in utils/config.py.
"""

import random
from utils.config import DDIL_LEVEL

def process_feed(raw_feed: str) -> str:
    """
    Process the raw simulation feed and apply DDIL modifications.

    This function simulates network impairments by:
      - Randomly dropping some event lines based on a drop probability determined by DDIL level.
      - Randomly obfuscating details in remaining lines (e.g., replacing words longer than 4 characters 
        with placeholder text) to simulate data degradation.

    Args:
        raw_feed (str): The unmodified event feed (a multi-line string).

    Returns:
        str: The modified event feed simulating DDIL effects (the "C2 feed").
    """
    # Determine drop probability based on DDIL_LEVEL.
    # For example, each level adds 10% drop chance up to a maximum of 50%.
    drop_probability = min(DDIL_LEVEL * 0.1, 0.5)
    # Use the same probability for obfuscation.
    obfuscate_probability = drop_probability

    # Split the raw feed into individual lines.
    lines = raw_feed.split("\n")
    modified_lines = []

    for line in lines:
        # Randomly decide whether to drop this line.
        if random.random() < drop_probability:
            continue

        # Randomly decide to obfuscate details in the line.
        if random.random() < obfuscate_probability:
            # Obfuscate words longer than 4 characters with "???"
            words = line.split()
            obfuscated_words = [word if len(word) < 5 else "???" for word in words]
            line = " ".join(obfuscated_words)
        
        modified_lines.append(line)
    
    modified_feed = "\n".join(modified_lines)
    return modified_feed


# Test harness for the DDIL Emulation module.
if __name__ == "__main__":
    # Sample raw feed for testing purposes.
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
        "Blue Leader Decision: Reinforce frontline units."
    )
    
    print("Original Feed:")
    print(sample_feed)
    print("\nModified DDIL Feed:")
    modified = process_feed(sample_feed)
    print(modified)
