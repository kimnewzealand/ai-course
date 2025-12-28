# Detective Agent

An AI agent for release risk assessment, built with Python 3.13+ and modern async patterns.

## Overview

Detective Agent analyzes software releases to identify potential risks by leveraging LLM capabilities with tool calling. It provides structured risk assessments through a conversational interface, with full observability via OpenTelemetry.

The agent evaluates:
- **Release metadata** - version numbers, changelog entries, commit history
- **Deployment metrics** - error rates, latency, rollback history
- **Test coverage** - unit test results, integration test status
- **Dependency changes** - security vulnerabilities, breaking changes

## Features

| Feature | Description |
|---------|-------------|
| **Multi-Provider Support** | OpenRouter provider with extensible Protocol-based architecture |
| **Tool Calling** | Registry-based tool system for release assessment operations |
| **Observability** | OpenTelemetry tracing with filesystem export for debugging |
| **Context Management** | Truncation strategy to manage LLM context windows (last 6 messages) |
| **Retry Logic** | Exponential backoff with jitter for resilient API interactions |
| **Conversation Persistence** | Save and resume conversations with JSON storage |
| **Type Safety** | Full type hints with `py.typed` marker for mypy/pyright |
| **Modern Python** | Pattern matching, async context managers, pydantic-settings |

## Prerequisites

- **Python 3.13.5+** - Required for modern language features
- **uv** package manager - [Installation guide](https://docs.astral.sh/uv/getting-started/installation/)

## Installation

### 1. Navigate to Project Directory

```bash
cd module6/project
```

### 2. Create Virtual Environment

```bash
uv venv
```

This creates a `.venv` directory with Python 3.13.5+.

### 3. Install Dependencies

```bash
# Install main dependencies only
uv sync

# Install with development dependencies (testing, type checking)
uv sync --extra dev
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Required: OpenRouter API key (get from https://openrouter.ai/)
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here

# Optional: Model selection (default shown below)
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free

# Optional: Response temperature 0.0-2.0 (default: 0.7)
OPENROUTER_TEMPERATURE=0.7

# Optional: Maximum tokens in response (default: 4096)
OPENROUTER_MAX_TOKENS=4096

# Optional: Request timeout in seconds (default: 30.0)
OPENROUTER_TIMEOUT=30.0
```

> **Note**: The `.env` file is git-ignored. Never commit API keys to version control.

## Usage

### CLI Interface

The agent provides an interactive command-line interface:

```bash
# Using the installed script
uv run detective-agent

# Or run the module directly
uv run python -m detective_agent.cli
```

**CLI Commands:**
- Type your message and press Enter to chat
- Type `new` to start a fresh conversation
- Type `history` to view conversation history
- Type `quit` or `exit` to exit

## Testing

All commands use `uv run` to execute within the virtual environment.

### Run All Tests

```bash
uv run pytest -v
```

### Run with Coverage Report

```bash
# Terminal coverage report
uv run pytest --cov=src/detective_agent --cov-report=term-missing

# HTML coverage report
uv run pytest --cov=src/detective_agent --cov-report=html
```

### Run Specific Test Files

```bash
# Test a specific module
uv run pytest src/detective_agent/models_test.py -v

# Run only tests matching a pattern
uv run pytest -k "test_send_message" -v
```

### Type Checking

```bash
uv run mypy src/detective_agent
```

## Project Structure

```
module6/project/
├── src/detective_agent/
│   ├── __init__.py           # Package exports (DetectiveAgent, AgentConfig, etc.)
│   ├── py.typed               # PEP 561 marker for type checkers
│   ├── types.py               # Shared type aliases (MessageList, MessageRole)
│   ├── config.py              # Configuration with pydantic-settings
│   ├── config_test.py         # Configuration tests
│   ├── models.py              # Data models (Message, Conversation)
│   ├── models_test.py         # Model tests
│   ├── agent.py               # DetectiveAgent core class
│   ├── agent_test.py          # Agent tests
│   ├── persistence.py         # ConversationStore for JSON persistence
│   ├── persistence_test.py    # Persistence tests
│   ├── cli.py                 # Command-line interface
│   ├── conftest.py            # Shared pytest fixtures
│   │
│   ├── providers/             # LLM Provider implementations
│   │   ├── __init__.py        # Exports Provider, OpenRouterProvider
│   │   ├── base.py            # Provider Protocol definition
│   │   ├── openrouter.py      # OpenRouter implementation
│   │   ├── openrouter_test.py # Provider tests with respx mocks
│   │   └── errors.py          # ProviderError, AuthenticationError, etc.
│   │
│   ├── tools/                 # Tool calling system (planned)
│   ├── context/               # Context window management (planned)
│   ├── retry/                 # Retry with exponential backoff (planned)
│   └── observability/         # OpenTelemetry tracing (planned)
│
├── tests/                     # Integration tests
│   └── conftest.py            # Mock fixtures for CI/CD
│
├── data/                      # Runtime data (git-ignored)
│   ├── conversations/         # Saved conversation JSON files
│   └── traces/                # OpenTelemetry trace exports
│
├── pyproject.toml             # Project config, dependencies, tool settings
├── .env                       # Environment variables (git-ignored)
├── .gitignore                 # Git ignore patterns
├── DESIGN.md                  # Architecture and design decisions
├── PLAN_kim.md                # Detailed implementation plan
├── STEPS.md                   # Step-by-step implementation guide
└── README.md                  # This file
```

## Documentation

| Document | Description |
|----------|-------------|
| [DESIGN.md](DESIGN.md) | Architecture decisions, design rationale, and system overview |
| [PLAN_kim.md](PLAN_kim.md) | Detailed implementation plan with code examples |
| [STEPS.md](STEPS.md) | Ordered implementation steps and milestones |

## License

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR OTHER DEALINGS IN THE SOFTWARE.

