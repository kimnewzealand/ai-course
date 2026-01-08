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

## Setup (Step 1.1)

From the repository root:

```bash
cd module7/project

# Create a virtual environment for this project
uv venv

# Install dependencies defined in pyproject.toml
uv sync
```

Then create your local `.env` file based on the template:

```bash
cp .env.example .env
```

Edit `.env` and set `GROQ_API_KEY` to your key from https://console.groq.com.

Later steps in Phase 1 will add the LangChain-based agent, CLI, observability,
and persistence. Refer to `PLAN_before.md`, `DESIGN.md`, and `EXERCISE.md` for
full details and acceptance criteria.

