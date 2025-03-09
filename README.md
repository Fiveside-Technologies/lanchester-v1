# Lanchester V1

Generative AI Tactical Simulation MVP

## Overview

The **Generative AI Tactical Simulation MVP** is a minimal viable product that demonstrates a multi-agent simulation leveraging generative AI to create a synthetic tactical environment. This project simulates a dynamic battlefield by using hierarchical agents (Director, Force Leaders, and SubAgents) that interact via LLM-based decision-making (using the OpenAI API). The simulation features:

-   A **CLI feed** that displays formatted, colored event updates.
-   A **map view** that visualizes real-time unit positions.
-   A simulation engine that advances through time ticks.
-   DDIL (Denied, Disrupted, Intermittent, Limited) network emulation to simulate realistic communication impairments.
-   An API server (using FastAPI) to expose simulation data and accept user commands.

## Features

-   **Hierarchical Agent Architecture:**

    -   **DirectorAgent:** Orchestrates the simulation and aggregates events.
    -   **ForceLeader Agents:** Manage groups (e.g., Red and Blue forces) and generate high-level decisions.
    -   **SubAgent:** Represents individual units/squad commanders that generate tactical actions.

-   **Real-Time Simulation:**

    -   The simulation engine processes ticks (time steps), updating agent states and events.
    -   Each tick simulates real-time delay and communication among agents.

-   **LLM Integration:**

    -   Agents use OpenAI API calls to generate decisions based on current context and simulation state.

-   **DDIL Emulation:**

    -   A dedicated module simulates network impairments (e.g., message drops or obfuscation) to mimic tactical communication challenges.

-   **Visualizations:**

    -   **CLI Feed:** Uses the Rich library for colored, formatted output.
    -   **Map View:** Uses matplotlib to display a graphical, real-time map of agent positions.

-   **API Server:**
    -   Exposes endpoints for accessing simulation feeds, submitting commands, and retrieving simulation status via FastAPI.

## File Structure

```
project_root/
├── main.py
├── agents/
│   ├── director.py
│   ├── force_leader.py
│   └── sub_agent.py
├── simulation/
│   ├── simulation_engine.py
│   └── ddil_emulation.py
├── api/
│   └── api_server.py
├── visualization/
│   ├── cli_feed.py
│   └── map_view.py
└── utils/
    ├── config.py
    └── helpers.py
```

## Installation

### Requirements

-   **Python 3.8+**
-   Required Python packages

### Installing Dependencies

To install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Simulation (CLI Mode)

To run the simulation from the command line, execute:

```bash
python main.py
```

This will prompt you to enter scenario details (such as scenario name, location, situation description, and number of units) and then start the simulation loop. You will see formatted event feeds in your terminal as the simulation progresses.

### Running the API Server

To start the API server (which uses FastAPI), run:

```bash
uvicorn api.api_server:app --reload
```

The API server will be available at http://0.0.0.0:5000/. Endpoints include:

-   `GET /feed?feed_type=raw|ddil`: Retrieve the simulation feed (raw or modified by DDIL emulation).
-   `POST /command`: Submit commands to the simulation (e.g., "pause", "rewind", or "redirect red force: move to point A").

Example JSON payload:

```json
{
    "command": "redirect red force: move to point A"
}
```

-   `GET /status`: Get the current simulation status (scenario details and tick count).

### Visualizations

#### CLI Feed Visualization

The CLI feed is rendered using the Rich library, providing clear, colored output of simulation events.

#### Map View Visualization

To see a graphical map with unit positions, run:

```bash
python visualization/map_view.py
```

This opens a matplotlib window that updates with agent positions in real time.

## Configuration

Global configuration settings are defined in `utils/config.py`:

-   `SIMULATION_TICK_DURATION`: Time (in seconds) for each simulation tick.
-   `DDIL_LEVEL`: Severity level of DDIL simulation (1 = mild, 5 = severe).
-   `OPENAI_API_KEY`: Your OpenAI API key (update this before running LLM-based features).
-   `OPENAI_MODEL`: Model used for LLM interactions (e.g., "gpt-4").

Adjust these parameters as needed to suit your testing and deployment environments.

## Future Enhancements

Future improvements could include:

-   Enhanced context management for LLM-based decision-making.
-   More nuanced DDIL simulation (e.g., dynamic adjustments based on simulated network conditions).
-   Expanded user commands and interactive simulation adjustments.
-   Improved persistence and logging of simulation data for detailed after-action reviews.
-   Additional API endpoints and integration with external C2 systems.
