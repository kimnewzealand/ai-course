"""Tracer for creating and managing spans."""

from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Generator

from detective_agent.observability.models import Span, SpanKind, SpanStatus, Trace

# Context variable to track current span
_current_span: ContextVar[Span | None] = ContextVar("current_span", default=None)


class Tracer:
    """Creates and manages traces and spans.

    Provides a context manager interface for automatic span lifecycle management.
    """

    def __init__(self, service_name: str = "detective-agent"):
        """Initialize tracer.

        Args:
            service_name: Name of the service for trace metadata.
        """
        self.service_name = service_name
        self._current_trace: Trace | None = None

    def start_trace(self, attributes: dict[str, Any] | None = None) -> Trace:
        """Start a new trace.

        Args:
            attributes: Optional attributes for the trace.

        Returns:
            The new Trace object.
        """
        self._current_trace = Trace(
            service_name=self.service_name,
            attributes=attributes or {},
        )
        return self._current_trace

    def get_current_trace(self) -> Trace | None:
        """Get the current active trace."""
        return self._current_trace

    def end_trace(self) -> Trace | None:
        """End and return the current trace.

        Returns:
            The completed trace or None if no trace was active.
        """
        trace = self._current_trace
        self._current_trace = None
        _current_span.set(None)
        return trace

    @contextmanager
    def span(
        self,
        name: str,
        kind: SpanKind = SpanKind.INTERNAL,
        attributes: dict[str, Any] | None = None,
    ) -> Generator[Span, None, None]:
        """Create a span as a context manager.

        Automatically handles timing and parent-child relationships.

        Args:
            name: Name of the span.
            kind: Kind of span (internal, client, server).
            attributes: Optional initial attributes.

        Yields:
            The active span.

        Raises:
            RuntimeError: If no trace is active.
        """
        if self._current_trace is None:
            raise RuntimeError("No active trace. Call start_trace() first.")

        # Get parent span if any
        parent_span = _current_span.get()
        parent_id = parent_span.span_id if parent_span else None

        # Create new span
        span = Span(
            trace_id=self._current_trace.trace_id,
            parent_span_id=parent_id,
            name=name,
            kind=kind,
            attributes=attributes or {},
        )

        # Add to trace
        self._current_trace.add_span(span)

        # Set as current span
        token = _current_span.set(span)

        try:
            yield span
            span.end(SpanStatus.OK)
        except Exception as e:
            span.set_attribute("error.type", type(e).__name__)
            span.set_attribute("error.message", str(e))
            span.end(SpanStatus.ERROR)
            raise
        finally:
            # Restore previous span
            _current_span.reset(token)

    def get_current_span(self) -> Span | None:
        """Get the current active span."""
        return _current_span.get()


# Global tracer instance
_global_tracer: Tracer | None = None


def get_tracer(service_name: str = "detective-agent") -> Tracer:
    """Get or create the global tracer instance.

    Args:
        service_name: Service name for the tracer.

    Returns:
        The global Tracer instance.
    """
    global _global_tracer
    if _global_tracer is None:
        _global_tracer = Tracer(service_name)
    return _global_tracer


def reset_tracer() -> None:
    """Reset the global tracer (useful for testing)."""
    global _global_tracer
    _global_tracer = None
    _current_span.set(None)

