# utils/config.py

"""
Configuration Module

This module defines global configuration settings for the simulation. It includes:
  - Simulation parameters (tick duration, default number of ticks, etc.)
  - DDIL emulation settings (severity level, which controls drop/obfuscation probabilities)
  - API configuration settings (host, port, etc.)
  - OpenAI API settings (API key, model)
  
These constants are imported and used by various modules across the project.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Simulation Settings
SIMULATION_TICK_DURATION = 2         # Duration (in seconds) per simulation tick.
DEFAULT_NUM_TICKS = 10               # Default number of simulation ticks for testing.

# DDIL Emulation Settings
# DDIL_LEVEL ranges from 1 (mild impairment) to 5 (severe impairment).
DDIL_LEVEL = 2                       # Adjust to simulate different network conditions.

# API Settings (if needed for the API server)
API_HOST = "0.0.0.0"
API_PORT = 5000

# OpenAI API Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Load from .env file
OPENAI_MODEL = "gpt-4o"                      # Model to be used for LLM calls.
