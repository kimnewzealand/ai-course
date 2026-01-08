# Investigator Agent Implementation Plan

## Overview

The Investigator Agent is an automated feature readiness assessor that analyzes feature metadata, test metrics, and review data to provide recommendations on whether a feature is ready to progress to the next development phase (Development → UAT → Production).

**Core Capability:** Given a natural language query like "Is the reservation feature ready for production?", the agent:
1. Identifies which feature the user is asking about
2. Retrieves relevant metadata from JIRA, metrics, and reviews
3. Analyzes the data against readiness criteria
4. Provides a clear recommendation with supporting evidence

See [DESIGN.md](DESIGN.md) for architectural details and [EXERCISE.md](EXERCISE.md) for complete acceptance criteria.

## Implementation Goals

- **SDK-Based Implementation**: Use a mature agent framework (LangChain)
- **Comprehensive Observability**: OpenTelemetry traces for all operations
- **Robust Error Handling**: Graceful handling of missing/malformed data
- **Context Management**: Handle large documents (>10KB) without exhausting token limits
- **High Accuracy**: >85% success rate on evaluation scenarios
- **Clear Decision Making**: Transparent reasoning for all recommendations

## Technology Stack

**Framework:** LangChain (Python)

**LLM Provider:** Groq (Free Tier with Open-Source Models)

**Python Version:** 3.13.5 (fixed)

> Pragmatic note: if Python 3.13.5 is not yet available in your environment, use the closest supported version (for example, 3.12.x) while developing, and update the pinned version and `requires-python` once 3.13.5 is reachable on your machines.

**Why LangChain:**
- Mature ecosystem with extensive tooling and integrations
- Built-in observability support (LangSmith, OpenTelemetry)
- Strong community support and comprehensive documentation
- Excellent tool/function calling abstractions
- Native support for conversation memory and persistence
- Easy integration with Groq via OpenAI-compatible API

**Why Groq:**
- **100% FREE tier** - No credit card required to get started
- **Fastest inference** - Up to 840 tokens/second (industry-leading)
- **Open-source models only** - Llama 3.1, Llama 3.3, Mixtral, Qwen
- **OpenAI-compatible API** - Works seamlessly with `langchain-openai`
- **Extremely low cost** - Llama 3.1 8B at $0.05/M input tokens
- **Get API key:** https://console.groq.com (instant, no payment required)

**Recommended Models:**
- **Llama 3.1 8B Instant** - Fastest, cheapest ($0.05/M input, $0.08/M output)
- **Llama 3.3 70B Versatile** - More capable ($0.59/M input, $0.79/M output)
- **Qwen3 32B** - Balanced performance ($0.29/M input, $0.59/M output)

**Core Dependencies (Fixed Versions):**
- `langchain==0.3.14` - Core framework
- `langchain-openai==0.2.14` - OpenAI-compatible provider (works with Groq)
- `langchain-community==0.3.14` - Community tools and utilities
- `langchain-core==0.3.28` - Core abstractions
- `opentelemetry-api==1.29.0` - Observability API
- `opentelemetry-sdk==1.29.0` - Observability SDK
- `pydantic==2.10.5` - Data validation and settings
- `pydantic-settings==2.7.1` - Settings management
- `python-dotenv==1.0.1` - Environment variable management

**Development Dependencies (Fixed Versions):**
- `pytest==8.3.4` - Testing framework
- `pytest-asyncio==0.24.0` - Async test support
- `black==24.10.0` - Code formatting
- `ruff==0.8.4` - Linting
- `mypy==1.14.1` - Type checking

## Data Architecture

The `incoming_data/` directory contains 4 features with realistic test data:

```
incoming_data/
├── feature1/  # Maintenance Scheduling ( READY - Production)
├── feature2/  # QR Code Check-in ( NOT READY - Blockers)
├── feature3/  # Resource Reservation ( AMBIGUOUS - Mixed signals)
└── feature4/  # Community Credits ( PARTIAL - Some gaps)

Each feature contains:
├── jira/
│   ├── feature_issue.json       # JIRA ticket metadata
│   └── issue_changelog.json     # Status history
├── metrics/
│   ├── performance_benchmarks.json
│   ├── pipeline_results.json
│   ├── security_scan_results.json
│   ├── test_coverage_report.json
│   └── unit_test_results.json
├── reviews/
│   ├── security.json            # Security review results
│   ├── stakeholders.json        # Stakeholder approvals
│   └── uat.json                 # UAT test results
└── planning/
    ├── ARCHITECTURE.md (large, >10KB)
    ├── DESIGN_DOC.md (large, >10KB)
    ├── DATABASE_SCHEMA.md
    ├── DEPLOYMENT_PLAN.md
    └── ... (10+ markdown files)
```

**Total Data:** ~1MB across all features

## Required Tools

### Tool 1: Feature Metadata Lookup
**Purpose:** Retrieve JIRA metadata for all features or a specific feature

**Input:** None (returns all features) or `feature_id` (returns specific feature)

**Output:**
```json
{
  "features": [
    {
      "folder": "feature1",
      "jira_key": "PLAT-1523",
      "feature_id": "FEAT-MS-001",
      "summary": "Maintenance Scheduling & Alert System",
      "status": "Production",
      "data_quality": "complete"
    }
  ]
}
```

### Tool 2: Testing Results Tool
**Purpose:** Retrieve testing metrics for a feature (unit tests, coverage, performance, pipeline, security scans)

**Input:** 
- `feature_id`: The feature identifier
- `data_type`: One of: `metrics/unit_test_results`, `metrics/test_coverage_report`, `metrics/performance_benchmarks`, `metrics/pipeline_results`, `metrics/security_scan_results`

**Output:** JSON content from the requested file

**Error Handling:** Return clear error if file missing or malformed

## Implementation Phases

### Phase 1: Foundation & Setup (DETAILED BELOW)
### Phase 2: Feature Metadata Tool
### Phase 3: Testing Results Tool
### Phase 4: Observability Tracing
### Phase 5: Retry with Exponential Back-off
### Phase 6: Evaluations

---

## PHASE 1: Foundation & Setup (DETAILED)

**Goal:** Establish the project foundation with chosen SDK, basic agent setup, observability, and conversation persistence.

### Step 1.1: Project Initialization

**Tasks:**
- [ ] Create project directory structure (see structure above)
- [ ] Initialize uv for dependency management
- [ ] Create pyproject.toml with LangChain dependencies
- [ ] Set up virtual environment with uv
- [ ] Install core dependencies
- [ ] Create .env.example template
- [ ] Set up .gitignore

**Commands:**
```bash
# Navigate to project directory
cd module7/project

# Ensure Python 3.13.5 is installed and available
python --version  # Should show Python 3.13.5

# Create virtual environment with Python 3.13.5
uv venv --python 3.13.5

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Unix/MacOS:
source .venv/bin/activate

# Install dependencies with exact versions from pyproject.toml
uv sync

# Or manually add dependencies with exact versions:
uv add langchain==0.3.14 langchain-openai==0.2.14
uv add langchain-community==0.3.14 langchain-core==0.3.28
uv add opentelemetry-api==1.29.0 opentelemetry-sdk==1.29.0
uv add pydantic==2.10.5 pydantic-settings==2.7.1 python-dotenv==1.0.1

# Add dev dependencies with exact versions
uv add --dev pytest==8.3.4 pytest-asyncio==0.24.0
uv add --dev black==24.10.0 ruff==0.8.4 mypy==1.14.1

# Create directory structure
mkdir -p src/investigator_agent/{tools,observability,persistence,evaluation}
mkdir -p tests/{unit,integration}
mkdir -p data/{conversations,traces,evaluations}

# Create __init__.py files
touch src/investigator_agent/__init__.py
touch src/investigator_agent/tools/__init__.py
touch src/investigator_agent/observability/__init__.py
touch src/investigator_agent/persistence/__init__.py
touch src/investigator_agent/evaluation/__init__.py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
```

**Create .env.example:**
```bash
# Groq Configuration (Free Tier - Open Source Models)
# Get your free API key at: https://console.groq.com (no credit card required)
GROQ_API_KEY=your_groq_api_key_here

# Model Configuration
# Recommended models (all open-source):
# - llama-3.1-8b-instant (fastest, cheapest - $0.05/M input tokens)
# - llama-3.3-70b-versatile (more capable - $0.59/M input tokens)
# - qwen3-32b (balanced - $0.29/M input tokens)
MODEL_NAME=llama-3.1-8b-instant

# Agent Configuration
TEMPERATURE=0.0
MAX_TOKENS=4096

# Paths
DATA_DIR=incoming_data
CONVERSATIONS_DIR=data/conversations
TRACES_DIR=data/traces

# Observability
ENABLE_TRACING=true
TRACE_EXPORT_FORMAT=json
```

Note: `MODEL_NAME`, `TEMPERATURE`, and `MAX_TOKENS` map directly to `AgentConfig.model_name`, `AgentConfig.temperature`, and `AgentConfig.max_tokens` in `config.py`.

**Deliverables:**
- [ ] Project folder with proper structure
- [ ] pyproject.toml with all dependencies
- [ ] Virtual environment created and activated
- [ ] .env.example template
- [ ] .gitignore configured
- [ ] README.md with setup instructions

**Acceptance Criteria:**
- [ ] Python 3.13.5 is installed and active
- [ ] `uv sync` runs without errors
- [ ] Virtual environment is activated
- [ ] Can import LangChain: `python -c "import langchain; print(langchain.__version__)"` (should show 0.3.14)
- [ ] All directories created
- [ ] .env.example exists for reference
- [ ] All dependencies installed at exact versions specified

**Project Structure (LangChain Implementation):**
```
module7/project/
├── src/
│   └── investigator_agent/
│       ├── __init__.py
│       ├── agent.py              # LangChain agent orchestration
│       ├── config.py             # Configuration management
│       ├── models.py             # Pydantic data models
│       ├── prompts.py            # System prompts and templates
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── feature_metadata.py    # LangChain tool for JIRA data
│       │   ├── analysis_data.py       # LangChain tool for metrics/reviews
│       │   └── base.py                # Base tool utilities
│       ├── observability/
│       │   ├── __init__.py
│       │   ├── tracer.py              # OpenTelemetry setup
│       │   └── callbacks.py           # LangChain callbacks for tracing
│       ├── persistence/
│       │   ├── __init__.py
│       │   └── conversation_store.py  # Conversation save/load
│       └── evaluation/
│           ├── __init__.py
│           ├── scenarios.py           # Test scenarios
│           └── runner.py              # Evaluation runner
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_config.py
│   │   ├── test_tools.py
│   │   └── test_persistence.py
│   └── integration/
│       └── test_agent_flow.py
├── data/
│   ├── conversations/            # Saved conversations (JSON)
│   ├── traces/                   # OpenTelemetry traces (JSON)
│   └── evaluations/              # Evaluation results
├── incoming_data/                # Test data (already provided)
├── cli.py                        # Interactive CLI entry point
├── pyproject.toml               # Dependencies (uv format)
├── .env                         # Environment variables (git-ignored)
├── .env.example                 # Environment template
├── .gitignore
├── README.md                    # Setup and usage instructions
├── PLAN.md                      # This file
├── DESIGN.md                    # Architecture spec
└── EXERCISE.md                  # Acceptance criteria
```

**Dependencies (pyproject.toml for uv):**
```toml
[project]
name = "investigator-agent"
version = "0.1.0"
description = "Feature readiness assessment agent using LangChain"
requires-python = "==3.13.5"

dependencies = [
    "langchain==0.3.14",
    "langchain-openai==0.2.14",
    "langchain-community==0.3.14",
    "langchain-core==0.3.28",
    "opentelemetry-api==1.29.0",
    "opentelemetry-sdk==1.29.0",
    "pydantic==2.10.5",
    "pydantic-settings==2.7.1",
    "python-dotenv==1.0.1",
]

[project.optional-dependencies]
dev = [
    "pytest==8.3.4",
    "pytest-asyncio==0.24.0",
    "black==24.10.0",
    "ruff==0.8.4",
    "mypy==1.14.1",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.black]
line-length = 100
target-version = ["py313"]

[tool.ruff]
line-length = 100
target-version = "py313"
```

**Note (branch `feature/1-1-project-init`)**  
During implementation, `langchain-core` was updated from `0.3.28` to `0.3.29` in
`pyproject.toml` to satisfy the resolver constraints for `langchain==0.3.14`
when running `uv sync`.

### Step 1.2: Configuration Management

**Tasks:**
- [ ] Create configuration system using Pydantic Settings
- [ ] Set up environment variable loading (.env file)
- [ ] Define configuration models with validation
- [ ] Add configuration factory function

**Create `src/investigator_agent/config.py`:**
```python
"""Configuration management for Investigator Agent."""

from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentConfig(BaseSettings):
    """Main configuration for the Investigator Agent."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Groq LLM Settings (Free Tier - Open Source Models)
    groq_api_key: str = Field(..., description="Groq API key from console.groq.com")
    model_name: str = Field(
        default="llama-3.1-8b-instant",
        description="Groq model (llama-3.1-8b-instant, llama-3.3-70b-versatile, qwen3-32b)"
    )

    # Agent Settings
    temperature: float = Field(
        default=0.0,
        ge=0.0,
        le=2.0,
        description="Temperature for LLM (0.0 for deterministic)"
    )
    max_tokens: int = Field(
        default=4096,
        gt=0,
        description="Maximum tokens for LLM response"
    )

    # Data Paths
    data_dir: Path = Field(
        default=Path("incoming_data"),
        description="Directory containing feature data"
    )
    conversations_dir: Path = Field(
        default=Path("data/conversations"),
        description="Directory for saved conversations"
    )
    traces_dir: Path = Field(
        default=Path("data/traces"),
        description="Directory for OpenTelemetry traces"
    )
    evaluations_dir: Path = Field(
        default=Path("data/evaluations"),
        description="Directory for evaluation results"
    )

    # Observability
    enable_tracing: bool = Field(
        default=True,
        description="Enable OpenTelemetry tracing"
    )
    trace_export_format: Literal["json", "otlp"] = Field(
        default="json",
        description="Trace export format"
    )

    @field_validator("data_dir", "conversations_dir", "traces_dir", "evaluations_dir")
    @classmethod
    def ensure_path_exists(cls, v: Path) -> Path:
        """Ensure directory exists, create if needed."""
        v.mkdir(parents=True, exist_ok=True)
        return v

    def get_base_url(self) -> str:
        """Get Groq API base URL (OpenAI-compatible)."""
        return "https://api.groq.com/openai/v1"


def load_config() -> AgentConfig:
    """Load and validate configuration from environment."""
    try:
        config = AgentConfig()
        return config
    except Exception as e:
        raise ValueError(f"Configuration error: {e}") from e
```

**Deliverables:**
- [ ] `config.py` with Pydantic Settings
- [ ] `.env` file created (from .env.example)
- [ ] Configuration loading and validation logic
- [ ] Automatic directory creation

**Acceptance Criteria:**
- [ ] Configuration loads from .env file
- [ ] Missing required config (GROQ_API_KEY) raises clear error
- [ ] Configuration validates on load (type checking, ranges)
- [ ] Directories auto-created if missing
- [ ] Sensitive data (API keys) in .gitignore

**Test Configuration:**
```bash
# Create .env from template
cp .env.example .env

# Get your free Groq API key from https://console.groq.com
# Edit .env with your GROQ_API_KEY

# Then test configuration loading
python -c "from investigator_agent.config import load_config; config = load_config(); print(f'Loaded config for Groq with model: {config.model_name}')"
```

### Step 1.3: Basic Agent Setup with LangChain

**Tasks:**
- [ ] Create main agent class using LangChain
- [ ] Initialize ChatOpenAI configured for Groq's OpenAI-compatible API
- [ ] Set up conversation memory (ConversationBufferMemory)
- [ ] Implement basic conversation loop
- [ ] Create simple CLI for testing

**Create `src/investigator_agent/agent.py`:**
```python
"""Core Investigator Agent using LangChain."""

from typing import Any

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from investigator_agent.config import AgentConfig


class InvestigatorAgent:
    """Feature readiness assessment agent using LangChain."""

    def __init__(self, config: AgentConfig):
        """Initialize the agent with configuration."""
        self.config = config

        # Initialize Groq LLM (OpenAI-compatible)
        self.llm = ChatOpenAI(
            model=config.model_name,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            openai_api_key=config.groq_api_key,
            openai_api_base=config.get_base_url(),
        )

        # Set up conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
        )

        # Tools will be added in Phase 2-3
        self.tools = []

        # Create prompt template
        self.prompt = self._create_prompt()

        # Agent executor (will be initialized when tools are added)
        self.agent_executor = None

    def _create_prompt(self) -> ChatPromptTemplate:
        """Create the agent prompt template."""
        system_message = """You are the Investigator Agent, an automated feature readiness assessor.

Your role is to help determine if software features are ready to progress to the next development phase.

When asked about a feature, you should:
1. Understand what the user is asking
2. Provide helpful information about feature assessment

For now, you can have general conversations about feature readiness assessment.
In later phases, you will have tools to retrieve actual feature data."""

        return ChatPromptTemplate.from_messages([
            SystemMessage(content=system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

    async def send_message(self, user_message: str) -> str:
        """Send a message and get response."""
        try:
            # For Phase 1, use simple LLM call without agent executor
            # (Agent executor requires tools, which we'll add in Phase 2)
            from langchain_core.messages import HumanMessage

            # Get chat history
            history = self.memory.chat_memory.messages

            # Create messages list
            messages = [
                SystemMessage(content=self.prompt.messages[0].content),
                *history,
                HumanMessage(content=user_message),
            ]

            # Get response
            response = await self.llm.ainvoke(messages)

            # Save to memory
            self.memory.chat_memory.add_user_message(user_message)
            self.memory.chat_memory.add_ai_message(response.content)

            return response.content

        except Exception as e:
            return f"Error: {str(e)}"

    def reset_conversation(self):
        """Clear conversation history."""
        self.memory.clear()
```

**Create `cli.py` (in project root):**
```python
"""Interactive CLI for Investigator Agent."""

import asyncio
import sys

from investigator_agent.agent import InvestigatorAgent
from investigator_agent.config import load_config


async def main():
    """Run interactive CLI."""
    print("=" * 60)
    print("Investigator Agent - Feature Readiness Assessment")
    print("=" * 60)
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'reset' to start a new conversation")
    print("=" * 60)
    print()

    try:
        config = load_config()
        agent = InvestigatorAgent(config)
        print(f"✓ Agent initialized with Groq ({config.model_name})")
        print()
    except Exception as e:
        print(f"✗ Failed to initialize agent: {e}")
        sys.exit(1)

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("\nGoodbye!")
                break

            if user_input.lower() == "reset":
                agent.reset_conversation()
                print("\n✓ Conversation reset\n")
                continue

            # Get response
            response = await agent.send_message(user_input)
            print(f"\nAgent: {response}\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n✗ Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
```

**Deliverables:**
- [ ] `agent.py` with LangChain agent
- [ ] `cli.py` for interactive testing
- [ ] Basic conversation functionality
- [ ] Memory management

**Acceptance Criteria:**
- [ ] Agent initializes without errors
- [ ] Can send message and receive response from LLM
- [ ] Conversation history maintained across messages
- [ ] CLI allows interactive testing
- [ ] Basic error handling for API failures
- [ ] Can reset conversation

**Manual Test:**
```bash
# Start CLI
python cli.py

# Test basic conversation
You: Hello, can you help me assess features?
Agent: [Should respond appropriately about feature assessment]

You: What can you do?
Agent: [Should describe capabilities]

You: reset
# Should clear conversation

You: exit
# Should exit cleanly
```

### Step 1.4: OpenTelemetry Observability with LangChain Callbacks

This step sets up basic tracing for early debugging (LLM calls and core operations). In Phase 4 you will extend this into full observability and add trace inspection tools.

**Tasks:**
- [ ] Set up OpenTelemetry SDK
- [ ] Create custom LangChain callback handler for tracing
- [ ] Implement trace/span creation for agent operations
- [ ] Add file-based trace exporter (JSON format)
- [ ] Instrument LLM calls with timing and token counts

**Create `src/investigator_agent/observability/tracer.py`:**
```python
"""OpenTelemetry tracing setup."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExporter, SpanExportResult
from opentelemetry.sdk.resources import Resource


class FileSpanExporter(SpanExporter):
    """Export spans to JSON files."""

    def __init__(self, traces_dir: Path):
        self.traces_dir = traces_dir
        self.traces_dir.mkdir(parents=True, exist_ok=True)

    def export(self, spans) -> SpanExportResult:
        """Export spans to file."""
        try:
            # Group by date
            date_str = datetime.now().strftime("%Y-%m-%d")
            date_dir = self.traces_dir / date_str
            date_dir.mkdir(exist_ok=True)

            # Create trace file
            timestamp = datetime.now().strftime("%H%M%S")
            trace_file = date_dir / f"trace_{timestamp}.json"

            # Convert spans to dict
            trace_data = {
                "timestamp": datetime.now().isoformat(),
                "spans": [self._span_to_dict(span) for span in spans],
            }

            # Write to file
            with open(trace_file, "w") as f:
                json.dump(trace_data, f, indent=2)

            return SpanExportResult.SUCCESS
        except Exception as e:
            print(f"Error exporting trace: {e}")
            return SpanExportResult.FAILURE

    def _span_to_dict(self, span) -> dict[str, Any]:
        """Convert span to dictionary."""
        return {
            "name": span.name,
            "span_id": format(span.context.span_id, "016x"),
            "trace_id": format(span.context.trace_id, "032x"),
            "start_time": span.start_time,
            "end_time": span.end_time,
            "duration_ns": span.end_time - span.start_time if span.end_time else 0,
            "attributes": dict(span.attributes) if span.attributes else {},
            "status": str(span.status.status_code) if span.status else "UNSET",
        }

    def shutdown(self):
        """Shutdown exporter."""
        pass


def setup_tracing(traces_dir: Path) -> trace.Tracer:
    """Set up OpenTelemetry tracing."""
    # Create resource
    resource = Resource.create({"service.name": "investigator-agent"})

    # Create tracer provider
    provider = TracerProvider(resource=resource)

    # Add file exporter
    exporter = FileSpanExporter(traces_dir)
    processor = SimpleSpanProcessor(exporter)
    provider.add_span_processor(processor)

    # Set as global
    trace.set_tracer_provider(provider)

    # Return tracer
    return trace.get_tracer(__name__)
```

**Create `src/investigator_agent/observability/callbacks.py`:**
```python
"""LangChain callbacks for observability."""

from typing import Any
from uuid import UUID

from langchain.callbacks.base import BaseCallbackHandler
from opentelemetry import trace


class TracingCallbackHandler(BaseCallbackHandler):
    """LangChain callback handler for OpenTelemetry tracing."""

    def __init__(self, tracer: trace.Tracer):
        self.tracer = tracer
        self.spans = {}

    def on_llm_start(
        self, serialized: dict[str, Any], prompts: list[str], **kwargs: Any
    ) -> None:
        """Start LLM span."""
        run_id = kwargs.get("run_id")
        span = self.tracer.start_span("llm_call")
        span.set_attribute("model", serialized.get("name", "unknown"))
        span.set_attribute("prompts_count", len(prompts))
        self.spans[run_id] = span

    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        """End LLM span."""
        run_id = kwargs.get("run_id")
        if run_id in self.spans:
            span = self.spans[run_id]

            # Extract token usage if available
            if hasattr(response, "llm_output") and response.llm_output:
                token_usage = response.llm_output.get("token_usage", {})
                span.set_attribute("input_tokens", token_usage.get("prompt_tokens", 0))
                span.set_attribute("output_tokens", token_usage.get("completion_tokens", 0))
                span.set_attribute("total_tokens", token_usage.get("total_tokens", 0))

            span.end()
            del self.spans[run_id]

    def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        """Handle LLM error."""
        run_id = kwargs.get("run_id")
        if run_id in self.spans:
            span = self.spans[run_id]
            span.set_attribute("error", str(error))
            span.end()
            del self.spans[run_id]

    def on_tool_start(
        self, serialized: dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        """Start tool span."""
        run_id = kwargs.get("run_id")
        span = self.tracer.start_span("tool_execution")
        span.set_attribute("tool_name", serialized.get("name", "unknown"))
        span.set_attribute("input", input_str[:500])  # Truncate long inputs
        self.spans[run_id] = span

    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """End tool span."""
        run_id = kwargs.get("run_id")
        if run_id in self.spans:
            span = self.spans[run_id]
            span.set_attribute("output", output[:500])  # Truncate long outputs
            span.end()
            del self.spans[run_id]

    def on_tool_error(self, error: Exception, **kwargs: Any) -> None:
        """Handle tool error."""
        run_id = kwargs.get("run_id")
        if run_id in self.spans:
            span = self.spans[run_id]
            span.set_attribute("error", str(error))
            span.end()
            del self.spans[run_id]
```

**Update `agent.py` to use tracing:**
```python
# Add to imports
from investigator_agent.observability.tracer import setup_tracing
from investigator_agent.observability.callbacks import TracingCallbackHandler

# In __init__:
if config.enable_tracing:
    self.tracer = setup_tracing(config.traces_dir)
    self.callbacks = [TracingCallbackHandler(self.tracer)]
else:
    self.tracer = None
    self.callbacks = []

# In send_message, add callbacks parameter:
response = await self.llm.ainvoke(messages, config={"callbacks": self.callbacks})
```

**Deliverables:**
- [ ] `observability/tracer.py` with OpenTelemetry setup
- [ ] `observability/callbacks.py` with LangChain integration
- [ ] Trace export to `data/traces/` directory
- [ ] Instrumentation in agent core

**Acceptance Criteria:**
- [ ] Every LLM call generates trace spans
- [ ] Traces saved to `data/traces/YYYY-MM-DD/` directory
- [ ] LLM calls include token counts and timing (when available)
- [ ] Trace files are human-readable JSON
- [ ] Tool calls traced (will be tested in Phase 2-3)

**Manual Test:**
```bash
# Run a conversation
python cli.py
You: Test message
Agent: [Response]
You: exit

# Check trace was created
ls data/traces/$(date +%Y-%m-%d)/
# Should see trace_*.json file(s)

# Verify trace content
cat data/traces/$(date +%Y-%m-%d)/trace_*.json
# Should see structured trace with llm_call spans
```

### Step 1.5: Conversation Persistence

**Tasks:**
- [ ] Implement conversation save/load functionality
- [ ] Create conversation storage format (JSON)
- [ ] Add conversation ID generation
- [ ] Implement conversation listing
- [ ] Add ability to resume previous conversations

**Deliverables:**
 - [ ] `persistence/conversation_store.py` with save/load logic
 - [ ] Conversations saved to `data/conversations/` directory
 - [ ] CLI commands to list and resume conversations

**Conversation Storage Format:**
```json
{
  "conversation_id": "conv_20260107_103045",
  "created_at": "2026-01-07T10:30:45Z",
  "updated_at": "2026-01-07T10:35:12Z",
  "trace_id": "trace_abc123",
  "messages": [
    {
      "role": "system",
      "content": "You are the Investigator Agent...",
      "timestamp": "2026-01-07T10:30:45Z"
    },
    {
      "role": "user",
      "content": "Is the reservation feature ready?",
      "timestamp": "2026-01-07T10:31:00Z"
    },
    {
      "role": "assistant",
      "content": "Let me check the feature status...",
      "timestamp": "2026-01-07T10:31:02Z",
      "metadata": {
        "tool_calls": [],
        "tokens": 180
      }
    }
  ],
  "metadata": {
    "model": "llama-3.1-8b-instant",
    "total_tokens": 630,
    "message_count": 3
  }
}
```

**Acceptance Criteria:**
- [ ] Conversations automatically saved after each message
- [ ] Can list all saved conversations
- [ ] Can load and resume a previous conversation
- [ ] Conversation files include all messages and metadata
- [ ] Trace ID links conversation to its trace file

**Manual Test:**
```bash
# Start new conversation
python -m investigator_agent.cli
You: Test message 1
Agent: [Response]
You: exit

# List conversations
python -m investigator_agent.cli --list
# Should show saved conversation

# Resume conversation
python -m investigator_agent.cli --resume conv_20260107_103045
You: Test message 2
# Should continue from previous context
```

### Step 1.6: System Prompt (Initial Version)

**Tasks:**
- [ ] Create initial system prompt for agent role
- [ ] Define agent capabilities and limitations
- [ ] Add placeholder for tool descriptions (to be filled in Phase 2-3)
- [ ] Test prompt effectiveness with basic queries

**Deliverables:**
 - [ ] System prompt in configuration or separate file
 - [ ] Documentation of prompt design decisions

**Initial System Prompt Template:**
```
You are the Investigator Agent, an automated feature readiness assessor for the Release Confidence System.

Your role is to analyze feature metadata, test metrics, and review data to determine if a feature is ready to progress to the next development phase (Development → UAT → Production).

When a user asks about a feature's readiness:
1. Identify which feature they're asking about
2. Retrieve relevant data using your available tools
3. Analyze the data against readiness criteria
4. Provide a clear recommendation with supporting evidence

Available Tools:
[Tool descriptions will be added in Phase 2-3]

Decision Criteria:
- All unit tests must pass (0 failures)
- Test coverage should be >80%
- Security review must show LOW or MEDIUM risk (HIGH is blocking)
- All required stakeholder approvals must be obtained
- No critical bugs in current phase
- Documentation must be complete

Always provide:
- Clear recommendation (READY / NOT READY / NEEDS REVIEW)
- Specific evidence supporting your decision
- List of any blockers or concerns
- Next steps or actions required

Be concise but thorough. If data is missing or ambiguous, state this clearly.
```

**Acceptance Criteria:**
- [ ] System prompt defines agent role clearly
- [ ] Prompt includes decision criteria
- [ ] Agent behavior aligns with prompt instructions
- [ ] Prompt is configurable (not hardcoded)

### Step 1.7: Phase 1 Verification & Testing

**Tasks:**
- [ ] Write unit tests for configuration loading
- [ ] Write unit tests for conversation persistence
- [ ] Write integration test for basic conversation flow
- [ ] Manual testing of all Phase 1 components
- [ ] Document any issues or limitations discovered

**Test Coverage:**
```python
# Unit tests to create:
# - test_config.py: Configuration loading and validation
# - test_conversation_store.py: Save/load conversations
# - test_agent_basic.py: Agent initialization and basic chat

# Integration tests:
# - test_conversation_flow.py: End-to-end conversation with persistence and tracing
```

**Acceptance Criteria:**
- [ ] All unit tests pass
- [ ] Integration test demonstrates full conversation flow
- [ ] Manual CLI testing successful
- [ ] Traces generated correctly
- [ ] Conversations persisted correctly
- [ ] No errors in logs

**Phase 1 Completion Checklist:**
- [ ] Project structure created
- [ ] Dependencies installed
- [ ] Configuration system working
- [ ] Basic agent conversation functional
- [ ] OpenTelemetry tracing operational
- [ ] Conversation persistence working
- [ ] Initial system prompt defined
- [ ] All tests passing
- [ ] Manual testing successful
- [ ] Code committed to version control

---

## PHASE 2: Feature Metadata Tool (High-Level)

**Goal:** Build LangChain tool that retrieves JIRA metadata for features

**Key Tasks:**
- Implement feature metadata loader from JIRA JSON files
- Create feature ID → folder mapping utility
- Build LangChain `@tool` decorator or `StructuredTool`
- Handle missing/malformed data gracefully
- Add comprehensive error messages
- Write unit tests for all 4 features
- Integrate tool with agent using `create_openai_functions_agent`
- Update system prompt with tool description

**LangChain Tool Pattern:**
```python
from langchain.tools import tool

@tool
def get_feature_metadata(feature_id: str = None) -> dict:
    """Retrieve JIRA metadata for features.

    Args:
        feature_id: Optional feature ID. If None, returns all features.

    Returns:
        Dictionary with feature metadata including folder, jira_key,
        feature_id, summary, status, and data_quality.
    """
    # Implementation here
    pass
```

**Example output (single feature):**
```json
{
  "feature_id": "FEAT-RS-001",
  "jira_key": "RS-101",
  "folder": "feature1",
  "summary": "Reservation service refactor",
  "status": "READY - Production",
  "data_quality": "good"
}
```

**Acceptance Criteria:**
- Tool retrieves metadata for all 4 features
- Returns: folder, jira_key, feature_id, summary, status, data_quality
- Agent can call tool via LangChain agent executor
- Tool execution traced via callbacks
- Manual CLI test demonstrates feature identification

---

## PHASE 3: Testing Results Tool (High-Level)

**Goal:** Build a LangChain tool focused on **testing results** (unit tests, integration tests, load tests, etc.) rather than all analysis data.

**Key Tasks:**
- Implement a testing results loader for the metrics JSON files (e.g., unit, integration, performance, reliability, coverage)
- Normalize and validate metric schemas so the agent can compare features consistently
- Provide summarised views (per feature and per environment: dev, UAT, prod where applicable)
- Design tool outputs explicitly around “readiness signals” (e.g., failure rates, coverage thresholds, flaky tests)
- Integrate the Testing Results Tool as a separate LangChain tool the agent can call when reasoning about readiness
- Keep reviews/qualitative feedback for a later phase (or manual inspection), so this phase stays focused on **test data only**
- Write unit tests covering all supported testing metrics data types
- Integrate tool with agent executor
- Update system prompt with tool description

**LangChain Tool Pattern:**
```python
from langchain.tools import tool
from typing import Literal

@tool
def get_testing_results(
    feature_id: str,
    data_type: Literal[
        "metrics/unit_test_results",
        "metrics/test_coverage_report",
        "metrics/performance_benchmarks",
        "metrics/pipeline_results",
        "metrics/security_scan_results",
    ]
) -> dict:
    """Retrieve testing results for a feature.

    Args:
        feature_id: The feature identifier (e.g., "FEAT-MS-001")
        data_type: Type of testing results to retrieve

    Returns:
        Dictionary with the requested testing metrics
    """
    # Implementation here
    pass
```

**Acceptance Criteria:**
- Tool retrieves all supported testing metrics data types
- Handles missing files gracefully with clear errors
- Agent calls multiple testing result types during assessment
- Tool execution traced via callbacks
- Manual CLI test shows multi-metric testing workflow

**Example normalized metrics summary (readiness signals for one feature/environment):**
```json
{
  "feature_id": "FEAT-RS-001",
  "environment": "uat",
  "tests": {
    "unit": {"passed": 128, "failed": 2, "flake_rate": 0.01},
    "integration": {"passed": 40, "failed": 0}
  },
  "coverage": {"line": 0.86, "branch": 0.79},
  "readiness_signals": {
    "overall": "borderline",
    "blocked": false,
    "notes": ["coverage below 0.90 target in UAT"]
  }
}
```

---

## PHASE 4: Observability Tracing (High-Level)

**Goal:** Extend the basic tracing from Step 1.4 into rich observability for the Investigator Agent using OpenTelemetry and LangChain callbacks so you can debug and understand behavior and cost.

**Key Tasks:**
- Instrument all LLM calls and tool calls with OpenTelemetry spans
- Include key attributes: model name, tokens in/out, latency, tool names, feature IDs
- Persist traces to JSON files under `data/traces/` for offline inspection
- Add a simple trace viewer script (e.g., pretty-print recent spans grouped by conversation)
- Wire tracing callbacks into the CLI workflow
- Document how to use traces to debug readiness decisions

**Implementation Sketch:**
```python
# In observability/tracer.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExporter, SpanExportResult


class FileSpanExporter(SpanExporter):
    def export(self, spans: list[trace.Span]) -> SpanExportResult:
        # Write spans to JSONL file under config.traces_dir
        ...


def setup_tracer(traces_dir: Path) -> trace.Tracer:
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(FileSpanExporter(traces_dir)))
    trace.set_tracer_provider(provider)
    return trace.get_tracer(__name__)
```

**Acceptance Criteria:**
- Every LLM call and tool call produces trace spans
- Traces are written to files under `data/traces/`
- Each span records duration, model, token counts, and tool names
- You can follow a full readiness decision as a trace timeline

---

## PHASE 5: Retry with Exponential Back-off (High-Level)

**Goal:** Make the agent resilient to transient failures (rate limits, network issues, temporary provider errors) using structured retries with exponential back-off.

**Key Tasks:**
- Identify all external calls that can fail transiently (LLM calls, file I/O if needed)
- Implement a small retry utility with exponential back-off and jitter
- Wrap LLM invocations and critical tool operations with this retry logic
- Log retry attempts into traces and/or console output
- Add configuration options for max retries and back-off parameters

**Implementation Sketch:**
```python
import asyncio
import random


async def with_retry(fn, *, retries: int = 3, base_delay: float = 0.5, max_delay: float = 8.0):
    last_exc = None
    for attempt in range(retries):
        try:
            return await fn()
        except Exception as exc:
            last_exc = exc
            delay = min(max_delay, base_delay * (2 ** attempt))
            delay *= 1 + random.random() * 0.25  # jitter
            await asyncio.sleep(delay)
    raise last_exc
```

**Acceptance Criteria:**
- Transient LLM errors no longer crash the CLI
- Retries are visible in logs/traces
- Back-off grows with each failed attempt
- Retry behavior is configurable via settings

---

## PHASE 6: Evaluations (High-Level)

**Goal:** Automated evaluation of agent behavior and decisions using the real incoming_data scenarios.

**Key Tasks:**
- Create 8+ evaluation scenarios using the 4 provided features (and variations)
- Build an evaluation runner that calls the agent programmatically
- Implement scoring for 4 dimensions (identification, tool usage, decision quality, error handling)
- Generate structured JSON reports summarizing performance
- Add baseline comparison capability (e.g., previous run vs current)
- Document how to add new eval cases

**Acceptance Criteria:**
- Eval framework runs automatically from a single command
- Tests all 4 readiness scenarios and additional edge cases
- Achieves >70% pass rate initially (stretch target: >85%)
- Generates machine-readable reports
- Can track regression over time


---

## Next Steps

1. **Review this plan** - Ensure it aligns with your goals and preferences
2. **Start Phase 1** - Begin with Step 1.1 (Project Initialization)
3. **Set up LangChain environment** - Install dependencies with uv
4. **Build incrementally** - Complete each step, test thoroughly, commit progress
5. **Move to Phase 2** - Once Phase 1 is fully working and tested

**Quick Start Commands:**
```bash
cd module7/project

# Ensure Python 3.13.5 is available
python --version  # Must be 3.13.5

# Initialize project with Python 3.13.5
uv venv --python 3.13.5
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies at exact versions
uv sync

# Create .env file
cp .env.example .env

# Get your FREE Groq API key (no credit card required):
# 1. Go to https://console.groq.com
# 2. Sign up for free
# 3. Copy your API key
# 4. Edit .env and set GROQ_API_KEY=your_key_here

# Test basic setup
python -c "import langchain; print('LangChain version:', langchain.__version__)"
# Should output: LangChain version: 0.3.14

# Verify Python version
python -c "import sys; print(f'Python {sys.version}')"
# Should show Python 3.13.5
```

**Remember:**
- Build incrementally - don't skip steps
- We will never accept failing tests, skipped tests, deprecation warnings, or any linting errors/warnings. These should never be skipped or suppressed without the explicit agreement with the human user.
- The code has proper decoupling to ensure ease in future features, maintenance, and fault-finding.
- Code should not be duplicated except through explicit instruction with the human user. When you think you have identified a rare scenario where it makes sense to not adhere to DRY principles, ask the opinion of the human user for guidance about how to proceed.
- Check traces - verify observability
- Refer to DESIGN.md and EXERCISE.md frequently
- Use LangChain documentation: https://python.langchain.com/



