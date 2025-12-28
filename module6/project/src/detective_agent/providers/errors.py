"""Provider error classes for LLM API interactions."""


class ProviderError(Exception):
    """Base provider error."""

    pass


class AuthenticationError(ProviderError):
    """Invalid API key or credentials."""

    pass


class RateLimitError(ProviderError):
    """Provider rate limiting - retryable error."""

    pass


class ValidationError(ProviderError):
    """Invalid request format."""

    pass


class NetworkError(ProviderError):
    """Connection issues - retryable error."""

    pass


class TimeoutError(ProviderError):
    """Request timed out - retryable error."""

    pass

