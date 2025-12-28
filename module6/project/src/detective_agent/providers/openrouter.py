"""OpenRouter API provider implementation."""

import httpx
from httpx import Timeout

from detective_agent.config import ProviderConfig
from detective_agent.models import Message
from detective_agent.providers.base import ProviderCapabilities
from detective_agent.providers.errors import (
    AuthenticationError,
    NetworkError,
    ProviderError,
    RateLimitError,
    TimeoutError,
    ValidationError,
)
from detective_agent.types import MessageList


class OpenRouterProvider:
    """OpenRouter API provider with async context manager support."""

    def __init__(self, config: ProviderConfig):
        self.config = config
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "OpenRouterProvider":
        """Enter async context manager and initialize HTTP client."""
        self._client = httpx.AsyncClient(
            base_url=self.config.base_url,
            timeout=Timeout(
                connect=5.0,  # Fast fail on connection issues
                read=self.config.timeout,  # Allow longer read for LLM responses
                write=10.0,
                pool=5.0,
            ),
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "HTTP-Referer": "https://github.com/yourusername/detective-agent",
                "X-Title": "Detective Agent",
            },
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context manager and cleanup resources."""
        if self._client:
            await self._client.aclose()

    @property
    def client(self) -> httpx.AsyncClient:
        """Get HTTP client, ensuring it's initialized."""
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
            "stream": False,  # Disable streaming (required for tool support)
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
                "provider": "openrouter",
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
            ProviderCapabilities indicating what OpenRouter supports.
        """
        return ProviderCapabilities(
            supports_tools=True,
            supports_streaming=False,  # Not implemented yet
            supports_vision=False,  # Model-dependent, not implemented
            max_context_tokens=128000,  # Llama 3.1 context window
        )

