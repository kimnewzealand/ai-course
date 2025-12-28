"""Shared type aliases for the detective agent package.

This module provides a single source of truth for all type aliases
used throughout the codebase, preventing duplication and ensuring consistency.
"""

from typing import Any, Literal, TypeAlias

from detective_agent.models import Message

# Message-related types
MessageList: TypeAlias = list[Message]
MessageRole: TypeAlias = Literal["user", "assistant", "system", "tool"]
MetadataDict: TypeAlias = dict[str, Any]

# Release-related types
ReleaseData: TypeAlias = dict[str, Any]

