"""Tests for observability module."""

import json
import time
from pathlib import Path

import pytest

from detective_agent.observability import (
    FileTraceExporter,
    Span,
    SpanKind,
    SpanStatus,
    Trace,
    Tracer,
    reset_tracer,
)


class TestSpan:
    """Tests for Span model."""

    def test_span_creation(self):
        """Test creating a span with required fields."""
        span = Span(trace_id="trace-123", name="test-span")

        assert span.trace_id == "trace-123"
        assert span.name == "test-span"
        assert span.span_id is not None
        assert span.parent_span_id is None
        assert span.status == SpanStatus.UNSET
        assert span.kind == SpanKind.INTERNAL

    def test_span_end(self):
        """Test ending a span sets time and status."""
        span = Span(trace_id="trace-123", name="test-span")
        assert span.end_time is None

        span.end(SpanStatus.OK)

        assert span.end_time is not None
        assert span.status == SpanStatus.OK

    def test_span_duration(self):
        """Test span duration calculation."""
        span = Span(trace_id="trace-123", name="test-span")
        time.sleep(0.01)  # 10ms
        span.end()

        assert span.duration_ms is not None
        assert span.duration_ms >= 10  # At least 10ms

    def test_span_set_attribute(self):
        """Test setting attributes on span."""
        span = Span(trace_id="trace-123", name="test-span")

        span.set_attribute("key", "value")
        span.set_attribute("count", 42)

        assert span.attributes["key"] == "value"
        assert span.attributes["count"] == 42

    def test_span_add_event(self):
        """Test adding events to span."""
        span = Span(trace_id="trace-123", name="test-span")

        span.add_event("request_started", {"url": "http://example.com"})

        assert len(span.events) == 1
        assert span.events[0]["name"] == "request_started"
        assert span.events[0]["attributes"]["url"] == "http://example.com"


class TestTrace:
    """Tests for Trace model."""

    def test_trace_creation(self):
        """Test creating a trace."""
        trace = Trace()

        assert trace.trace_id is not None
        assert trace.spans == []
        assert trace.service_name == "detective-agent"

    def test_trace_add_span(self):
        """Test adding spans to trace."""
        trace = Trace()
        span = Span(trace_id=trace.trace_id, name="test-span")

        trace.add_span(span)

        assert len(trace.spans) == 1
        assert trace.spans[0].name == "test-span"

    def test_trace_root_span(self):
        """Test getting root span."""
        trace = Trace()
        root = Span(trace_id=trace.trace_id, name="root")
        child = Span(trace_id=trace.trace_id, name="child", parent_span_id=root.span_id)

        trace.add_span(root)
        trace.add_span(child)

        assert trace.root_span == root


class TestTracer:
    """Tests for Tracer."""

    def setup_method(self):
        """Reset global tracer before each test."""
        reset_tracer()

    def test_tracer_start_trace(self):
        """Test starting a trace."""
        tracer = Tracer()
        trace = tracer.start_trace()

        assert trace is not None
        assert tracer.get_current_trace() == trace

    def test_tracer_span_context_manager(self):
        """Test span as context manager."""
        tracer = Tracer()
        tracer.start_trace()

        with tracer.span("test-operation") as span:
            assert span.name == "test-operation"
            assert tracer.get_current_span() == span

        assert span.end_time is not None
        assert span.status == SpanStatus.OK

    def test_tracer_nested_spans(self):
        """Test nested span parent-child relationship."""
        tracer = Tracer()
        tracer.start_trace()

        with tracer.span("parent") as parent_span:
            with tracer.span("child") as child_span:
                assert child_span.parent_span_id == parent_span.span_id

    def test_tracer_span_error_handling(self):
        """Test span captures errors."""
        tracer = Tracer()
        tracer.start_trace()

        with pytest.raises(ValueError):
            with tracer.span("failing-op") as span:
                raise ValueError("Test error")

        assert span.status == SpanStatus.ERROR
        assert span.attributes["error.type"] == "ValueError"

    def test_tracer_no_trace_raises(self):
        """Test span creation without trace raises error."""
        tracer = Tracer()

        with pytest.raises(RuntimeError, match="No active trace"):
            with tracer.span("orphan"):
                pass


class TestFileTraceExporter:
    """Tests for FileTraceExporter."""

    def test_export_creates_file(self, tmp_path: Path):
        """Test exporting a trace creates a JSON file."""
        exporter = FileTraceExporter(tmp_path)
        trace = Trace()
        span = Span(trace_id=trace.trace_id, name="test-span")
        span.end()
        trace.add_span(span)

        filepath = exporter.export(trace)

        assert filepath.exists()
        assert filepath.suffix == ".json"

    def test_export_json_format(self, tmp_path: Path):
        """Test exported file is valid JSON with expected structure."""
        exporter = FileTraceExporter(tmp_path)
        trace = Trace()
        span = Span(trace_id=trace.trace_id, name="test-span")
        span.set_attribute("key", "value")
        span.end()
        trace.add_span(span)

        filepath = exporter.export(trace)

        with open(filepath) as f:
            data = json.load(f)

        assert data["trace_id"] == trace.trace_id
        assert len(data["spans"]) == 1
        assert data["spans"][0]["name"] == "test-span"
        assert data["spans"][0]["attributes"]["key"] == "value"

    def test_list_traces(self, tmp_path: Path):
        """Test listing exported traces."""
        exporter = FileTraceExporter(tmp_path)

        # Export two traces
        for _ in range(2):
            trace = Trace()
            span = Span(trace_id=trace.trace_id, name="test")
            span.end()
            trace.add_span(span)
            exporter.export(trace)

        traces = exporter.list_traces()
        assert len(traces) == 2

    def test_load_trace(self, tmp_path: Path):
        """Test loading a trace from file."""
        exporter = FileTraceExporter(tmp_path)
        trace = Trace()
        span = Span(trace_id=trace.trace_id, name="test-span")
        span.end()
        trace.add_span(span)

        filepath = exporter.export(trace)
        loaded = exporter.load_trace(filepath)

        assert loaded["trace_id"] == trace.trace_id

