"""Tests for observability.tracer and observability.callbacks."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

from opentelemetry import trace

from investigator_agent.observability.callbacks import TracingCallbackHandler
from investigator_agent.observability.tracer import FileSpanExporter, setup_tracing


def test_file_span_exporter_writes_trace_file(tmp_path: Path) -> None:
    """FileSpanExporter should write a JSON file with spans."""

    exporter = FileSpanExporter(tmp_path)

    # Create a real tracer/span using OpenTelemetry SDK to ensure we have
    # compatible objects. This is a minimal in-memory provider.
    tracer_provider = trace.get_tracer_provider()
    tracer = tracer_provider.get_tracer(__name__)
    with tracer.start_as_current_span("test_span") as span:  # type: ignore[assignment]
        spans = [span]

    result = exporter.export(spans)
    assert result.name == "SUCCESS"

    # Verify a JSON trace file exists
    date_dirs = list(tmp_path.iterdir())
    assert date_dirs, "Expected date directory to be created"
    trace_files = list(date_dirs[0].iterdir())
    assert trace_files, "Expected at least one trace file"

    with trace_files[0].open(encoding="utf-8") as f:
        data = json.load(f)

    assert "spans" in data
    assert isinstance(data["spans"], list)
    assert data["spans"][0]["name"] == "test_span"


def test_setup_tracing_returns_tracer(tmp_path: Path) -> None:
    """setup_tracing should configure and return a tracer."""

    tracer = setup_tracing(tmp_path)
    assert isinstance(tracer, trace.Tracer)


def test_tracing_callback_handler_llm_span_lifecycle() -> None:
    """TracingCallbackHandler should create and finish LLM spans."""

    tracer = MagicMock()
    span = MagicMock()
    tracer.start_span.return_value = span

    handler = TracingCallbackHandler(tracer)
    run_id = "run-123"

    # Start
    handler.on_llm_start({"name": "test-model"}, ["prompt"], run_id=run_id)
    assert run_id in handler.spans

    # End with token usage
    response = SimpleNamespace(
        llm_output={
            "token_usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}
        }
    )
    handler.on_llm_end(response, run_id=run_id)

    # Span should be ended and removed
    span.set_attribute.assert_any_call("input_tokens", 10)
    span.set_attribute.assert_any_call("output_tokens", 5)
    span.set_attribute.assert_any_call("total_tokens", 15)
    span.end.assert_called_once()
    assert run_id not in handler.spans


def test_tracing_callback_handler_tool_span_lifecycle() -> None:
    """TracingCallbackHandler should create and finish tool spans."""

    tracer = MagicMock()
    span = MagicMock()
    tracer.start_span.return_value = span

    handler = TracingCallbackHandler(tracer)
    run_id = "tool-run-1"

    handler.on_tool_start({"name": "my_tool"}, "input-data", run_id=run_id)
    assert run_id in handler.spans

    handler.on_tool_end("output-data", run_id=run_id)
    span.set_attribute.assert_any_call("tool_name", "my_tool")
    span.set_attribute.assert_any_call("input", "input-data")
    span.set_attribute.assert_any_call("output", "output-data")
    span.end.assert_called_once()
    assert run_id not in handler.spans
