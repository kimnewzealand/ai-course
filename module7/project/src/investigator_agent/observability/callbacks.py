"""LangChain callbacks for OpenTelemetry tracing.

Implements :class:`TracingCallbackHandler` based on the Step 1.4 plan in
PLAN_before.md.
"""

from __future__ import annotations

from typing import Any, Dict, List

from langchain.callbacks.base import BaseCallbackHandler
from opentelemetry import trace


class TracingCallbackHandler(BaseCallbackHandler):
    """LangChain callback handler for OpenTelemetry tracing."""

    def __init__(self, tracer: trace.Tracer) -> None:
        self.tracer = tracer
        self.spans: Dict[Any, Any] = {}

    # LLM events ---------------------------------------------------------

    def on_llm_start(self, serialized: dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        """Start an LLM span when a model call begins."""

        run_id = kwargs.get("run_id")
        span = self.tracer.start_span("llm_call")
        span.set_attribute("model", serialized.get("name", "unknown"))
        span.set_attribute("prompts_count", len(prompts))
        self.spans[run_id] = span

    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        """End the LLM span and record token usage if available."""

        run_id = kwargs.get("run_id")
        span = self.spans.get(run_id)
        if not span:
            return

        # Extract token usage if provided by the backend
        llm_output = getattr(response, "llm_output", None)
        if isinstance(llm_output, dict):
            token_usage = llm_output.get("token_usage", {})
            span.set_attribute("input_tokens", token_usage.get("prompt_tokens", 0))
            span.set_attribute("output_tokens", token_usage.get("completion_tokens", 0))
            span.set_attribute("total_tokens", token_usage.get("total_tokens", 0))

        span.end()
        self.spans.pop(run_id, None)

    def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        """Record errors on the LLM span and end it."""

        run_id = kwargs.get("run_id")
        span = self.spans.get(run_id)
        if not span:
            return

        span.set_attribute("error", str(error))
        span.end()
        self.spans.pop(run_id, None)

    # Tool events --------------------------------------------------------

    def on_tool_start(self, serialized: dict[str, Any], input_str: str, **kwargs: Any) -> None:
        """Start a span for tool execution."""

        run_id = kwargs.get("run_id")
        span = self.tracer.start_span("tool_execution")
        span.set_attribute("tool_name", serialized.get("name", "unknown"))
        span.set_attribute("input", input_str[:500])
        self.spans[run_id] = span

    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """End the tool span and record (truncated) output."""

        run_id = kwargs.get("run_id")
        span = self.spans.get(run_id)
        if not span:
            return

        span.set_attribute("output", output[:500])
        span.end()
        self.spans.pop(run_id, None)

    def on_tool_error(self, error: Exception, **kwargs: Any) -> None:
        """Record errors on tool spans and end them."""

        run_id = kwargs.get("run_id")
        span = self.spans.get(run_id)
        if not span:
            return

        span.set_attribute("error", str(error))
        span.end()
        self.spans.pop(run_id, None)
