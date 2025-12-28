"""Filesystem-based trace exporter."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from detective_agent.observability.models import Trace


class FileTraceExporter:
    """Exports traces to JSON files on the filesystem.

    Creates human-readable trace files organized by date.
    """

    def __init__(self, output_dir: Path | str = "data/traces"):
        """Initialize the exporter.

        Args:
            output_dir: Directory to write trace files.
        """
        self.output_dir = Path(output_dir)

    def export(self, trace: Trace) -> Path:
        """Export a trace to a JSON file.

        Args:
            trace: The trace to export.

        Returns:
            Path to the created trace file.
        """
        # Create directory structure: traces/YYYY-MM-DD/
        date_dir = self.output_dir / trace.created_at.strftime("%Y-%m-%d")
        date_dir.mkdir(parents=True, exist_ok=True)

        # Create filename with timestamp and trace_id
        timestamp = trace.created_at.strftime("%H%M%S")
        filename = f"trace_{timestamp}_{trace.trace_id[:8]}.json"
        filepath = date_dir / filename

        # Convert trace to JSON-serializable format
        trace_data = self._serialize_trace(trace)

        # Write to file
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(trace_data, f, indent=2, default=str)

        return filepath

    def _serialize_trace(self, trace: Trace) -> dict[str, Any]:
        """Serialize a trace to a dictionary.

        Args:
            trace: The trace to serialize.

        Returns:
            JSON-serializable dictionary.
        """
        return {
            "trace_id": trace.trace_id,
            "service_name": trace.service_name,
            "created_at": trace.created_at.isoformat(),
            "duration_ms": trace.duration_ms,
            "attributes": trace.attributes,
            "spans": [self._serialize_span(span) for span in trace.spans],
        }

    def _serialize_span(self, span: Any) -> dict[str, Any]:
        """Serialize a span to a dictionary.

        Args:
            span: The span to serialize.

        Returns:
            JSON-serializable dictionary.
        """
        return {
            "trace_id": span.trace_id,
            "span_id": span.span_id,
            "parent_span_id": span.parent_span_id,
            "name": span.name,
            "kind": span.kind.value,
            "status": span.status.value,
            "start_time": span.start_time.isoformat(),
            "end_time": span.end_time.isoformat() if span.end_time else None,
            "duration_ms": span.duration_ms,
            "attributes": span.attributes,
            "events": span.events,
        }

    def list_traces(self, date: datetime | None = None) -> list[Path]:
        """List all trace files, optionally filtered by date.

        Args:
            date: Optional date to filter traces.

        Returns:
            List of trace file paths.
        """
        if date:
            date_dir = self.output_dir / date.strftime("%Y-%m-%d")
            if not date_dir.exists():
                return []
            return sorted(date_dir.glob("trace_*.json"))

        # Return all traces from all dates
        traces = []
        if self.output_dir.exists():
            for date_dir in sorted(self.output_dir.iterdir()):
                if date_dir.is_dir():
                    traces.extend(sorted(date_dir.glob("trace_*.json")))
        return traces

    def load_trace(self, filepath: Path) -> dict[str, Any]:
        """Load a trace from a file.

        Args:
            filepath: Path to the trace file.

        Returns:
            The trace data as a dictionary.
        """
        with open(filepath, encoding="utf-8") as f:
            return json.load(f)

