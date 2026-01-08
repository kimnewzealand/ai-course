"""OpenTelemetry tracing setup for the Investigator Agent.

Implements a simple file-based span exporter that writes JSON traces under
``config.traces_dir``. This is the concrete implementation of the plan in
PLAN_before.md Step 1.4.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor,
    SpanExportResult,
    SpanExporter,
)


class FileSpanExporter(SpanExporter):
    """Export spans to JSON files grouped by date.

    The layout is:

    ``traces_dir/YYYY-MM-DD/trace_HHMMSS.json``
    """

    def __init__(self, traces_dir: Path) -> None:
        self.traces_dir = traces_dir
        self.traces_dir.mkdir(parents=True, exist_ok=True)

    def export(self, spans: Iterable["trace.Span"]) -> SpanExportResult:
        """Export spans to a JSON file.

        This implementation is intentionally simple and optimized for
        debuggability rather than performance.
        """

        spans_list = list(spans)
        if not spans_list:
            return SpanExportResult.SUCCESS

        try:
            # Group by date
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            date_dir = self.traces_dir / date_str
            date_dir.mkdir(exist_ok=True)

            # File name based on time
            timestamp = now.strftime("%H%M%S")
            trace_file = date_dir / f"trace_{timestamp}.json"

            # Convert spans to serializable dicts
            trace_data = {
                "timestamp": now.isoformat(),
                "spans": [self._span_to_dict(span) for span in spans_list],
            }

            with trace_file.open("w", encoding="utf-8") as f:
                json.dump(trace_data, f, indent=2)

            return SpanExportResult.SUCCESS
        except Exception as exc:  # pragma: no cover - defensive
            print(f"Error exporting trace: {exc}")
            return SpanExportResult.FAILURE

    def _span_to_dict(self, span: Any) -> dict[str, Any]:
        """Convert a span to a JSON-serializable dictionary."""

        context = span.context
        return {
            "name": span.name,
            "span_id": f"{context.span_id:016x}" if context else None,
            "trace_id": f"{context.trace_id:032x}" if context else None,
            "start_time": span.start_time,
            "end_time": span.end_time,
            "duration_ns": (span.end_time - span.start_time) if span.end_time else 0,
            "attributes": dict(span.attributes) if getattr(span, "attributes", None) else {},
            "status": str(span.status.status_code) if getattr(span, "status", None) else "UNSET",
        }

    def shutdown(self) -> None:  # pragma: no cover - no-op
        """Shut down the exporter (no-op for file exporter)."""


def setup_tracing(traces_dir: Path) -> trace.Tracer:
    """Set up OpenTelemetry tracing with file-based exporter.

    Returns the configured :class:`trace.Tracer` instance.
    """

    resource = Resource.create({"service.name": "investigator-agent"})

    provider = TracerProvider(resource=resource)
    exporter = FileSpanExporter(traces_dir)
    processor = SimpleSpanProcessor(exporter)
    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)
    return trace.get_tracer(__name__)
