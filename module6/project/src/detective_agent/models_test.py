"""Tests for data models."""

from datetime import datetime, timezone

import pytest

from detective_agent.models import Conversation, Message


class TestMessage:
    """Tests for Message model."""

    def test_message_creation_with_defaults(self):
        """Test creating a message with default values."""
        msg = Message(role="user", content="Hello, world!")

        assert msg.role == "user"
        assert msg.content == "Hello, world!"
        assert isinstance(msg.timestamp, datetime)
        assert msg.metadata == {}

    def test_message_creation_with_all_fields(self):
        """Test creating a message with all fields specified."""
        timestamp = datetime.now(timezone.utc)
        metadata = {"source": "test"}

        msg = Message(
            role="assistant",
            content="Hi there!",
            timestamp=timestamp,
            metadata=metadata,
        )

        assert msg.role == "assistant"
        assert msg.content == "Hi there!"
        assert msg.timestamp == timestamp
        assert msg.metadata == {"source": "test"}

    def test_message_roles(self):
        """Test all valid message roles."""
        for role in ["user", "assistant", "system", "tool"]:
            msg = Message(role=role, content="test")
            assert msg.role == role

    def test_message_timestamp_is_utc(self):
        """Test that default timestamp is UTC."""
        msg = Message(role="user", content="test")
        # The timestamp should be close to now
        now = datetime.now(timezone.utc)
        diff = abs((now - msg.timestamp).total_seconds())
        assert diff < 1.0  # Within 1 second

    def test_message_json_serialization(self):
        """Test that messages can be serialized to JSON."""
        msg = Message(role="user", content="Hello")
        data = msg.model_dump()

        assert data["role"] == "user"
        assert data["content"] == "Hello"
        assert "timestamp" in data
        assert "metadata" in data


class TestConversation:
    """Tests for Conversation model."""

    def test_conversation_creation_with_defaults(self):
        """Test creating a conversation with default values."""
        conv = Conversation(system_prompt="You are helpful.")

        assert conv.system_prompt == "You are helpful."
        assert len(conv.id) > 0  # UUID should be generated
        assert conv.messages == []
        assert isinstance(conv.created_at, datetime)
        assert conv.metadata == {}

    def test_conversation_add_message(self):
        """Test adding messages to a conversation."""
        conv = Conversation(system_prompt="Test prompt")

        msg = conv.add_message("user", "Hello!")

        assert len(conv.messages) == 1
        assert conv.messages[0] == msg
        assert msg.role == "user"
        assert msg.content == "Hello!"

    def test_conversation_add_multiple_messages(self):
        """Test adding multiple messages."""
        conv = Conversation(system_prompt="Test")

        conv.add_message("user", "First")
        conv.add_message("assistant", "Second")
        conv.add_message("user", "Third")

        assert len(conv.messages) == 3
        assert conv.messages[0].content == "First"
        assert conv.messages[1].content == "Second"
        assert conv.messages[2].content == "Third"

    def test_conversation_unique_ids(self):
        """Test that each conversation gets a unique ID."""
        conv1 = Conversation(system_prompt="Test 1")
        conv2 = Conversation(system_prompt="Test 2")

        assert conv1.id != conv2.id

    def test_conversation_json_serialization(self):
        """Test that conversations can be serialized to JSON."""
        conv = Conversation(system_prompt="Test prompt")
        conv.add_message("user", "Hello")

        data = conv.model_dump()

        assert data["system_prompt"] == "Test prompt"
        assert len(data["messages"]) == 1
        assert data["messages"][0]["content"] == "Hello"
        assert "id" in data
        assert "created_at" in data

    def test_conversation_validation_from_dict(self):
        """Test creating conversation from dictionary (model_validate)."""
        data = {
            "id": "test-id-123",
            "system_prompt": "You are helpful.",
            "messages": [{"role": "user", "content": "Hi"}],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "metadata": {"key": "value"},
        }

        conv = Conversation.model_validate(data)

        assert conv.id == "test-id-123"
        assert conv.system_prompt == "You are helpful."
        assert len(conv.messages) == 1
        assert conv.metadata == {"key": "value"}

