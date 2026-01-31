# MITRE Bot

An intelligent Incident Analysis Agent that leverages the MITRE ATT&CK framework to analyze security incidents, identify techniques, and provide mitigation strategies using a multi-agent system.

## Features

- **Incident Analysis**: Analyzes natural language descriptions of security incidents.
- **MITRE Mapping**: Identifies relevant MITRE ATT&CK techniques (STIX IDs).
- **Expert Guidance**: Provides technical details, detection opportunities, and mitigation strategies.
- **Multi-Agent Architecture**:
  - **Incident Analysis Lead**: Orchestrates the investigation.
  - **Pattern Analyst**: Identifies ATT&CK techniques from descriptions.
  - **MITRE Specialist**: Retrieves deep technical context and defense strategies.

## Prerequisites

- Python 3.12+
- `uv` (recommended for dependency management) or `pip`

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd mitre-bot
    ```

2.  **Install dependencies**:
    Using `uv`:
    ```bash
    uv sync
    ```
    Or using `pip`:
    ```bash
    pip install .
    ```

3.  **Configure Environment**:
    Create a `.env` file in the root directory:
    ```bash
    touch .env
    ```
    Add the following variables:
    ```env
    # Model to use and add prefix as providers
    # example MODEL=groq:openai/gpt-oss-20b
    MODEL=
    GEMINI_API_KEY=your_api_key_here
    YOUR_PROVIDER_API_KEY=your_api_key_here
    ```

## Usage

**Interactive Mode**:
Run the agent without arguments to enter the interactive prompt:
```bash
uv run -m main
```

## Project Structure

- `app/`: Source code for agents and tools.
  - `agents/`: Agent definitions and prompts.
  - `tools/`: Tools for retrieving MITRE data.
- `main.py`: Entry point for the application.
- `AGENTS.md`: Detailed agent personas and workflows.
- `attack-patterns.json` / `enterprise-attack.json`: MITRE ATT&CK dataset.
