"""Tests for OpenRouter provider."""

import httpx
import pytest
import respx
from httpx import Response

from detective_agent.config import ProviderConfig
from detective_agent.models import Message
from detective_agent.providers.errors import (
    AuthenticationError,
    NetworkError,
    ProviderError,
    RateLimitError,
    TimeoutError,
    ValidationError,
)
from detective_agent.providers.openrouter import OpenRouterProvider


@pytest.fixture
def provider_config():
    """Create a test provider configuration."""
    return ProviderConfig(api_key="test-api-key")


@pytest.fixture
def sample_messages():
    """Create sample messages for testing."""
    return [
        Message(role="system", content="You are helpful."),
        Message(role="user", content="Hello!"),
    ]


def mock_completion_response(content: str = "Hello there!"):
    """Create a mock completion response."""
    return {
        "choices": [{"message": {"content": content}}],
        "model": "test-model",
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
    }


class TestOpenRouterProvider:
    """Tests for OpenRouterProvider."""

    @pytest.mark.asyncio
    async def test_context_manager_initializes_client(self, provider_config):
        """Test that async context manager initializes the client."""
        provider = OpenRouterProvider(provider_config)

        assert provider._client is None

        async with provider:
            assert provider._client is not None
            assert isinstance(provider._client, httpx.AsyncClient)

        # Client should be closed after exiting
        assert provider._client is not None  # Still assigned but closed

    @pytest.mark.asyncio
    async def test_client_property_raises_without_context(self, provider_config):
        """Test that accessing client without context manager raises."""
        provider = OpenRouterProvider(provider_config)

        with pytest.raises(RuntimeError) as exc_info:
            _ = provider.client

        assert "async with" in str(exc_info.value)

    @pytest.mark.asyncio
    @respx.mock
    async def test_complete_success(self, provider_config, sample_messages):
        """Test successful completion."""
        respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
            return_value=Response(200, json=mock_completion_response("Hi!"))
        )

        async with OpenRouterProvider(provider_config) as provider:
            response = await provider.complete(
                messages=sample_messages, temperature=0.7, max_tokens=100
            )

        assert response.role == "assistant"
        assert response.content == "Hi!"
        assert response.metadata["provider"] == "openrouter"

    @pytest.mark.asyncio
    @respx.mock
    async def test_complete_with_tools(self, provider_config, sample_messages):
        """Test completion with tools parameter."""
        route = respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
            return_value=Response(200, json=mock_completion_response())
        )

        tools = [{"type": "function", "function": {"name": "test_tool"}}]

        async with OpenRouterProvider(provider_config) as provider:
            await provider.complete(
                messages=sample_messages, temperature=0.7, max_tokens=100, tools=tools
            )

        # Verify tools were included in request
        request_body = route.calls[0].request.content
        import json

        body = json.loads(request_body)
        assert "tools" in body
        assert body["tools"] == tools

    @pytest.mark.asyncio
    @respx.mock
    async def test_complete_always_disables_streaming(self, provider_config, sample_messages):
        """Test that streaming is always disabled (required for tool support)."""
        route = respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
            return_value=Response(200, json=mock_completion_response())
        )

        async with OpenRouterProvider(provider_config) as provider:
            await provider.complete(
                messages=sample_messages, temperature=0.7, max_tokens=100
            )

        import json

        body = json.loads(route.calls[0].request.content)
        assert body.get("stream") is False

    @pytest.mark.asyncio
    @respx.mock
    async def test_complete_authentication_error(self, provider_config, sample_messages):
        """Test 401 response raises AuthenticationError."""
        respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
            return_value=Response(401, json={"error": "Invalid API key"})
        )

        async with OpenRouterProvider(provider_config) as provider:
            with pytest.raises(AuthenticationError) as exc_info:
                await provider.complete(
                    messages=sample_messages, temperature=0.7, max_tokens=100
                )

        assert exc_info.value.__cause__ is not None  # Exception chaining

    @pytest.mark.asyncio
    @respx.mock
    async def test_complete_rate_limit_error(self, provider_config, sample_messages):
        """Test 429 response raises RateLimitError."""
        respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
            return_value=Response(429, json={"error": "Rate limited"})
        )

        async with OpenRouterProvider(provider_config) as provider:
            with pytest.raises(RateLimitError) as exc_info:
                await provider.complete(
                    messages=sample_messages, temperature=0.7, max_tokens=100
                )

        assert exc_info.value.__cause__ is not None

    @pytest.mark.asyncio
    @respx.mock
    async def test_complete_validation_error(self, provider_config, sample_messages):
        """Test 400 response raises ValidationError."""
        respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
            return_value=Response(400, json={"error": "Invalid request"})
        )

        async with OpenRouterProvider(provider_config) as provider:
            with pytest.raises(ValidationError):
                await provider.complete(
                    messages=sample_messages, temperature=0.7, max_tokens=100
                )

    @pytest.mark.asyncio
    @respx.mock
    async def test_complete_server_error(self, provider_config, sample_messages):
        """Test 500 response raises ProviderError."""
        respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
            return_value=Response(500, json={"error": "Internal server error"})
        )

        async with OpenRouterProvider(provider_config) as provider:
            with pytest.raises(ProviderError) as exc_info:
                await provider.complete(
                    messages=sample_messages, temperature=0.7, max_tokens=100
                )

        assert "500" in str(exc_info.value)

    def test_estimate_tokens_empty_messages(self, provider_config):
        """Test token estimation with empty message list."""
        provider = OpenRouterProvider(provider_config)
        tokens = provider.estimate_tokens([])
        assert tokens == 0

    def test_estimate_tokens_single_message(self, provider_config):
        """Test token estimation with single message."""
        provider = OpenRouterProvider(provider_config)
        messages = [Message(role="user", content="Hello world")]

        tokens = provider.estimate_tokens(messages)

        # "Hello world" is 11 chars -> ~2 tokens + 4 overhead = ~6
        assert tokens > 0
        assert tokens == (11 // 4) + 4  # 2 + 4 = 6

    def test_estimate_tokens_multiple_messages(self, provider_config):
        """Test token estimation with multiple messages."""
        provider = OpenRouterProvider(provider_config)
        messages = [
            Message(role="system", content="You are helpful."),  # 16 chars
            Message(role="user", content="Hi"),  # 2 chars
            Message(role="assistant", content="Hello!"),  # 6 chars
        ]

        tokens = provider.estimate_tokens(messages)

        # (16 + 2 + 6) // 4 = 6 content tokens + 3 * 4 = 12 overhead = 18
        expected = (16 + 2 + 6) // 4 + (3 * 4)
        assert tokens == expected

    @pytest.mark.asyncio
    @respx.mock
    async def test_complete_includes_usage_metadata(
        self, provider_config, sample_messages
    ):
        """Test that response includes usage metadata."""
        respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
            return_value=Response(200, json=mock_completion_response())
        )

        async with OpenRouterProvider(provider_config) as provider:
            response = await provider.complete(
                messages=sample_messages, temperature=0.7, max_tokens=100
            )

        assert "usage" in response.metadata
        assert response.metadata["usage"]["total_tokens"] == 15

    @pytest.mark.asyncio
    @respx.mock
    async def test_complete_formats_messages_correctly(
        self, provider_config, sample_messages
    ):
        """Test that messages are formatted correctly in request."""
        import json

        route = respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
            return_value=Response(200, json=mock_completion_response())
        )

        async with OpenRouterProvider(provider_config) as provider:
            await provider.complete(
                messages=sample_messages, temperature=0.7, max_tokens=100
            )

        request_body = json.loads(route.calls[0].request.content)
        assert len(request_body["messages"]) == 2
        assert request_body["messages"][0]["role"] == "system"
        assert request_body["messages"][0]["content"] == "You are helpful."
        assert request_body["messages"][1]["role"] == "user"

    @pytest.mark.asyncio
    @respx.mock
    async def test_complete_extracts_tool_calls_from_response(
        self, provider_config, sample_messages
    ):
        """Test that tool_calls are extracted from response and stored in metadata."""
        tool_calls_response = {
            "choices": [
                {
                    "message": {
                        "content": None,
                        "tool_calls": [
                            {
                                "id": "call_123",
                                "type": "function",
                                "function": {
                                    "name": "get_weather",
                                    "arguments": '{"location": "NYC"}',
                                },
                            }
                        ],
                    }
                }
            ],
            "model": "test-model",
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        }

        respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
            return_value=Response(200, json=tool_calls_response)
        )

        async with OpenRouterProvider(provider_config) as provider:
            response = await provider.complete(
                messages=sample_messages, temperature=0.7, max_tokens=100
            )

        assert "tool_calls" in response.metadata
        assert len(response.metadata["tool_calls"]) == 1
        assert response.metadata["tool_calls"][0]["id"] == "call_123"
        assert response.content == ""  # Content should be empty string, not None

    @pytest.mark.asyncio
    @respx.mock
    async def test_complete_formats_assistant_messages_with_tool_calls(
        self, provider_config
    ):
        """Test that assistant messages with tool_calls are formatted correctly."""
        import json

        route = respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
            return_value=Response(200, json=mock_completion_response())
        )

        # Message with tool_calls in metadata (simulating conversation history)
        messages_with_tool_calls = [
            Message(role="system", content="You are helpful."),
            Message(role="user", content="What's the weather?"),
            Message(
                role="assistant",
                content="",
                metadata={
                    "tool_calls": [
                        {
                            "id": "call_123",
                            "type": "function",
                            "function": {"name": "get_weather", "arguments": "{}"},
                        }
                    ]
                },
            ),
            Message(
                role="tool",
                content='{"temp": 72}',
                metadata={"tool_call_id": "call_123", "name": "get_weather"},
            ),
        ]

        async with OpenRouterProvider(provider_config) as provider:
            await provider.complete(
                messages=messages_with_tool_calls, temperature=0.7, max_tokens=100
            )

        request_body = json.loads(route.calls[0].request.content)

        # Assistant message should include tool_calls
        assistant_msg = request_body["messages"][2]
        assert "tool_calls" in assistant_msg
        assert assistant_msg["content"] is None

        # Tool message should include tool_call_id
        tool_msg = request_body["messages"][3]
        assert tool_msg["tool_call_id"] == "call_123"

    def test_get_capabilities(self, provider_config):
        """Test that get_capabilities returns correct values."""
        provider = OpenRouterProvider(provider_config)
        caps = provider.get_capabilities()

        assert caps.supports_tools is True
        assert caps.supports_streaming is False
        assert caps.supports_vision is False
        assert caps.max_context_tokens == 128000

