"""Data models for OpenTelemetry-style tracing."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class SpanStatus(str, Enum):
    """Status of a span execution."""

    UNSET = "unset"
    OK = "ok"
    ERROR = "error"


class SpanKind(str, Enum):
    """Kind of span for categorization."""

    INTERNAL = "internal"
    CLIENT = "client"  # Outgoing calls (e.g., LLM API)
    SERVER = "server"


class Span(BaseModel):
    """A single unit of work within a trace.

    Follows OpenTelemetry span semantics.
    """

    model_config = ConfigDict(frozen=False, slots=True)

    # Identity
    trace_id: str
    span_id: str = Field(default_factory=lambda: str(uuid4())[:16])
    parent_span_id: str | None = None
    name: str

    # Timing
    start_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: datetime | None = None

    # Classification
    kind: SpanKind = SpanKind.INTERNAL
    status: SpanStatus = SpanStatus.UNSET

    # Data
    attributes: dict[str, Any] = Field(default_factory=dict)
    events: list[dict[str, Any]] = Field(default_factory=list)

    def end(self, status: SpanStatus = SpanStatus.OK) -> None:
        """Mark the span as complete.

        Args:
            status: Final status of the span.
        """
        self.end_time = datetime.now(timezone.utc)
        self.status = status

    def set_attribute(self, key: str, value: Any) -> None:
        """Set an attribute on the span.

        Args:
            key: Attribute name.
            value: Attribute value.
        """
        self.attributes[key] = value

    def add_event(self, name: str, attributes: dict[str, Any] | None = None) -> None:
        """Add an event to the span.

        Args:
            name: Event name.
            attributes: Optional event attributes.
        """
        self.events.append({
            "name": name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "attributes": attributes or {},
        })

    @property
    def duration_ms(self) -> float | None:
        """Calculate span duration in milliseconds."""
        if self.end_time is None:
            return None
        delta = self.end_time - self.start_time
        return delta.total_seconds() * 1000


class Trace(BaseModel):
    """A collection of spans representing a complete operation.

    A trace represents the entire journey of a request/conversation.
    """

    model_config = ConfigDict(frozen=False, slots=True)

    trace_id: str = Field(default_factory=lambda: str(uuid4()))
    spans: list[Span] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Metadata for the trace
    service_name: str = "detective-agent"
    attributes: dict[str, Any] = Field(default_factory=dict)

    def add_span(self, span: Span) -> None:
        """Add a span to the trace.

        Args:
            span: The span to add.
        """
        self.spans.append(span)

    @property
    def root_span(self) -> Span | None:
        """Get the root span (no parent)."""
        for span in self.spans:
            if span.parent_span_id is None:
                return span
        return None

    @property
    def duration_ms(self) -> float | None:
        """Get total trace duration from root span."""
        root = self.root_span
        if root:
            return root.duration_ms
        return None

