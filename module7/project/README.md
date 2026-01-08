# Investigator Agent (Module 7)

This project implements the **Investigator Agent**, a feature readiness assessor
used in Module 7 of the AI course. The agent analyzes feature metadata, test
metrics, and review data to recommend whether a feature is ready to progress to
the next development phase.

Phase 1 (Issue #1) focuses on **foundation and setup**: project structure,
dependencies, configuration, basic agent, observability, and persistence.

## Project layout

The intended layout (simplified) is:

- `src/investigator_agent/` – agent implementation and support modules
- `tests/` – unit and integration tests
- `data/` – conversations, traces, and evaluation results
- `incoming_data/` – pre-provided example data

For the full structure and detailed plan, see
`module7/project/PLAN_before.md`.

## Prerequisites

- Python **3.13.5** installed and available on your PATH
- [`uv`](https://docs.astral.sh/uv/) installed for dependency and environment management

## Setup

### 1. Create Virtual Environment

From the repository root:

```bash
cd module7/project

# Create a virtual environment for this project
uv venv

# Activate the virtual environment
# PowerShell (recommended on Windows)
.venv\Scripts\Activate.ps1
# cmd.exe on Windows
.venv\Scripts\activate.bat
# Git Bash on Windows
source .venv/Scripts/activate
# WSL / Linux / macOS
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install all dependencies (including the package in editable mode)
uv sync

# Or install the package in development mode
uv pip install -e .
```

### 3. Configure Environment

Create your local `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` and set your `GROQ_API_KEY`:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key from https://console.groq.com (no credit card required).

## Running Tests

Run all tests:

```bash
uv run python -m pytest
```

Run tests with verbose output:

```bash
uv run python -m pytest -v
```

Run specific test file:

```bash
uv run python -m pytest tests/unit/test_config.py -v
```

Run tests with coverage:

```bash
uv run python -m pytest --cov=investigator_agent --cov-report=term-missing
```

## Running the Agent

**Note:** The agent CLI will be available after Step 1.3 (Basic Agent Setup) is completed.

Once implemented, you'll be able to run:

```bash
# Run the agent interactively
uv run python -m cli.py

# Or if a CLI script is configured
investigator-agent
```

## Development

### Code Formatting

```bash
# Format code with black
uv run black src/ tests/

# Check code style with ruff
uv run ruff check src/ tests/
```

### Type Checking

```bash
# Run mypy for type checking
uv run mypy src/
```

## Project Status

**Completed Steps:**
- ✅ Step 1.1: Project Initialization
- ✅ Step 1.2: Configuration Management
- ✅ Step 1.3: Basic Agent Setup with LangChain

**Next Steps:**

- ⏳ Step 1.4: Observability (OpenTelemetry)
- ⏳ Step 1.5: Conversation Persistence

Refer to `PLAN_before.md`, `DESIGN.md`, and `EXERCISE.md` for full details and acceptance criteria.

