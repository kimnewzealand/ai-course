# Detective Agent

AI agent for release risk assessment using tool calling and observability.

## Overview

The Detective Agent is a Python-based AI agent that assesses software release risks by:
- Analyzing release metadata (version, changes, test results)
- Evaluating deployment metrics (error rates, performance)
- Using tools to gather information and file risk reports
- Providing structured risk assessments with severity levels

## Features

- **OpenRouter Provider**: Uses free open-source models (Llama 3.1 8B Instruct)
- **Tool Calling**: Extensible tool framework for release assessment
- **Observability**: OpenTelemetry tracing for debugging and monitoring
- **Context Management**: Smart truncation to manage conversation history
- **Retry Logic**: Exponential backoff for resilient API calls
- **Evaluation System**: Automated testing of agent behavior

## Setup

### Prerequisites

- Python 3.13.5+
- uv package manager

### Installation

1. Clone the repository and navigate to the project:
```bash
cd module6/project
```

2. Create virtual environment:
```bash
uv venv
```

3. Install dependencies:
```bash
uv sync
```

4. Set up environment variables:
```bash
# Create .env file
echo "OPENROUTER_API_KEY=your-key-here" > .env
```

## Usage

### CLI

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Run the agent
python -m detective_agent.cli
```

### Programmatic

```python
from detective_agent.agent import DetectiveAgent
from detective_agent.providers.openrouter import OpenRouterProvider
from detective_agent.config import AgentConfig, ProviderConfig

# Configure
provider_config = ProviderConfig(api_key="your-key")
agent_config = AgentConfig(provider=provider_config)

# Initialize
provider = OpenRouterProvider(provider_config)
agent = DetectiveAgent(provider, agent_config)

# Use
response = await agent.send_message("Assess risk for release v2.1.0")
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest src/detective_agent/models_test.py
```

## Project Structure

```
detective-agent/
├── src/detective_agent/       # Main source code
│   ├── models.py              # Data models
│   ├── config.py              # Configuration
│   ├── agent.py               # Agent core
│   ├── providers/             # LLM providers
│   ├── tools/                 # Tool framework
│   └── observability/         # Tracing
├── tests/                     # Integration tests
├── evals/                     # Evaluation system
└── data/                      # Runtime data
```

## Documentation

- [DESIGN.md](DESIGN.md) - Architecture and design decisions
- [PLAN_kim.md](PLAN_kim.md) - Implementation plan
- [STEPS.md](STEPS.md) - Step-by-step guide

## License

MIT

