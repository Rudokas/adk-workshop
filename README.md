# My Agent Project

An AI agent project using Google's Agent Development Kit (ADK) that plays an adventure game. The agent uses Gemini 2.5 Flash model and interacts with an adventure game API to navigate through game scenarios.

## Features

- AI-powered adventure game player using Google ADK
- OpenAPI toolset integration for game interaction
- Custom utility functions for hash-based exit finding
- Web content fetching capabilities

## Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Google ADK API key
- Adventure game API key

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd my_agent_project
```

2. Install dependencies using uv:
```bash
uv sync
```

This will create a virtual environment and install all required dependencies including `google-adk`.

## Configuration

Set up your environment variables by creating a `.env` file in the `x/` directory:

```bash
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=found_at_google_console_apis_credentials
ADK_API_KEY=another_very_secret_key_value
```

Run these commands to authenticate to google cloud

```bash
gcloud auth login
gcloud config set project gemini-test 
```

The agent uses this API key to authenticate with the adventure game API at `https://adventure.wietsevenema.eu/`. Dont forget to start the level

## Usage

Run the ADK web interface:

```bash
adk web
```

Then open your browser to the localhost URL provided (typically http://localhost:8000), and type `start game` to begin playing.

**Note:** If you make changes to the code, you need to kill the `adk web` process (Ctrl+C) and run it again to see the changes.
