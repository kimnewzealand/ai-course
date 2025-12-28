# Detective Agent Implementation Plan (Python)

## Overview
Python implementation of the Detective Agent. See [DESIGN.md](DESIGN.md) for more about **what** the agent does and **why** design decisions were made.

This document covers **how** to build the agent in Python - specific packages, project structure, testing approach, and implementation details.  

## Implementation Goals
- Clear, readable Python code that shows exactly what's happening
- Multi-provider support (Anthropic, OpenRouter, Ollama, etc)
- OpenTelemetry observability
- Context window management
- Retry mechanism with exponential backoff
- Tool calling foundation
- Interaction persistence
- Basic reasoning and evaluations

## Implementation Constitution
- Clear, readable Python code that shows exactly what's happening
- For interfaces, use Protocol, and DO NOT use an ABC
- Place unit tests in the folder as the code under test
- Unit tests have a `_test.py` suffix and DO NOT have a `test_` prefix
- The `/tests` folder should only contain integration tests and common test assets
- When you're running tests and Python scripts, remember that the `python` binary is in the virtual environment
- Use `uv venv` to create the venv and `uv add` when adding dependencies
- Never use `pip` or `uv pip` and never create `requirements.txt`

## Pythonic Best Practices Applied
This implementation follows modern Python best practices:
- **Type Safety**: TypeAlias for complex types, comprehensive type hints
- **Resource Management**: Async context managers (`__aenter__`/`__aexit__`) for automatic cleanup
- **Configuration**: `pydantic-settings` for environment variable management
- **Error Handling**: Exception chaining with `from e` to preserve stack traces
- **Modern Python**: Pattern matching (match/case), walrus operator where appropriate
- **Performance**: `__slots__` on Pydantic models for reduced memory usage
- **Datetime**: `datetime.now(timezone.utc)` instead of deprecated `utcnow()`
- **Logging**: Structured logging instead of print statements
- **Enums**: Type-safe constants using `str, Enum` pattern
- **Path Handling**: `pathlib.Path` for cross-platform compatibility
- **Documentation**: Google-style docstrings with Args, Returns, Raises sections

## Implementation Steps
The recommended order of implementation is defined in [STEPS.md](STEPS.md). The phases of implementation defined later in this document align with these progression of steps.

## Technology Stack
- **Python 3.13.5** with async/await and modern features (match/case, TypeAlias, etc.)
- **uv** for dependency and venv management
- **httpx** for HTTP client (async, HTTP/2 support)
- **OpenTelemetry SDK** for traces and metrics
- **pydantic** for data validation and models
- **pydantic-settings** for configuration management with environment variables
- **pytest** + **pytest-asyncio** for testing
- **respx** for mocking httpx in tests

## Project Structure

```
module6/project/
├── src/
│   └── detective_agent/
│       ├── __init__.py
│       ├── py.typed                 # PEP 561 marker for type checkers
│       ├── types.py                 # Shared type aliases (MessageList, etc.)
│       ├── config.py                # Configuration management
│       ├── config_test.py           # Configuration test
│       ├── models.py                # Data models (Message, Conversation, etc.)
│       ├── models_test.py           # Data models test
│       ├── conftest.py              # Shared pytest fixtures for unit tests
│       ├── providers/
│       │   ├── __init__.py
│       │   ├── base.py            # Provider Protocol
│       │   ├── openrouter.py      # OpenRouter implementation
│       │   ├── openrouter_test.py  # OpenRouter test
│       │   └── errors.py          # Provider error types
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── base.py            # Tool abstractions
│       │   ├── registry.py        # Tool registry and execution
│       │   ├── registry_test.py    # Tool registry test
│       │   ├── release_tools.py   # Release assessment tools
│       │   ├── release_tools_test.py # Release assessment tools test
│       │   └── errors.py          # Tool error types
│       ├── context/
│       │   ├── __init__.py
│       │   └── truncation.py      # Truncation strategy
│       ├── retry/
│       │   ├── __init__.py
│       │   └── backoff.py         # Retry with exponential backoff
│       ├── observability/
│       │   ├── __init__.py
│       │   ├── tracing.py         # OpenTelemetry tracing
│       │   └── exporter.py        # Filesystem trace export
│       ├── agent.py                # Agent core
│       ├── agent_test.py            # Agent test
│       ├── persistence.py          # Conversation persistence
│       ├── persistence_test.py      # Conversation persistence test
│       └── cli.py                  # CLI interface
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Shared fixtures for integration tests
│   ├── integration/
│   │   ├── conftest.py              # Integration-specific fixtures with mock mode
│   │   └── test_agent_workflow.py
│   └── fixtures/
│       └── mock_releases.json
├── data/
│   ├── conversations/              # Saved conversations
│   │   └── .gitkeep
│   ├── traces/                     # OpenTelemetry traces
│   │   └── .gitkeep
│   └── risk_reports/               # Filed risk reports
│       └── .gitkeep
├── evals/
│   ├── __init__.py
│   ├── scenarios/                  # Evaluation test cases
│   ├── baselines/                  # Baseline results
│   ├── runner.py                   # Evaluation runner
│   └── reports/                    # Evaluation reports
├── .env.example                    # Environment variable template
├── .gitignore                      # Git ignore patterns
├── pyproject.toml                  # Project configuration
└── README.md                       # Project documentation
```

## Step-by-Step Implementation

### Step 1: Say Hello to Your Agent

**Goal:** Build minimal working agent with OpenRouter provider


#### 1.0 Project Setup

**Tasks:**
1. Initialize project with `uv`
2. Set up Python 3.13.5 virtual environment
3. Configure `pyproject.toml` with dependencies
4. Create directory structure
5. Set up basic README
6. Create `.gitignore` file
7. Create `.env.example` file

**Dependencies to add:**
```bash
# Core dependencies
uv add httpx pydantic pydantic-settings

# Testing dependencies (includes coverage for >80% target)
uv add --dev pytest pytest-asyncio respx pytest-cov

# Type checking dependencies
uv add --dev mypy types-respx

# OpenTelemetry dependencies (added in Step 2)
# uv add opentelemetry-api opentelemetry-sdk

# Install all dependencies
uv sync
```

**File:** `pyproject.toml`
```toml
[project]
name = "detective-agent"
version = "0.1.0"
description = "AI agent for release risk assessment"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "httpx>=0.27.0",
    "pydantic>=2.9.0",
    "pydantic-settings>=2.5.0",
    "opentelemetry-api>=1.27.0",
    "opentelemetry-sdk>=1.27.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "pytest-cov>=5.0.0",
    "respx>=0.21.0",
    "mypy>=1.11.0",
    "types-respx>=0.21.0",
]

[project.scripts]
detective-agent = "detective_agent.cli:main_sync"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["src", "tests"]
python_files = ["*_test.py", "test_*.py"]
addopts = "--cov=detective_agent --cov-report=term-missing --cov-fail-under=80"

[tool.mypy]
python_version = "3.13"
strict = true
plugins = ["pydantic.mypy"]

[tool.pydantic-mypy]
init_forbid_extra = true
init_typed = true
warn_required_dynamic_aliases = true

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/detective_agent"]
```

**File:** `.gitignore`
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Environment
.env
.env.local

# Runtime data
data/conversations/*.json
data/traces/*.json
data/risk_reports/*.json

# Keep directory structure
!data/conversations/.gitkeep
!data/traces/.gitkeep
!data/risk_reports/.gitkeep

# Evaluation results
evals/baselines/*.json
evals/reports/*.json

# OS
.DS_Store
Thumbs.db
```

**File:** `.env.example`
```bash
# OpenRouter API Configuration (Required)
OPENROUTER_API_KEY=your-api-key-here

# Optional: Override defaults
# OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free
# OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
# OPENROUTER_TEMPERATURE=0.7
# OPENROUTER_MAX_TOKENS=4096
# OPENROUTER_TIMEOUT=30.0

# Agent Configuration (Optional)
# CONVERSATION_DIR=data/conversations
# TRACE_DIR=data/traces
```

**Acceptance Criteria:**
- ✅ Virtual environment created with `uv venv`
- ✅ All dependencies installed
- ✅ Directory structure matches plan
- ✅ Can run `pytest` (even with no tests yet)
- ✅ `.gitignore` file created
- ✅ `.env.example` file created

#### 1.1 Configuration System

**File:** `src/detective_agent/config.py`

**Implementation:**
```python
from pathlib import Path
from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class ProviderConfig(BaseSettings):
    """Configuration for LLM provider with environment variable support"""
    model_config = SettingsConfigDict(
        env_prefix="OPENROUTER_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    api_key: str  # Reads from OPENROUTER_API_KEY
    model: str = "meta-llama/llama-3.1-8b-instruct:free"  # OPENROUTER_MODEL
    base_url: str = "https://openrouter.ai/api/v1"
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, gt=0)
    timeout: float = 30.0

class AgentConfig(BaseSettings):
    """Main agent configuration with environment variable support"""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    provider: ProviderConfig | None = None
    system_prompt: str = "You are a helpful AI assistant."
    conversation_dir: Path = Path("data/conversations")
    trace_dir: Path = Path("data/traces")

    @model_validator(mode='before')
    @classmethod
    def load_provider_from_env(cls, data: dict) -> dict:
        """Ensure nested ProviderConfig is properly loaded from environment."""
        if 'provider' not in data or data['provider'] is None:
            data['provider'] = ProviderConfig()
        return data

    @field_validator('conversation_dir', 'trace_dir', mode='after')
    @classmethod
    def ensure_directory_exists(cls, v: Path) -> Path:
        """Create directory if it doesn't exist."""
        v.mkdir(parents=True, exist_ok=True)
        return v
```

**Environment Variables (automatically loaded via pydantic-settings):**
- `OPENROUTER_API_KEY`: API key for OpenRouter (required)
- `OPENROUTER_MODEL`: Model to use (default: meta-llama/llama-3.1-8b-instruct:free)
- `OPENROUTER_BASE_URL`: Base URL (default: https://openrouter.ai/api/v1)
- `OPENROUTER_TEMPERATURE`: Temperature (default: 0.7)
- `OPENROUTER_MAX_TOKENS`: Max tokens (default: 4096)
- `OPENROUTER_TIMEOUT`: Timeout in seconds (default: 30.0)

**Tests:** `src/detective_agent/config_test.py`
- Test configuration validation with pydantic-settings
- Test default values
- Test environment variable loading from .env file
- Test missing required fields (OPENROUTER_API_KEY)
- Test invalid values (temperature out of range, etc.)

#### 1.1.1 Shared Type Definitions

**File:** `src/detective_agent/types.py`

**Implementation:**
```python
"""Shared type aliases for the detective agent package.

This module provides a single source of truth for all type aliases
used throughout the codebase, preventing duplication and ensuring consistency.
"""
from typing import Any, Literal, TypeAlias

from detective_agent.models import Message

# Message-related types
MessageList: TypeAlias = list[Message]
MessageRole: TypeAlias = Literal["user", "assistant", "system", "tool"]
MetadataDict: TypeAlias = dict[str, Any]

# Release-related types
ReleaseData: TypeAlias = dict[str, Any]
```

**Note:** Import from this module instead of defining TypeAliases locally:
```python
from detective_agent.types import MessageList, MessageRole
```

#### 1.2 Data Models

**File:** `src/detective_agent/models.py`

**Implementation:**
```python
from datetime import datetime, timezone
from typing import Any, Literal, TypeAlias
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

# Type aliases for clarity
MessageRole: TypeAlias = Literal["user", "assistant", "system", "tool"]
MetadataDict: TypeAlias = dict[str, Any]

class Message(BaseModel):
    """Single message in a conversation"""
    model_config = ConfigDict(frozen=False, slots=True)

    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: MetadataDict = Field(default_factory=dict)

class Conversation(BaseModel):
    """Ongoing dialogue between user and agent"""
    model_config = ConfigDict(frozen=False, slots=True)

    id: str = Field(default_factory=lambda: str(uuid4()))
    system_prompt: str
    messages: list[Message] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: MetadataDict = Field(default_factory=dict)

    def add_message(self, role: MessageRole, content: str) -> Message:
        """Add a message to the conversation.

        Args:
            role: The role of the message sender.
            content: The message content.

        Returns:
            The created Message object.
        """
        msg = Message(role=role, content=content)
        self.messages.append(msg)
        return msg
```

**Tests:** `src/detective_agent/models_test.py`
- Test message creation
- Test conversation creation
- Test add_message method
- Test JSON serialization

#### 1.3 Provider Abstraction

**File:** `src/detective_agent/providers/base.py`

**Implementation:**
```python
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from detective_agent.types import MessageList  # Import from shared types module
from detective_agent.models import Message


@dataclass(frozen=True, slots=True)
class ProviderCapabilities:
    """Capabilities supported by a provider.

    Used to determine what features a provider supports before attempting
    to use them (e.g., tool calling, streaming, vision).
    """
    supports_tools: bool = False
    supports_streaming: bool = False
    supports_vision: bool = False
    max_context_tokens: int = 128000


@runtime_checkable
class Provider(Protocol):
    """Protocol for LLM providers"""

    async def complete(
        self,
        messages: MessageList,
        temperature: float,
        max_tokens: int,
        tools: list[dict] | None = None,  # Added from start for Step 6 compatibility
    ) -> Message:
        """Send messages to LLM and get response.

        Args:
            messages: List of messages in the conversation.
            temperature: Sampling temperature (0.0 to 2.0).
            max_tokens: Maximum tokens to generate.
            tools: Optional list of tool definitions for function calling.

        Returns:
            Assistant's response message.

        Raises:
            ProviderError: If the API call fails.
        """
        ...

    def estimate_tokens(self, messages: MessageList) -> int:
        """Estimate token count for messages.

        Args:
            messages: List of messages to estimate.

        Returns:
            Estimated token count.
        """
        ...

    def get_capabilities(self) -> ProviderCapabilities:
        """Report what this provider supports.

        Returns:
            ProviderCapabilities with flags for supported features.
        """
        ...
```

**File:** `src/detective_agent/providers/errors.py`

**Implementation:**
```python
class ProviderError(Exception):
    """Base provider error"""
    pass

class AuthenticationError(ProviderError):
    """Invalid API key or credentials"""
    pass

class RateLimitError(ProviderError):
    """Provider rate limiting"""
    pass

class ValidationError(ProviderError):
    """Invalid request format"""
    pass

class NetworkError(ProviderError):
    """Connection issues"""
    pass

class TimeoutError(ProviderError):
    """Request timed out - retryable error"""
    pass
```

#### 1.4 OpenRouter Provider Implementation

**File:** `src/detective_agent/providers/openrouter.py`

**Implementation:**
```python
import httpx

from detective_agent.config import ProviderConfig
from detective_agent.models import Message
from detective_agent.types import MessageList  # Import from shared types module
from detective_agent.providers.errors import (
    AuthenticationError,
    NetworkError,
    ProviderError,
    RateLimitError,
    TimeoutError,
    ValidationError,
)

class OpenRouterProvider:
    """OpenRouter API provider with async context manager support"""

    def __init__(self, config: ProviderConfig):
        self.config = config
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "OpenRouterProvider":
        """Enter async context manager and initialize HTTP client"""
        from httpx import Timeout

        self._client = httpx.AsyncClient(
            base_url=self.config.base_url,
            timeout=Timeout(
                connect=5.0,  # Fast fail on connection issues
                read=self.config.timeout,  # Allow longer read for LLM responses
                write=10.0,
                pool=5.0
            ),
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "HTTP-Referer": "https://github.com/yourusername/detective-agent",
                "X-Title": "Detective Agent"
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context manager and cleanup resources"""
        if self._client:
            await self._client.aclose()

    @property
    def client(self) -> httpx.AsyncClient:
        """Get HTTP client, ensuring it's initialized"""
        if self._client is None:
            raise RuntimeError(
                "Provider not initialized. Use 'async with' context manager."
            )
        return self._client

    async def complete(
        self,
        messages: MessageList,
        temperature: float,
        max_tokens: int,
        tools: list[dict] | None = None,
    ) -> Message:
        """Call OpenRouter API to generate completion.

        Args:
            messages: List of messages in the conversation.
            temperature: Sampling temperature (0.0 to 2.0).
            max_tokens: Maximum tokens to generate.
            tools: Optional list of tool definitions for function calling.

        Returns:
            Assistant's response message.

        Raises:
            AuthenticationError: Invalid API key.
            RateLimitError: Rate limit exceeded.
            ValidationError: Invalid request format.
            NetworkError: Connection issues.
            TimeoutError: Request timed out.
            ProviderError: Other API errors.
        """
        # Format messages for OpenAI/OpenRouter API
        formatted_messages = []
        for m in messages:
            msg_dict = {"role": m.role, "content": m.content}

            # Assistant messages may have tool_calls
            if m.role == "assistant" and m.metadata.get("tool_calls"):
                msg_dict["tool_calls"] = m.metadata["tool_calls"]
                # Content can be null when tool_calls present
                if not m.content:
                    msg_dict["content"] = None

            # Tool response messages need tool_call_id
            if m.role == "tool" and m.metadata.get("tool_call_id"):
                msg_dict["tool_call_id"] = m.metadata["tool_call_id"]

            formatted_messages.append(msg_dict)

        request_body = {
            "model": self.config.model,
            "messages": formatted_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if tools:
            request_body["tools"] = tools

        try:
            response = await self.client.post("/chat/completions", json=request_body)
            response.raise_for_status()
            data = response.json()

            message = data["choices"][0]["message"]
            content = message.get("content") or ""  # Content may be None when tool_calls present
            tool_calls = message.get("tool_calls")

            metadata = {
                "model": data.get("model"),
                "usage": data.get("usage", {}),
                "provider": "openrouter"
            }

            # Include tool_calls in metadata if present
            if tool_calls:
                metadata["tool_calls"] = tool_calls

            return Message(role="assistant", content=content, metadata=metadata)

        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out: {str(e)}") from e
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Invalid API key") from e
            elif e.response.status_code == 429:
                raise RateLimitError("Rate limit exceeded") from e
            elif e.response.status_code == 400:
                raise ValidationError(f"Invalid request: {e.response.text}") from e
            else:
                raise ProviderError(
                    f"HTTP {e.response.status_code}: {e.response.text}"
                ) from e
        except httpx.RequestError as e:
            raise NetworkError(f"Network error: {str(e)}") from e

    def estimate_tokens(self, messages: MessageList) -> int:
        """Rough token estimation (4 chars ≈ 1 token).

        Uses ~4 chars per token for content, plus overhead per message.

        Args:
            messages: List of messages to estimate.

        Returns:
            Estimated token count.
        """
        content_tokens = sum(len(m.content) for m in messages) // 4
        # Add ~4 tokens overhead per message for role, delimiters
        message_overhead = len(messages) * 4
        return content_tokens + message_overhead

    def get_capabilities(self) -> ProviderCapabilities:
        """Report OpenRouter provider capabilities.

        Returns:
            ProviderCapabilities indicating OpenRouter supports tools.
        """
        return ProviderCapabilities(
            supports_tools=True,
            supports_streaming=False,  # Not implemented yet
            supports_vision=False,  # Model-dependent
            max_context_tokens=128000,  # Llama 3.1 context window
        )
```

**Tests:** `src/detective_agent/providers/openrouter_test.py`
- Test successful completion (using respx to mock)
- Test error handling (401, 429, 400, 500) with exception chaining
- Test token estimation
- Test message formatting
- Test async context manager (__aenter__ and __aexit__)
- Test client property raises error when not initialized
- Test get_capabilities returns correct values

#### 1.5 Conversation Persistence

**File:** `src/detective_agent/persistence.py`

**Implementation:**
```python
import json
from pathlib import Path
from detective_agent.models import Conversation

class ConversationStore:
    """Filesystem-based conversation persistence"""

    def __init__(self, base_dir: str = "data/conversations"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save(self, conversation: Conversation) -> None:
        """Save conversation to filesystem"""
        file_path = self.base_dir / f"{conversation.id}.json"
        with open(file_path, "w") as f:
            json.dump(conversation.model_dump(), f, indent=2, default=str)

    def load(self, conversation_id: str) -> Conversation:
        """Load conversation from filesystem"""
        file_path = self.base_dir / f"{conversation_id}.json"
        with open(file_path, "r") as f:
            data = json.load(f)
        return Conversation.model_validate(data)

    def list_conversations(self) -> list[str]:
        """List all conversation IDs"""
        return [f.stem for f in self.base_dir.glob("*.json")]
```

**Tests:** `src/detective_agent/persistence_test.py`
- Test save conversation
- Test load conversation
- Test list conversations
- Test round-trip (save then load)

#### 1.6 Agent Core (Basic)

**File:** `src/detective_agent/agent.py`

**Implementation:**
```python
from detective_agent.models import Conversation, Message
from detective_agent.providers.base import Provider
from detective_agent.config import AgentConfig
from detective_agent.persistence import ConversationStore

class DetectiveAgent:
    """Core agent orchestration"""

    def __init__(
        self,
        provider: Provider,
        config: AgentConfig,
        conversation: Conversation | None = None
    ):
        self.provider = provider
        self.config = config
        self.conversation = conversation or Conversation(
            system_prompt=config.system_prompt
        )
        self.store = ConversationStore(config.conversation_dir)

    async def send_message(self, content: str) -> str:
        """Send user message and get assistant response"""
        # Add user message
        self.conversation.add_message("user", content)

        # Prepare messages for provider (system + history)
        messages = [
            Message(role="system", content=self.conversation.system_prompt)
        ] + self.conversation.messages

        # Call provider
        response = await self.provider.complete(
            messages=messages,
            temperature=self.config.provider.temperature,
            max_tokens=self.config.provider.max_tokens,
        )

        # Add assistant response to conversation
        self.conversation.messages.append(response)

        # Save conversation
        self.store.save(self.conversation)

        return response.content

    def get_history(self, limit: int | None = None) -> list[Message]:
        """Get conversation history"""
        if limit:
            return self.conversation.messages[-limit:]
        return self.conversation.messages

    def new_conversation(self) -> None:
        """Start a new conversation"""
        self.conversation = Conversation(
            system_prompt=self.config.system_prompt
        )
```

**Tests:** `src/detective_agent/agent_test.py`
- Test send_message
- Test conversation history
- Test new_conversation
- Test persistence integration

#### 1.7 CLI Interface

**File:** `src/detective_agent/cli.py`

**Implementation:**
```python
import asyncio
import logging

from pydantic import ValidationError

from detective_agent.agent import DetectiveAgent
from detective_agent.config import AgentConfig
from detective_agent.providers.openrouter import OpenRouterProvider

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    """CLI for interacting with the agent"""
    # Load configuration from environment
    try:
        config = AgentConfig()
    except ValidationError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Make sure OPENROUTER_API_KEY is set in .env file")
        return

    logger.info("Detective Agent CLI started")
    logger.info(f"Using model: {config.provider.model}")

    print("Detective Agent CLI")
    print("Type 'exit' to quit, 'new' for new conversation, 'history' to see messages")
    print("-" * 60)

    # Use async context manager for automatic cleanup
    async with OpenRouterProvider(config.provider) as provider:
        agent = DetectiveAgent(provider, config)

        while True:
            try:
                user_input = input("\nYou: ").strip()
            except (EOFError, KeyboardInterrupt):
                logger.info("Received interrupt signal")
                break

            # Use pattern matching for command handling
            match user_input.lower():
                case "exit" | "quit":
                    logger.info("User requested exit")
                    break
                case "new":
                    agent.new_conversation()
                    logger.info("Started new conversation")
                    print("Started new conversation")
                case "history":
                    for msg in agent.get_history():
                        print(f"{msg.role}: {msg.content[:100]}...")
                case "" | None:
                    continue
                case _:
                    try:
                        response = await agent.send_message(user_input)
                        print(f"\nAssistant: {response}")
                    except Exception as e:
                        logger.error(f"Error processing message: {e}", exc_info=True)
                        print(f"Error: {e}")

    logger.info("Detective Agent CLI stopped")

def main_sync():
    """Synchronous wrapper for console script entry point.

    This enables the 'detective-agent' command via pyproject.toml scripts.
    """
    asyncio.run(main())

if __name__ == "__main__":
    main_sync()
```

**Acceptance Criteria for Step 1:**
- ✅ CLI starts and connects to OpenRouter using pydantic-settings
- ✅ User can send messages and receive responses
- ✅ Conversation history maintained in memory
- ✅ Conversations saved to filesystem as JSON
- ✅ Can continue previous conversations
- ✅ Proper error handling with exception chaining
- ✅ Async context manager for resource cleanup
- ✅ Logging instead of print statements
- ✅ Pattern matching for CLI commands
- ✅ Type aliases for complex types
- ✅ At least 3 automated tests per module
- ✅ Provider abstraction interface defined
- ✅ Provider reports capabilities via `get_capabilities()` method

**Deferred to Step 2 (Observability):**
- `get_context()` method on DetectiveAgent - provides conversation metadata including message count, token usage, provider info, trace IDs, and tool calls. This is deferred because it depends on tracing infrastructure from Step 2.

---

### Step 2: Observability (Traces and Spans)

**Goal:** Add OpenTelemetry visibility into agent operations

#### 2.1 OpenTelemetry Setup

**File:** `src/detective_agent/observability/tracing.py`

**Implementation:**
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from detective_agent.observability.exporter import FilesystemSpanExporter

# Initialize tracer provider
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

def init_tracing(trace_dir: str = "data/traces"):
    """Initialize OpenTelemetry tracing with filesystem export"""
    exporter = FilesystemSpanExporter(trace_dir)
    span_processor = SimpleSpanProcessor(exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)
```

#### 2.2 Filesystem Trace Exporter

**File:** `src/detective_agent/observability/exporter.py`

**Implementation:**
```python
import json
from pathlib import Path
from datetime import datetime
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
from opentelemetry.sdk.trace import ReadableSpan

class FilesystemSpanExporter(SpanExporter):
    """Export spans to filesystem as JSON.

    Writes traces immediately to prevent data loss on crash.
    Each span is appended to its trace file as it's exported.
    """

    def __init__(self, base_dir: str = "data/traces"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def export(self, spans: list[ReadableSpan]) -> SpanExportResult:
        """Export spans to filesystem immediately.

        Writes each span to disk as it's received to prevent
        data loss on crash. Appends to existing trace files.
        """
        for span in spans:
            trace_id = format(span.context.trace_id, '032x')
            file_path = self.base_dir / f"{trace_id}.json"

            span_data = {
                "name": span.name,
                "trace_id": trace_id,
                "span_id": format(span.context.span_id, '016x'),
                "parent_span_id": format(span.parent.span_id, '016x') if span.parent else None,
                "start_time": span.start_time,
                "end_time": span.end_time,
                "duration_ns": span.end_time - span.start_time,
                "attributes": dict(span.attributes) if span.attributes else {},
                "status": str(span.status),
            }

            # Append to existing trace file or create new one
            if file_path.exists():
                with open(file_path, "r+") as f:
                    data = json.load(f)
                    data["spans"].append(span_data)
                    f.seek(0)
                    json.dump(data, f, indent=2, default=str)
                    f.truncate()
            else:
                with open(file_path, "w") as f:
                    json.dump({
                        "trace_id": trace_id,
                        "spans": [span_data]
                    }, f, indent=2, default=str)

        return SpanExportResult.SUCCESS

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        """Flush is a no-op since we write immediately."""
        return True

    def shutdown(self) -> None:
        """Shutdown exporter - nothing to flush since we write immediately."""
        pass
```

#### 2.3 Instrument Agent Operations

**Update:** `src/detective_agent/agent.py`

Add tracing to `send_message`:
```python
from detective_agent.observability.tracing import tracer

async def send_message(self, content: str) -> str:
    """Send user message and get assistant response"""
    with tracer.start_as_current_span("agent.send_message") as span:
        span.set_attribute("conversation.id", self.conversation.id)
        span.set_attribute("message.content_length", len(content))

        # Add user message
        self.conversation.add_message("user", content)

        # Prepare messages
        messages = [
            Message(role="system", content=self.conversation.system_prompt)
        ] + self.conversation.messages

        # Call provider (will create child span)
        response = await self.provider.complete(
            messages=messages,
            temperature=self.config.provider.temperature,
            max_tokens=self.config.provider.max_tokens,
        )

        # Track token usage
        if "usage" in response.metadata:
            usage = response.metadata["usage"]
            span.set_attribute("tokens.input", usage.get("prompt_tokens", 0))
            span.set_attribute("tokens.output", usage.get("completion_tokens", 0))
            span.set_attribute("tokens.total", usage.get("total_tokens", 0))

        # Add response and save
        self.conversation.messages.append(response)
        self.store.save(self.conversation)

        span.set_attribute("conversation.message_count", len(self.conversation.messages))

        return response.content
```

#### 2.4 Instrument Provider Calls

**Update:** `src/detective_agent/providers/openrouter.py`

Add tracing to `complete`:
```python
from detective_agent.observability.tracing import tracer

async def complete(self, messages: list[Message], temperature: float, max_tokens: int) -> Message:
    """Call OpenRouter API"""
    with tracer.start_as_current_span("provider.complete") as span:
        span.set_attribute("provider.name", "openrouter")
        span.set_attribute("provider.model", self.config.model)
        span.set_attribute("provider.temperature", temperature)
        span.set_attribute("provider.max_tokens", max_tokens)
        span.set_attribute("provider.message_count", len(messages))

        try:
            response = await self.client.post(...)
            # ... existing code ...

            # Add usage metrics to span
            if "usage" in data:
                usage = data["usage"]
                span.set_attribute("tokens.input", usage.get("prompt_tokens", 0))
                span.set_attribute("tokens.output", usage.get("completion_tokens", 0))

            return Message(...)
        except Exception as e:
            from opentelemetry.trace import StatusCode
            span.record_exception(e)
            span.set_status(StatusCode.ERROR, str(e))  # Mark span as error
            raise
```

#### 2.5 Link Traces to Conversations

**Update:** `src/detective_agent/models.py`

Add trace_id to Conversation metadata:
```python
from opentelemetry import trace

class Conversation(BaseModel):
    # ... existing fields ...

    def __init__(self, **data):
        super().__init__(**data)
        # Capture trace ID when conversation starts
        if "trace_id" not in self.metadata:
            current_span = trace.get_current_span()
            if current_span.is_recording():
                trace_id = format(current_span.get_span_context().trace_id, '032x')
                self.metadata["trace_id"] = trace_id
```

**Acceptance Criteria for Step 2:**
- ✅ Each conversation has unique trace ID
- ✅ Traces saved to filesystem as JSON
- ✅ Spans capture operation name, duration, timestamps
- ✅ Provider spans include model, tokens, duration
- ✅ Conversation spans include message count, total tokens
- ✅ Trace files are human-readable
- ✅ Can correlate conversation JSON with trace JSON
- ✅ Automated tests verify trace generation

---

### Step 3: Context Window Management [DEFERRED]

> **⚠️ DEFERRED**: This step is deferred and will not be implemented at this time.

**Goal:** Handle conversations exceeding token limits using truncation strategy

#### 3.1 Truncation Strategy Implementation

**File:** `src/detective_agent/context/truncation.py`

**Implementation:**
```python
from detective_agent.models import Message, Conversation
from detective_agent.providers.base import Provider

class TruncationStrategy:
    """Keep last N messages when approaching token limit"""

    def __init__(
        self,
        max_messages: int = 6,  # Last 6 messages (3 user + 3 assistant)
        token_limit: int = 100000,  # Model's context window
        reserve_tokens: int = 4096,  # Reserve for response
        safety_margin: float = 0.1,  # 10% buffer
    ):
        self.max_messages = max_messages
        self.token_limit = token_limit
        self.reserve_tokens = reserve_tokens
        self.safety_margin = safety_margin

    def manage_context(
        self,
        conversation: Conversation,
        provider: Provider
    ) -> list[Message]:
        """Return messages that fit within token budget"""
        # Always include system prompt
        system_msg = Message(role="system", content=conversation.system_prompt)

        # Calculate available tokens
        available_tokens = int(
            (self.token_limit - self.reserve_tokens) * (1 - self.safety_margin)
        )

        # Start with system prompt
        messages = [system_msg]
        system_tokens = provider.estimate_tokens([system_msg])
        used_tokens = system_tokens

        # Take last N messages
        recent_messages = conversation.messages[-self.max_messages:]

        # Add messages while under budget
        for msg in recent_messages:
            msg_tokens = provider.estimate_tokens([msg])
            if used_tokens + msg_tokens <= available_tokens:
                messages.append(msg)
                used_tokens += msg_tokens
            else:
                # Hit token limit, stop adding messages
                break

        return messages

    def get_context_stats(
        self,
        conversation: Conversation,
        provider: Provider
    ) -> dict:
        """Get context window utilization stats"""
        managed_messages = self.manage_context(conversation, provider)
        used_tokens = provider.estimate_tokens(managed_messages)

        return {
            "total_messages": len(conversation.messages),
            "included_messages": len(managed_messages) - 1,  # Exclude system
            "truncated_messages": len(conversation.messages) - (len(managed_messages) - 1),
            "used_tokens": used_tokens,
            "available_tokens": self.token_limit - self.reserve_tokens,
            "utilization": used_tokens / (self.token_limit - self.reserve_tokens),
        }
```

**Tests:** `src/detective_agent/context/truncation_test.py`
- Test truncation with short conversation (no truncation needed)
- Test truncation with long conversation (truncation applied)
- Test system prompt always preserved
- Test token budget calculation
- Test context stats

#### 3.2 Integrate Context Management into Agent

**Update:** `src/detective_agent/agent.py`

```python
from detective_agent.context.truncation import TruncationStrategy

class DetectiveAgent:
    def __init__(self, provider: Provider, config: AgentConfig, conversation: Conversation | None = None):
        # ... existing code ...
        self.context_strategy = TruncationStrategy(
            max_messages=6,  # User preference: last 6 messages
            token_limit=100000,  # Claude's context window
        )

    async def send_message(self, content: str) -> str:
        """Send user message and get assistant response"""
        with tracer.start_as_current_span("agent.send_message") as span:
            # ... add user message ...

            # Manage context window
            with tracer.start_as_current_span("agent.manage_context"):
                messages = self.context_strategy.manage_context(
                    self.conversation,
                    self.provider
                )

                # Add context stats to span
                stats = self.context_strategy.get_context_stats(
                    self.conversation,
                    self.provider
                )
                span.set_attribute("context.total_messages", stats["total_messages"])
                span.set_attribute("context.included_messages", stats["included_messages"])
                span.set_attribute("context.truncated_messages", stats["truncated_messages"])
                span.set_attribute("context.used_tokens", stats["used_tokens"])
                span.set_attribute("context.utilization", stats["utilization"])

            # Call provider with managed messages
            response = await self.provider.complete(
                messages=messages,
                temperature=self.config.provider.temperature,
                max_tokens=self.config.provider.max_tokens,
            )

            # ... rest of existing code ...
```

**Acceptance Criteria for Step 3:** [DEFERRED]
- ⏸️ Agent calculates token count before each call
- ⏸️ Conversation truncates when needed
- ⏸️ System prompt always preserved
- ⏸️ Last 6 messages preserved (3 user + 3 assistant)
- ⏸️ Context window state visible in traces
- ⏸️ Long conversations don't cause API errors
- ⏸️ Automated tests verify truncation behavior

---

### Step 4: Retry Mechanism

**Goal:** Handle transient failures with exponential backoff

#### 4.1 Retry Configuration and Logic

**File:** `src/detective_agent/retry/backoff.py`

**Implementation:**
```python
import asyncio
import random
from typing import TypeVar, Callable, Awaitable
from detective_agent.providers.errors import (
    RateLimitError, NetworkError, ProviderError, TimeoutError,
    AuthenticationError, ValidationError
)
from detective_agent.observability.tracing import tracer

T = TypeVar('T')

class RetryConfig:
    """Configuration for retry behavior"""
    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_factor: float = 2.0,
        jitter: bool = True,
    ):
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.jitter = jitter

async def execute_with_retry(
    operation: Callable[[], Awaitable[T]],
    config: RetryConfig,
    operation_name: str = "operation"
) -> T:
    """Execute operation with retry logic"""
    last_exception = None

    for attempt in range(1, config.max_attempts + 1):
        with tracer.start_as_current_span(f"retry.{operation_name}") as span:
            span.set_attribute("retry.attempt", attempt)
            span.set_attribute("retry.max_attempts", config.max_attempts)

            try:
                result = await operation()
                if attempt > 1:
                    span.set_attribute("retry.succeeded_after_retries", True)
                return result

            except (RateLimitError, NetworkError, TimeoutError, ProviderError) as e:
                last_exception = e
                span.record_exception(e)
                span.set_attribute("retry.error_type", type(e).__name__)

                if attempt < config.max_attempts:
                    # Calculate backoff delay
                    delay = min(
                        config.initial_delay * (config.backoff_factor ** (attempt - 1)),
                        config.max_delay
                    )

                    # Add jitter
                    if config.jitter:
                        delay = delay * (0.5 + random.random())

                    span.set_attribute("retry.backoff_delay", delay)

                    await asyncio.sleep(delay)
                else:
                    span.set_attribute("retry.exhausted", True)

            except (AuthenticationError, ValidationError) as e:
                # Don't retry these errors
                span.record_exception(e)
                span.set_attribute("retry.non_retryable", True)
                raise

    # All retries exhausted
    raise last_exception
```

**Tests:** `src/detective_agent/retry/backoff_test.py`
- Test successful operation (no retry)
- Test retry on RateLimitError
- Test retry on NetworkError
- Test retry on TimeoutError
- Test exponential backoff calculation
- Test jitter application
- Test max attempts exhausted
- Test non-retryable errors fail immediately

#### 4.2 Integrate Retry into Provider

**Update:** `src/detective_agent/providers/openrouter.py`

```python
from detective_agent.retry.backoff import execute_with_retry, RetryConfig

class OpenRouterProvider:
    def __init__(self, config: ProviderConfig):
        # ... existing code ...
        self.retry_config = RetryConfig(
            max_attempts=3,
            initial_delay=1.0,
            backoff_factor=2.0,
        )

    async def complete(self, messages: list[Message], temperature: float, max_tokens: int) -> Message:
        """Call OpenRouter API with retry logic"""
        async def _make_request():
            with tracer.start_as_current_span("provider.complete") as span:
                # ... existing implementation ...
                return Message(...)

        return await execute_with_retry(
            _make_request,
            self.retry_config,
            operation_name="provider.complete"
        )
```

**Acceptance Criteria for Step 4:**
- ✅ Rate limit errors trigger retries
- ✅ Retries use exponential backoff
- ✅ Max retry attempts configurable
- ✅ Jitter added to prevent thundering herd
- ✅ Auth/validation errors fail immediately
- ✅ Retry attempts tracked in traces
- ✅ Automated tests verify retry behavior

---

### Step 5: System Prompt Engineering

**Goal:** Give agent clear purpose and instructions

**Update:** `src/detective_agent/config.py`

```python
DEFAULT_SYSTEM_PROMPT = """You are a Detective Agent, part of a Release Confidence System.

Your role is to investigate software releases and assess their risk level.

When analyzing a release, you should:
1. Retrieve the release summary using the get_release_summary tool
2. Carefully analyze the data for potential risks:
   - Test failures (especially in critical areas)
   - Elevated error rates or degraded performance metrics
   - High-impact changes (payment processing, authentication, etc.)
3. File a risk report using the file_risk_report tool with:
   - Severity: "high", "medium", or "low"
   - Clear findings explaining your assessment

Risk Assessment Guidelines:
- HIGH: Test failures in critical areas, elevated error rates (>5%), risky changes
- MEDIUM: Minor test failures, slight metric degradation, moderate changes
- LOW: All tests passing, healthy metrics, low-impact changes

Be thorough, objective, and clear in your analysis."""

class AgentConfig(BaseModel):
    # ... existing fields ...
    system_prompt: str = DEFAULT_SYSTEM_PROMPT
```

**Acceptance Criteria for Step 5:**
- ✅ Default system prompt defines agent purpose
- ✅ System prompt explains tool usage
- ✅ System prompt is easily configurable
- ✅ Agent behavior reflects instructions
- ✅ Tested with various prompts

---

### Step 6: Tool Abstraction

**Goal:** Enable agent to use tools for release risk assessment

#### 6.1 Tool Data Models

**Update:** `src/detective_agent/models.py`

Add tool-related models:
```python
from typing import Callable, Awaitable
from datetime import datetime, timezone

class ToolDefinition(BaseModel):
    """Definition of a callable tool"""
    name: str
    description: str
    parameters: dict[str, Any]  # JSON schema
    handler: Callable[[dict], Awaitable[Any]] = Field(exclude=True)

class ToolCall(BaseModel):
    """Request from LLM to execute a tool"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    arguments: dict[str, Any]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ToolResult(BaseModel):
    """Result of tool execution"""
    tool_call_id: str
    content: str
    success: bool
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = Field(default_factory=dict)
```

#### 6.2 Tool Errors

**File:** `src/detective_agent/tools/errors.py`

```python
class ToolError(Exception):
    """Base tool error"""
    pass

class ToolNotFoundError(ToolError):
    """Requested tool not registered"""
    pass

class InvalidArgumentsError(ToolError):
    """Arguments don't match schema"""
    pass

class ToolExecutionError(ToolError):
    """Tool handler raised an exception"""
    pass

class ToolTimeoutError(ToolError):
    """Tool execution exceeded time limit"""
    pass
```

#### 6.3 Tool Registry

**File:** `src/detective_agent/tools/registry.py`

```python
from detective_agent.models import ToolDefinition, ToolCall, ToolResult
from detective_agent.tools.errors import (
    ToolNotFoundError, InvalidArgumentsError, ToolExecutionError
)
from detective_agent.observability.tracing import tracer

class ToolRegistry:
    """Registry for managing and executing tools"""

    def __init__(self):
        self.tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        """Register a tool"""
        self.tools[tool.name] = tool

    def get_tools(self) -> list[ToolDefinition]:
        """Get all registered tools"""
        return list(self.tools.values())

    async def execute(self, tool_call: ToolCall) -> ToolResult:
        """Execute a tool call"""
        with tracer.start_as_current_span("tool.execute") as span:
            span.set_attribute("tool.name", tool_call.name)
            span.set_attribute("tool.call_id", tool_call.id)

            # Find tool
            if tool_call.name not in self.tools:
                raise ToolNotFoundError(f"Tool '{tool_call.name}' not found")

            tool = self.tools[tool_call.name]

            try:
                # Execute handler
                result = await tool.handler(tool_call.arguments)

                span.set_attribute("tool.success", True)

                return ToolResult(
                    tool_call_id=tool_call.id,
                    content=str(result),
                    success=True,
                    metadata={"tool_name": tool_call.name}
                )

            except Exception as e:
                span.record_exception(e)
                span.set_attribute("tool.success", False)

                return ToolResult(
                    tool_call_id=tool_call.id,
                    content=f"Error: {str(e)}",
                    success=False,
                    metadata={"tool_name": tool_call.name, "error": str(e)}
                )

    def format_for_anthropic(self) -> list[dict]:
        """Format tools for Anthropic API"""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.parameters
            }
            for tool in self.tools.values()
        ]
```

**Tests:** `src/detective_agent/tools/registry_test.py`
- Test tool registration
- Test tool execution success
- Test tool execution failure
- Test tool not found error
- Test format for Anthropic API

#### 6.4 Release Assessment Tools

**File:** `src/detective_agent/tools/release_tools.py`

Release data is loaded from `releases.json` file instead of hardcoded mock data.
This allows the agent to work with real release information.

```python
import json
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, TypeAlias

# Type aliases
ReleaseData: TypeAlias = dict[str, Any]

# Default path to releases.json (relative to project root)
DEFAULT_RELEASES_PATH = Path("releases.json")

class RiskSeverity(str, Enum):
    """Risk severity levels for release assessments"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ReleaseDataError(Exception):
    """Error loading or parsing release data."""
    pass

def load_releases(releases_path: Path | None = None) -> dict[str, ReleaseData]:
    """Load release data from JSON file.

    Args:
        releases_path: Path to the releases.json file. Defaults to project root.

    Returns:
        Dictionary mapping release IDs to release data.

    Raises:
        ReleaseDataError: If file not found or JSON parsing fails.
    """
    path = releases_path or DEFAULT_RELEASES_PATH

    if not path.exists():
        raise ReleaseDataError(f"Releases file not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        raise ReleaseDataError(f"Invalid JSON in releases file: {e}") from e

async def get_release_summary(
    args: dict[str, Any], releases_path: Path | None = None
) -> ReleaseData:
    """Get release summary tool handler.

    Args:
        args: Dictionary containing release_id.
        releases_path: Optional path to releases.json for testing.

    Returns:
        Release data dictionary or error.
    """
    release_id = args.get("release_id", "")

    try:
        releases = load_releases(releases_path)
    except ReleaseDataError as e:
        return {"error": str(e)}

    if release_id in releases:
        return releases[release_id]
    else:
        return {"error": f"Release {release_id} not found", "available_releases": list(releases.keys())}

async def file_risk_report(args: dict[str, Any]) -> dict[str, str]:
    """File risk report tool handler.

    Args:
        args: Dictionary containing release_id, severity, and findings.

    Returns:
        Status dictionary with report information.

    Raises:
        ValueError: If severity is invalid.
    """
    release_id = args.get("release_id")
    severity_str = args.get("severity")
    findings = args.get("findings", [])

    # Validate severity using Enum
    try:
        severity = RiskSeverity(severity_str)
    except ValueError as e:
        valid_severities = ", ".join(s.value for s in RiskSeverity)
        raise ValueError(
            f"Invalid severity: {severity_str}. Must be one of: {valid_severities}"
        ) from e

    # Save report to filesystem
    report_dir = Path("data/risk_reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "release_id": release_id,
        "severity": severity.value,
        "findings": findings,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    report_file = report_dir / f"{release_id}_risk_report.json"
    report_file.write_text(json.dumps(report, indent=2))

    return {
        "status": "success",
        "report_id": f"{release_id}_risk_report",
        "message": f"Risk report filed for {release_id} with severity: {severity.value}"
    }

# Tool definitions
GET_RELEASE_SUMMARY_TOOL = ToolDefinition(
    name="get_release_summary",
    description="Retrieve high-level release information including version, changes, test results, and deployment metrics",
    parameters={
        "type": "object",
        "properties": {
            "release_id": {
                "type": "string",
                "description": "The release version identifier (e.g., 'v2.1.0')"
            }
        },
        "required": ["release_id"]
    },
    handler=get_release_summary
)

FILE_RISK_REPORT_TOOL = ToolDefinition(
    name="file_risk_report",
    description="File a risk assessment report for a release with severity level and findings",
    parameters={
        "type": "object",
        "properties": {
            "release_id": {
                "type": "string",
                "description": "The release version identifier"
            },
            "severity": {
                "type": "string",
                "enum": ["high", "medium", "low"],
                "description": "Risk severity level"
            },
            "findings": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of key findings and concerns"
            }
        },
        "required": ["release_id", "severity", "findings"]
    },
    handler=file_risk_report
)
```

**Tests:** `src/detective_agent/tools/release_tools_test.py`

Tests use a `MOCK_RELEASES` fixture to provide test data without reading from the actual `releases.json` file, maintaining test isolation:

```python
import pytest
from pathlib import Path
import tempfile
import json

# Test fixture for mock release data
MOCK_RELEASES = {
    "v2.1.0": {
        "version": "v2.1.0",
        "changes": ["Added payment processing", "Fixed authentication bug"],
        "tests": {"passed": 142, "failed": 2, "skipped": 5},
        "deployment_metrics": {"error_rate": 0.02, "response_time_p95": 450}
    },
    "v2.0.0": {
        "version": "v2.0.0",
        "changes": ["Minor UI updates"],
        "tests": {"passed": 149, "failed": 0, "skipped": 0},
        "deployment_metrics": {"error_rate": 0.001, "response_time_p95": 320}
    }
}

@pytest.fixture
def mock_releases_file(tmp_path):
    """Create a temporary releases.json file for testing."""
    releases_file = tmp_path / "releases.json"
    releases_file.write_text(json.dumps(MOCK_RELEASES))
    return releases_file
```

Test cases:
- Test get_release_summary with valid release (using fixture)
- Test get_release_summary with invalid release
- Test list_releases functionality
- Test file_risk_report with valid data
- Test file_risk_report with invalid severity
- Test report file creation
- Test error handling for file not found
- Test error handling for invalid JSON

#### 6.5 Update Provider for Tool Calling

**Update:** `src/detective_agent/providers/openrouter.py`

Add tool support to complete method:
```python
async def complete(
    self,
    messages: list[Message],
    temperature: float,
    max_tokens: int,
    tools: list[dict] | None = None,
) -> Message:
    """Call OpenRouter API with optional tool support"""
    with tracer.start_as_current_span("provider.complete") as span:
        # ... existing span attributes ...

        request_body = {
            "model": self.config.model,
            "messages": [
                {"role": m.role, "content": m.content}
                for m in messages
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        # Add tools if provided
        if tools:
            request_body["tools"] = tools
            span.set_attribute("provider.tools_count", len(tools))

        try:
            response = await self.client.post("/chat/completions", json=request_body)
            response.raise_for_status()
            data = response.json()

            choice = data["choices"][0]
            message = choice["message"]

            # Check for tool calls
            tool_calls = message.get("tool_calls", [])

            metadata = {
                "model": data.get("model"),
                "usage": data.get("usage", {}),
                "provider": "openrouter",
            }

            if tool_calls:
                metadata["tool_calls"] = tool_calls
                span.set_attribute("provider.tool_calls_count", len(tool_calls))

            return Message(
                role="assistant",
                content=message.get("content", ""),
                metadata=metadata
            )

        except Exception as e:
            # ... existing error handling ...
```

#### 6.6 Integrate Tool Loop into Agent

**Update:** `src/detective_agent/agent.py`

```python
import json
from detective_agent.tools.registry import ToolRegistry
from detective_agent.models import ToolCall, ToolResult, ToolDefinition

class DetectiveAgent:
    def __init__(self, provider: Provider, config: AgentConfig, conversation: Conversation | None = None):
        # ... existing code ...
        self.tool_registry = ToolRegistry()

    def register_tool(self, tool: ToolDefinition) -> None:
        """Register a tool with the agent"""
        self.tool_registry.register(tool)

    async def send_message(self, content: str) -> str:
        """Send user message and get assistant response with tool loop"""
        with tracer.start_as_current_span("agent.send_message") as span:
            # Add user message
            self.conversation.add_message("user", content)

            # Tool loop
            max_iterations = 10
            for iteration in range(max_iterations):
                with tracer.start_as_current_span("agent.tool_loop_iteration") as iter_span:
                    iter_span.set_attribute("iteration", iteration)

                    # Manage context
                    messages = self.context_strategy.manage_context(
                        self.conversation,
                        self.provider
                    )

                    # Get tools formatted for provider
                    tools = self.tool_registry.format_for_anthropic() if self.tool_registry.get_tools() else None

                    # Call provider
                    response = await self.provider.complete(
                        messages=messages,
                        temperature=self.config.provider.temperature,
                        max_tokens=self.config.provider.max_tokens,
                        tools=tools,
                    )

                    # Check for tool calls
                    tool_calls_data = response.metadata.get("tool_calls", [])

                    if not tool_calls_data:
                        # No tool calls, we're done
                        self.conversation.messages.append(response)
                        self.store.save(self.conversation)
                        return response.content

                    # Execute tool calls
                    iter_span.set_attribute("tool_calls_count", len(tool_calls_data))

                    # Add assistant message with tool calls
                    self.conversation.messages.append(response)

                    # Execute each tool
                    for tc_data in tool_calls_data:
                        # Safely parse JSON arguments from LLM
                        try:
                            arguments = json.loads(tc_data["function"]["arguments"])
                        except json.JSONDecodeError as e:
                            logger.error(f"Failed to parse tool arguments: {e}")
                            # Add error message to conversation and continue
                            error_msg = Message(
                                role="tool",
                                content=f"Error: Invalid JSON in tool arguments: {e}",
                                metadata={
                                    "tool_call_id": tc_data["id"],
                                    "tool_name": tc_data["function"]["name"],
                                    "error": True
                                }
                            )
                            self.conversation.messages.append(error_msg)
                            continue

                        tool_call = ToolCall(
                            id=tc_data["id"],
                            name=tc_data["function"]["name"],
                            arguments=arguments
                        )

                        # Execute tool
                        tool_result = await self.tool_registry.execute(tool_call)

                        # Add tool result as message
                        tool_msg = Message(
                            role="tool",
                            content=tool_result.content,
                            metadata={
                                "tool_call_id": tool_result.tool_call_id,
                                "tool_name": tool_call.name,
                                "success": tool_result.success
                            }
                        )
                        self.conversation.messages.append(tool_msg)

                    # Continue loop to get next response

            # Max iterations reached
            raise RuntimeError("Tool loop exceeded maximum iterations")
```

**Tests:** `src/detective_agent/agent_test.py` (add to existing tests)
- Test tool registration
- Test tool loop with single tool call
- Test tool loop with multiple tool calls
- Test tool loop termination
- Test max iterations exceeded
- Test JSON parse error handling (malformed tool arguments)

**Acceptance Criteria for Step 6:**
- ✅ Tool abstraction interface defined
- ✅ Tools can be registered with agent
- ✅ Agent formats tools for provider API
- ✅ Tool execution loop works end-to-end
- ✅ get_release_summary returns mock data
- ✅ file_risk_report validates and saves reports
- ✅ Tool calls visible in conversation history
- ✅ Tool execution captured in traces
- ✅ Error handling for tool failures
- ✅ Automated tests for tools
- ✅ CLI demo of release assessment workflow

---

### Step 7: Evaluation System

**Goal:** Validate agent behavior through automated evaluation

#### 7.1 Evaluation Data Models

**File:** `evals/models.py`

```python
from pydantic import BaseModel
from typing import Literal, Any

class TestScenario(BaseModel):
    """A single evaluation test case"""
    id: str
    description: str
    release_data: dict
    expected_tools: list[str]
    expected_severity: Literal["high", "medium", "low"]
    expected_findings_keywords: list[str]

class ScenarioResult(BaseModel):
    """Result of running a single scenario"""
    scenario_id: str
    status: Literal["passed", "failed"]
    scores: dict[str, float]
    details: dict[str, Any]

class EvaluationReport(BaseModel):
    """Complete evaluation report"""
    summary: dict[str, Any]
    scenarios: list[ScenarioResult]
    regression_analysis: dict[str, Any] | None = None
```

#### 7.2 Test Scenarios

**File:** `evals/scenarios/release_assessment.json`

```json
[
  {
    "id": "high_risk_release",
    "description": "Release with test failures and elevated error rate",
    "release_data": {
      "version": "v2.1.0",
      "changes": ["Added payment processing", "Fixed authentication bug"],
      "tests": {"passed": 142, "failed": 5, "skipped": 5},
      "deployment_metrics": {
        "error_rate": 0.08,
        "response_time_p95": 450
      }
    },
    "expected_tools": ["get_release_summary", "file_risk_report"],
    "expected_severity": "high",
    "expected_findings_keywords": ["test failures", "error rate", "payment"]
  },
  {
    "id": "low_risk_release",
    "description": "Clean release with all tests passing",
    "release_data": {
      "version": "v2.0.0",
      "changes": ["Minor UI updates", "Performance improvements"],
      "tests": {"passed": 149, "failed": 0, "skipped": 0},
      "deployment_metrics": {
        "error_rate": 0.001,
        "response_time_p95": 320
      }
    },
    "expected_tools": ["get_release_summary", "file_risk_report"],
    "expected_severity": "low",
    "expected_findings_keywords": ["passing", "healthy", "low impact"]
  },
  {
    "id": "medium_risk_release",
    "description": "Release with minor issues",
    "release_data": {
      "version": "v1.9.0",
      "changes": ["Updated dependencies", "Minor bug fixes"],
      "tests": {"passed": 145, "failed": 1, "skipped": 3},
      "deployment_metrics": {
        "error_rate": 0.015,
        "response_time_p95": 380
      }
    },
    "expected_tools": ["get_release_summary", "file_risk_report"],
    "expected_severity": "medium",
    "expected_findings_keywords": ["minor", "slight", "moderate"]
  }
]
```

#### 7.3 Evaluation Runner

**File:** `evals/runner.py`

```python
import json
from pathlib import Path
from detective_agent.agent import DetectiveAgent
from evals.models import TestScenario, ScenarioResult, EvaluationReport

class EvaluationRunner:
    """Run evaluation scenarios against the agent"""

    def __init__(self, agent: DetectiveAgent):
        self.agent = agent

    async def run_scenario(self, scenario: TestScenario) -> ScenarioResult:
        """Run a single evaluation scenario"""
        # Start fresh conversation
        self.agent.new_conversation()

        # Send evaluation prompt
        prompt = f"Assess the risk for release {scenario.release_data['version']}"
        response = await self.agent.send_message(prompt)

        # Evaluate tool usage
        tool_usage_score = self._evaluate_tool_usage(scenario)

        # Evaluate decision quality
        decision_score = self._evaluate_decision_quality(scenario)

        # Determine pass/fail
        overall_score = (tool_usage_score + decision_score) / 2
        status = "passed" if overall_score >= 0.7 else "failed"

        return ScenarioResult(
            scenario_id=scenario.id,
            status=status,
            scores={
                "tool_usage": tool_usage_score,
                "decision_quality": decision_score,
                "overall": overall_score
            },
            details={
                "response": response,
                "conversation_id": self.agent.conversation.id
            }
        )

    def _evaluate_tool_usage(self, scenario: TestScenario) -> float:
        """Evaluate if correct tools were called"""
        messages = self.agent.conversation.messages
        tools_called = set()

        for msg in messages:
            if msg.role == "assistant" and "tool_calls" in msg.metadata:
                for tc in msg.metadata["tool_calls"]:
                    tools_called.add(tc["function"]["name"])

        expected_tools = set(scenario.expected_tools)
        if tools_called == expected_tools:
            return 1.0
        elif tools_called.intersection(expected_tools):
            return 0.5
        else:
            return 0.0

    def _evaluate_decision_quality(self, scenario: TestScenario) -> float:
        """Evaluate if severity and findings are correct"""
        # Find the risk report in conversation
        for msg in self.agent.conversation.messages:
            if msg.role == "tool" and "file_risk_report" in msg.metadata.get("tool_name", ""):
                try:
                    report = json.loads(msg.content)
                except:
                    # If content is not JSON, it might be the success message
                    continue

                # Check severity
                severity_correct = report.get("severity") == scenario.expected_severity

                # Check findings contain expected keywords
                findings_text = " ".join(report.get("findings", [])).lower()
                keywords_found = sum(
                    1 for kw in scenario.expected_findings_keywords
                    if kw.lower() in findings_text
                )
                keyword_score = keywords_found / len(scenario.expected_findings_keywords) if scenario.expected_findings_keywords else 0

                return (1.0 if severity_correct else 0.0) * 0.6 + keyword_score * 0.4

        return 0.0

    async def run_evaluation(self, scenarios: list[TestScenario]) -> EvaluationReport:
        """Run all scenarios and generate report"""
        results = []

        for scenario in scenarios:
            result = await self.run_scenario(scenario)
            results.append(result)

        # Calculate summary
        total = len(results)
        passed = sum(1 for r in results if r.status == "passed")
        avg_scores = {
            "tool_usage": sum(r.scores["tool_usage"] for r in results) / total,
            "decision_quality": sum(r.scores["decision_quality"] for r in results) / total,
            "overall": sum(r.scores["overall"] for r in results) / total,
        }

        return EvaluationReport(
            summary={
                "pass_rate": passed / total,
                "total_scenarios": total,
                "passed": passed,
                "failed": total - passed,
                "avg_scores": avg_scores
            },
            scenarios=results
        )

    def save_baseline(self, report: EvaluationReport, version: str) -> None:
        """Save evaluation results as baseline"""
        baseline_dir = Path("evals/baselines")
        baseline_dir.mkdir(parents=True, exist_ok=True)

        baseline_file = baseline_dir / f"{version}.json"
        with open(baseline_file, "w") as f:
            json.dump(report.model_dump(), f, indent=2)

    def compare_to_baseline(self, current: EvaluationReport, baseline_version: str) -> dict:
        """Compare current results to baseline"""
        baseline_file = Path(f"evals/baselines/{baseline_version}.json")
        with open(baseline_file) as f:
            baseline_data = json.load(f)
        baseline = EvaluationReport.model_validate(baseline_data)

        # Calculate deltas
        pass_rate_delta = current.summary["pass_rate"] - baseline.summary["pass_rate"]

        regressions = []
        improvements = []

        if pass_rate_delta < -0.05:
            regressions.append(f"Pass rate decreased by {abs(pass_rate_delta):.1%}")
        elif pass_rate_delta > 0.05:
            improvements.append(f"Pass rate increased by {pass_rate_delta:.1%}")

        return {
            "baseline_version": baseline_version,
            "pass_rate_delta": pass_rate_delta,
            "regressions": regressions,
            "improvements": improvements
        }
```

**Tests:** `evals/runner_test.py`
- Test scenario execution
- Test tool usage evaluation
- Test decision quality evaluation
- Test report generation
- Test baseline save/load
- Test regression comparison

**Acceptance Criteria for Step 7:**
- ✅ Eval framework runs scenarios automatically
- ✅ Tool usage evaluated for correctness
- ✅ Decision quality measured
- ✅ Test suite includes 5+ scenarios
- ✅ Regression tracking compares to baseline
- ✅ Structured JSON reports generated
- ✅ Eval results include pass/fail and diagnostics
- ✅ Automated tests verify eval framework
- ✅ Documentation for adding new eval cases
- ✅ CLI supports baseline establishment

---

## Testing Strategy

### Unit Tests
- Each module has co-located `_test.py` file
- Use `pytest` and `pytest-asyncio`
- Mock external dependencies with `respx`
- Aim for >80% code coverage (enforced via pytest-cov)

**Shared test fixtures:**
```python
# src/detective_agent/conftest.py
import pytest
from detective_agent.config import ProviderConfig, AgentConfig

@pytest.fixture
def mock_provider_config():
    """Provide a test configuration without real API key."""
    return ProviderConfig(api_key="test-key-not-real")

@pytest.fixture
def mock_agent_config(mock_provider_config):
    """Provide a test agent configuration."""
    return AgentConfig(provider=mock_provider_config)
```

**Example test structure:**
```python
# src/detective_agent/providers/openrouter_test.py
import pytest
import respx
from httpx import Response
from detective_agent.providers.openrouter import OpenRouterProvider
from detective_agent.config import ProviderConfig

@pytest.mark.asyncio
async def test_complete_success():
    """Test successful API call"""
    config = ProviderConfig(api_key="test-key")
    provider = OpenRouterProvider(config)

    with respx.mock:
        respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
            return_value=Response(200, json={
                "choices": [{"message": {"content": "Hello!"}}],
                "usage": {"total_tokens": 10}
            })
        )

        response = await provider.complete(
            messages=[Message(role="user", content="Hi")],
            temperature=0.7,
            max_tokens=100
        )

        assert response.content == "Hello!"
        assert response.role == "assistant"
```

### Integration Tests
- Located in `/tests/integration/`
- Test end-to-end workflows
- Support both real API and mock mode for CI/CD
- Verify conversation persistence and traces

**Test fixtures for mock mode:**
```python
# tests/integration/conftest.py
import os
import pytest
import httpx
import respx

@pytest.fixture
def use_real_api():
    """Skip test if no real API key available."""
    if not os.getenv("OPENROUTER_API_KEY"):
        pytest.skip("OPENROUTER_API_KEY not set - skipping real API test")

@pytest.fixture
def mock_openrouter(respx_mock):
    """Mock OpenRouter API for integration tests without real API key."""
    respx_mock.post("https://openrouter.ai/api/v1/chat/completions").mock(
        return_value=httpx.Response(200, json={
            "choices": [{"message": {"content": "Mocked response"}}],
            "usage": {"total_tokens": 10}
        })
    )
    return respx_mock
```

**Example integration test with mock support:**
```python
# tests/integration/test_agent_workflow.py
import os
import pytest
from detective_agent.agent import DetectiveAgent
from detective_agent.providers.openrouter import OpenRouterProvider
from detective_agent.config import AgentConfig, ProviderConfig

@pytest.mark.asyncio
async def test_full_conversation_workflow_mocked(mock_openrouter):
    """Test complete conversation with mocked API (runs in CI)"""
    config = AgentConfig(
        provider=ProviderConfig(api_key="test-key-for-mock")
    )
    async with OpenRouterProvider(config.provider) as provider:
        agent = DetectiveAgent(provider, config)

        # Send message (uses mock)
        response = await agent.send_message("Hello!")
        assert response == "Mocked response"

        # Verify conversation saved
        assert len(agent.conversation.messages) == 2  # user + assistant

@pytest.mark.asyncio
async def test_full_conversation_workflow_real(use_real_api):
    """Test with real API (only runs when API key available)"""
    config = AgentConfig(
        provider=ProviderConfig(api_key=os.getenv("OPENROUTER_API_KEY"))
    )
    async with OpenRouterProvider(config.provider) as provider:
        agent = DetectiveAgent(provider, config)

        # Send message
        response = await agent.send_message("Hello!")
        assert len(response) > 0

        # Verify conversation saved
        assert len(agent.conversation.messages) == 2  # user + assistant

        # Verify trace created
        trace_id = agent.conversation.metadata.get("trace_id")
        assert trace_id is not None
```

### Evaluation Tests
- Located in `/evals/`
- Test agent behavior and decision quality
- Track regressions over time
- Generate machine-readable reports

---

## Running the Agent

### CLI Usage
```bash
# Set API key
export OPENROUTER_API_KEY="your-key-here"

# Run CLI
python -m detective_agent.cli

# Run with specific model
export OPENROUTER_MODEL="meta-llama/llama-3.1-8b-instruct:free"
python -m detective_agent.cli
```

### Programmatic Usage
```python
from detective_agent.agent import DetectiveAgent
from detective_agent.providers.openrouter import OpenRouterProvider
from detective_agent.config import AgentConfig, ProviderConfig
from detective_agent.tools.release_tools import (
    GET_RELEASE_SUMMARY_TOOL,
    FILE_RISK_REPORT_TOOL
)

# Configure
provider_config = ProviderConfig(api_key="your-key")
agent_config = AgentConfig(provider=provider_config)

# Initialize
provider = OpenRouterProvider(provider_config)
agent = DetectiveAgent(provider, agent_config)

# Register tools
agent.register_tool(GET_RELEASE_SUMMARY_TOOL)
agent.register_tool(FILE_RISK_REPORT_TOOL)

# Use agent
response = await agent.send_message("Assess risk for release v2.1.0")
print(response)
```

### Running Evaluations
```bash
# Run evaluations
python -m evals.runner

# Save baseline
python -m evals.runner --save-baseline v1.0.0

# Compare to baseline
python -m evals.runner --compare-baseline v1.0.0
```

---

## Configuration Reference

### Environment Variables
- `OPENROUTER_API_KEY`: Required. API key for OpenRouter
- `OPENROUTER_MODEL`: Optional. Model to use (default: meta-llama/llama-3.1-8b-instruct:free)

### Context Window Settings (Truncation Strategy)
- `max_messages`: **6** (last 3 user + 3 assistant messages) - **User specified**
- `token_limit`: 128000 (Llama 3.1's context window)
- `reserve_tokens`: 4096 (reserved for response)
- `safety_margin`: 0.1 (10% buffer)

**Rationale for 6 messages:**
- Keeps recent context relevant
- Prevents token limit errors
- Simple and predictable behavior
- Sufficient for most release assessment tasks

### Retry Settings
- `max_attempts`: 3
- `initial_delay`: 1.0 seconds
- `max_delay`: 60.0 seconds
- `backoff_factor`: 2.0
- `jitter`: true

### Provider Settings (OpenRouter)
- `base_url`: https://openrouter.ai/api/v1
- `model`: meta-llama/llama-3.1-8b-instruct:free (default)
- `temperature`: 0.7
- `max_tokens`: 4096
- `timeout`: 30.0 seconds

---

## File Organization Summary

```
module6/project/
├── src/detective_agent/          # Main source code
│   ├── __init__.py
│   ├── models.py                  # Data models
│   ├── models_test.py             # Unit tests
│   ├── config.py                  # Configuration
│   ├── config_test.py             # Unit tests
│   ├── agent.py                   # Agent core
│   ├── agent_test.py              # Unit tests
│   ├── persistence.py             # Conversation storage
│   ├── persistence_test.py        # Unit tests
│   ├── cli.py                     # CLI interface
│   ├── providers/                 # Provider implementations
│   │   ├── __init__.py
│   │   ├── base.py                # Protocol
│   │   ├── openrouter.py          # OpenRouter provider
│   │   ├── openrouter_test.py     # Unit tests
│   │   └── errors.py              # Error types
│   ├── tools/                     # Tool framework
│   │   ├── __init__.py
│   │   ├── base.py                # Tool abstractions
│   │   ├── registry.py            # Tool registry
│   │   ├── registry_test.py       # Unit tests
│   │   ├── release_tools.py       # Release tools
│   │   ├── release_tools_test.py  # Unit tests
│   │   └── errors.py              # Error types
│   ├── context/                   # Context management
│   │   ├── __init__.py
│   │   ├── truncation.py          # Truncation strategy
│   │   └── truncation_test.py     # Unit tests
│   ├── retry/                     # Retry logic
│   │   ├── __init__.py
│   │   ├── backoff.py             # Exponential backoff
│   │   └── backoff_test.py        # Unit tests
│   └── observability/             # OpenTelemetry
│       ├── __init__.py
│       ├── tracing.py             # Tracing setup
│       └── exporter.py            # Filesystem exporter
├── tests/                         # Integration tests
│   ├── __init__.py
│   └── integration/
│       └── test_agent_workflow.py # End-to-end tests
├── evals/                         # Evaluation system
│   ├── __init__.py
│   ├── models.py                  # Eval data models
│   ├── runner.py                  # Eval runner
│   ├── runner_test.py             # Unit tests
│   ├── scenarios/                 # Test scenarios
│   │   └── release_assessment.json
│   ├── baselines/                 # Baseline results
│   └── reports/                   # Eval reports
├── data/                          # Runtime data
│   ├── conversations/             # Saved conversations
│   │   └── .gitkeep
│   ├── traces/                    # OpenTelemetry traces
│   │   └── .gitkeep
│   └── risk_reports/              # Filed risk reports
│       └── .gitkeep
├── .env.example                   # Environment variable template
├── .gitignore                     # Git ignore patterns
├── pyproject.toml                 # Project config
└── README.md                      # Documentation
```

---

## Pythonic Improvements Summary

This implementation incorporates modern Python best practices throughout:

### 1. **Type Safety & Clarity**
- **Type Aliases**: `MessageList`, `MessageRole`, `MetadataDict`, `ReleaseData` for complex types
- **Comprehensive Type Hints**: All functions and methods fully typed
- **Runtime Type Checking**: `@runtime_checkable` Protocol for provider interface

### 2. **Resource Management**
- **Async Context Managers**: `OpenRouterProvider` implements `__aenter__`/`__aexit__`
- **Automatic Cleanup**: Resources cleaned up even on exceptions
- **Property Guards**: Client property ensures initialization before use

### 3. **Configuration Management**
- **pydantic-settings**: Automatic environment variable loading
- **Type Validation**: Pydantic validates all config values
- **Defaults & Constraints**: Field validators ensure valid ranges (temperature 0-2, etc.)

### 4. **Error Handling**
- **Exception Chaining**: All `raise` statements use `from e` to preserve stack traces
- **Specific Exceptions**: Custom exception hierarchy for different error types
- **Structured Logging**: Logging with context instead of print statements

### 5. **Modern Python Features (3.10+)**
- **Pattern Matching**: CLI uses `match/case` for command handling
- **Union Types**: `X | None` instead of `Optional[X]`
- **Structural Pattern Matching**: Clean command dispatch

### 6. **Performance Optimizations**
- **__slots__**: Pydantic models use slots for reduced memory usage
- **Lazy Initialization**: HTTP client created only when needed
- **Efficient Path Operations**: pathlib.Path for cross-platform compatibility

### 7. **Datetime Handling**
- **Timezone-Aware**: `datetime.now(timezone.utc)` instead of deprecated `utcnow()`
- **ISO Format**: `.isoformat()` for JSON serialization
- **Consistent UTC**: All timestamps in UTC

### 8. **Type-Safe Constants**
- **Enums**: `RiskSeverity(str, Enum)` for severity levels
- **Literal Types**: `MessageRole` for message roles
- **Validation**: Enum validation with helpful error messages

### 9. **Documentation**
- **Google-Style Docstrings**: Args, Returns, Raises sections
- **Type Information**: Docstrings complement type hints
- **Examples**: Where helpful for complex APIs

### 10. **Testing Improvements**
- **Async Tests**: pytest-asyncio for async test support
- **Context Manager Tests**: Verify proper resource cleanup
- **Exception Chain Tests**: Verify `from e` preserves context

---

## Next Steps After Implementation

After completing all 7 steps, consider:

1. **Additional Providers**: Implement Anthropic and Ollama providers
2. **Advanced Context Management**: Add summarization strategy as alternative to truncation
3. **More Tools**: Add web search, file operations, code analysis
4. **Streaming Responses**: Support streaming for better UX
5. **Multi-Agent**: Coordinate multiple specialized agents
6. **Production Deployment**: Add monitoring, logging, error tracking
7. **Cost Tracking**: Track and report API costs per conversation
8. **Conversation Analytics**: Analyze patterns in agent behavior

---

## Success Criteria

The implementation is complete when:

### Functional Requirements
- ✅ Steps 1, 2, 4, 5, 6, 7 implemented with passing tests
- ✅ Agent can assess release risks using tools
- ✅ Full observability with OpenTelemetry traces
- ⏸️ Context window management (truncation) prevents token errors [DEFERRED]
- ⏸️ Last 6 messages retained (3 user + 3 assistant) [DEFERRED]
- ✅ Retry mechanism handles transient failures
- ✅ Evaluation system validates behavior
- ✅ OpenRouter provider fully functional
- ✅ CLI provides good user experience

### Code Quality & Pythonic Standards
- ✅ Type hints on all functions and methods
- ✅ Async context managers for resource management
- ✅ pydantic-settings for configuration
- ✅ Exception chaining with `from e`
- ✅ Pattern matching for control flow
- ✅ Logging instead of print statements
- ✅ Enums for type-safe constants
- ✅ pathlib.Path for file operations
- ✅ timezone-aware datetime handling
- ✅ Google-style docstrings

### Testing & Documentation
- ✅ All unit tests pass (>80% coverage)
- ✅ Integration tests verify end-to-end workflows
- ✅ Evaluation suite demonstrates agent capabilities
- ✅ Documentation is complete and clear
- ✅ Code is clean, readable, and well-tested

---

## Implementation Notes

### Key Design Decisions Made

1. **Provider Choice**: OpenRouter selected as first provider
   - Provides access to multiple models through single API
   - Compatible with OpenAI API format
   - Good for experimentation and cost optimization

2. **Context Window Strategy**: Truncation with 6 messages [DEFERRED]
   - Simple and predictable
   - Keeps most recent context
   - Prevents token limit errors
   - Easy to understand and debug
   - *Implementation deferred to future iteration*

3. **Tool Calling Format**: Anthropic-style tool definitions
   - Well-documented format
   - Supported by OpenRouter
   - Clean separation of tool definition and execution

4. **Observability**: OpenTelemetry with filesystem export
   - Standard format for traces
   - Easy to inspect during development
   - Can be upgraded to OTLP export later

5. **Testing Approach**: Co-located unit tests
   - Tests live next to code they test
   - Easy to find and maintain
   - Follows Python best practices

### Common Pitfalls to Avoid

1. **Don't use `pip`** - Always use `uv add` for dependencies
2. **Don't create `requirements.txt`** - Use `pyproject.toml`
3. **Don't use ABC** - Use Protocol for interfaces
4. **Don't put unit tests in `/tests`** - Co-locate with source
5. **Don't forget to activate venv** - Use `.venv/Scripts/python` on Windows
6. **Don't hardcode API keys** - Use environment variables
7. **Don't skip error handling** - Handle provider errors gracefully
8. **Don't ignore traces** - Use them for debugging

---

## Appendix: Quick Reference Commands

```bash
# Project setup
uv venv
uv add httpx pydantic pytest pytest-asyncio respx opentelemetry-api opentelemetry-sdk

# Run tests
.venv/Scripts/python -m pytest                    # All tests
.venv/Scripts/python -m pytest src/               # Unit tests only
.venv/Scripts/python -m pytest tests/             # Integration tests only
.venv/Scripts/python -m pytest -v                 # Verbose output
.venv/Scripts/python -m pytest --cov              # With coverage

# Run agent
export OPENROUTER_API_KEY="your-key"
.venv/Scripts/python -m detective_agent.cli

# Run evaluations
.venv/Scripts/python -m evals.runner
.venv/Scripts/python -m evals.runner --save-baseline v1.0.0
.venv/Scripts/python -m evals.runner --compare-baseline v1.0.0

# View traces
cat data/traces/<trace-id>.json | jq

# View conversations
cat data/conversations/<conversation-id>.json | jq

# View risk reports
cat data/risk_reports/<release-id>_risk_report.json | jq
```

---

**End of Implementation Plan**