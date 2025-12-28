"""Data models for the detective agent package."""

from datetime import datetime, timezone
from typing import Any, Literal, TypeAlias
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

# Type aliases for clarity
MessageRole: TypeAlias = Literal["user", "assistant", "system", "tool"]
MetadataDict: TypeAlias = dict[str, Any]


class Message(BaseModel):
    """Single message in a conversation."""

    model_config = ConfigDict(frozen=False, slots=True)

    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: MetadataDict = Field(default_factory=dict)


class Conversation(BaseModel):
    """Ongoing dialogue between user and agent."""

    model_config = ConfigDict(frozen=False, slots=True)

    id: str = Field(default_factory=lambda: str(uuid4()))
    system_prompt: str
    messages: list[Message] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: MetadataDict = Field(default_factory=dict)

    def add_message(self, role: MessageRole, content: str) -> Message:
        """Add a message to the conversation.

        Args:
            role: The role of the message sender.
            content: The message content.

        Returns:
            The created Message object.
        """
        msg = Message(role=role, content=content)
        self.messages.append(msg)
        return msg

