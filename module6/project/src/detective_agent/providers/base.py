"""Base provider protocol and abstractions."""

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from detective_agent.models import Message
from detective_agent.types import MessageList


@dataclass(frozen=True, slots=True)
class ProviderCapabilities:
    """Capabilities supported by a provider.

    Used to determine what features a provider supports before attempting
    to use them (e.g., tool calling, streaming, vision).

    Attributes:
        supports_tools: Whether the provider supports function/tool calling.
        supports_streaming: Whether the provider supports streaming responses.
        supports_vision: Whether the provider supports image inputs.
        max_context_tokens: Maximum context window size in tokens.
    """

    supports_tools: bool = False
    supports_streaming: bool = False
    supports_vision: bool = False
    max_context_tokens: int = 128000


@runtime_checkable
class Provider(Protocol):
    """Protocol for LLM providers."""

    async def complete(
        self,
        messages: MessageList,
        temperature: float,
        max_tokens: int,
        tools: list[dict] | None = None,
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

