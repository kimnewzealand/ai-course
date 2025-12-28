"""Tests for conversation persistence."""

import json
from pathlib import Path

import pytest

from detective_agent.models import Conversation
from detective_agent.persistence import ConversationStore


@pytest.fixture
def temp_store(tmp_path):
    """Create a ConversationStore with a temporary directory."""
    return ConversationStore(base_dir=tmp_path / "conversations")


@pytest.fixture
def sample_conversation():
    """Create a sample conversation for testing."""
    conv = Conversation(system_prompt="Test prompt")
    conv.add_message("user", "Hello!")
    conv.add_message("assistant", "Hi there!")
    return conv


class TestConversationStore:
    """Tests for ConversationStore."""

    def test_store_creates_directory(self, tmp_path):
        """Test that store creates base directory if it doesn't exist."""
        store_path = tmp_path / "new_dir" / "conversations"
        store = ConversationStore(base_dir=store_path)

        assert store_path.exists()
        assert store_path.is_dir()

    def test_save_conversation(self, temp_store, sample_conversation):
        """Test saving a conversation."""
        temp_store.save(sample_conversation)

        file_path = temp_store.base_dir / f"{sample_conversation.id}.json"
        assert file_path.exists()

        with open(file_path) as f:
            data = json.load(f)

        assert data["id"] == sample_conversation.id
        assert data["system_prompt"] == "Test prompt"
        assert len(data["messages"]) == 2

    def test_load_conversation(self, temp_store, sample_conversation):
        """Test loading a saved conversation."""
        temp_store.save(sample_conversation)

        loaded = temp_store.load(sample_conversation.id)

        assert loaded.id == sample_conversation.id
        assert loaded.system_prompt == sample_conversation.system_prompt
        assert len(loaded.messages) == 2
        assert loaded.messages[0].content == "Hello!"
        assert loaded.messages[1].content == "Hi there!"

    def test_load_nonexistent_conversation(self, temp_store):
        """Test that loading nonexistent conversation raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            temp_store.load("nonexistent-id")

    def test_list_conversations_empty(self, temp_store):
        """Test listing conversations when none exist."""
        conversations = temp_store.list_conversations()
        assert conversations == []

    def test_list_conversations(self, temp_store):
        """Test listing multiple conversations."""
        conv1 = Conversation(system_prompt="First")
        conv2 = Conversation(system_prompt="Second")
        conv3 = Conversation(system_prompt="Third")

        temp_store.save(conv1)
        temp_store.save(conv2)
        temp_store.save(conv3)

        conversations = temp_store.list_conversations()

        assert len(conversations) == 3
        assert conv1.id in conversations
        assert conv2.id in conversations
        assert conv3.id in conversations

    def test_round_trip_preserves_data(self, temp_store):
        """Test that save then load preserves all conversation data."""
        original = Conversation(
            system_prompt="Round trip test",
            metadata={"key": "value", "number": 42},
        )
        original.add_message("user", "First message")
        original.add_message("assistant", "Response message")
        original.add_message("user", "Follow up")

        temp_store.save(original)
        loaded = temp_store.load(original.id)

        assert loaded.id == original.id
        assert loaded.system_prompt == original.system_prompt
        assert len(loaded.messages) == len(original.messages)
        assert loaded.metadata["key"] == "value"
        assert loaded.metadata["number"] == 42

        for orig_msg, loaded_msg in zip(original.messages, loaded.messages):
            assert orig_msg.role == loaded_msg.role
            assert orig_msg.content == loaded_msg.content

    def test_save_overwrites_existing(self, temp_store, sample_conversation):
        """Test that saving again overwrites the existing file."""
        temp_store.save(sample_conversation)

        # Add more messages
        sample_conversation.add_message("user", "Another message")
        temp_store.save(sample_conversation)

        loaded = temp_store.load(sample_conversation.id)
        assert len(loaded.messages) == 3

    def test_store_with_path_object(self, tmp_path):
        """Test that store accepts Path objects."""
        store = ConversationStore(base_dir=tmp_path / "path_test")
        assert isinstance(store.base_dir, Path)

