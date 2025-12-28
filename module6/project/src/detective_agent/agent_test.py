"""Tests for DetectiveAgent."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from detective_agent.agent import DetectiveAgent
from detective_agent.config import AgentConfig, ProviderConfig
from detective_agent.models import Conversation, Message


@pytest.fixture
def mock_provider():
    """Create a mock provider."""
    provider = MagicMock()
    provider.complete = AsyncMock(
        return_value=Message(role="assistant", content="Mock response")
    )
    provider.temperature = 0.7
    provider.max_tokens = 4096
    return provider


@pytest.fixture
def agent_config(tmp_path):
    """Create an agent configuration with temp directories."""
    return AgentConfig(
        provider=ProviderConfig(api_key="test-key"),
        system_prompt="You are a test assistant.",
        conversation_dir=tmp_path / "conversations",
        trace_dir=tmp_path / "traces",
    )


@pytest.fixture
def agent(mock_provider, agent_config):
    """Create a DetectiveAgent with mock provider."""
    return DetectiveAgent(provider=mock_provider, config=agent_config)


class TestDetectiveAgent:
    """Tests for DetectiveAgent."""

    def test_agent_initialization(self, mock_provider, agent_config):
        """Test agent initialization."""
        agent = DetectiveAgent(provider=mock_provider, config=agent_config)

        assert agent.provider == mock_provider
        assert agent.config == agent_config
        assert agent.conversation is not None
        assert agent.conversation.system_prompt == "You are a test assistant."

    def test_agent_with_existing_conversation(self, mock_provider, agent_config):
        """Test agent with existing conversation."""
        existing_conv = Conversation(system_prompt="Existing prompt")
        existing_conv.add_message("user", "Previous message")

        agent = DetectiveAgent(
            provider=mock_provider, config=agent_config, conversation=existing_conv
        )

        assert agent.conversation == existing_conv
        assert len(agent.conversation.messages) == 1

    @pytest.mark.asyncio
    async def test_send_message(self, agent, mock_provider):
        """Test sending a message."""
        response = await agent.send_message("Hello!")

        assert response == "Mock response"
        assert len(agent.conversation.messages) == 2
        assert agent.conversation.messages[0].role == "user"
        assert agent.conversation.messages[0].content == "Hello!"
        assert agent.conversation.messages[1].role == "assistant"
        mock_provider.complete.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_message_includes_system_prompt(self, agent, mock_provider):
        """Test that send_message includes system prompt in provider call."""
        await agent.send_message("Test message")

        call_args = mock_provider.complete.call_args
        messages = call_args.kwargs["messages"]

        assert messages[0].role == "system"
        assert messages[0].content == "You are a test assistant."

    @pytest.mark.asyncio
    async def test_send_message_saves_conversation(self, agent):
        """Test that send_message saves conversation to store."""
        await agent.send_message("Save me!")

        # Verify conversation was saved
        loaded = agent.store.load(agent.conversation.id)
        assert loaded.id == agent.conversation.id
        assert len(loaded.messages) == 2

    def test_get_history(self, agent):
        """Test getting conversation history."""
        agent.conversation.add_message("user", "First")
        agent.conversation.add_message("assistant", "Second")
        agent.conversation.add_message("user", "Third")

        history = agent.get_history()

        assert len(history) == 3
        assert history[0].content == "First"
        assert history[2].content == "Third"

    def test_get_history_with_limit(self, agent):
        """Test getting limited conversation history."""
        agent.conversation.add_message("user", "First")
        agent.conversation.add_message("assistant", "Second")
        agent.conversation.add_message("user", "Third")
        agent.conversation.add_message("assistant", "Fourth")

        history = agent.get_history(limit=2)

        assert len(history) == 2
        assert history[0].content == "Third"
        assert history[1].content == "Fourth"

    def test_new_conversation(self, agent):
        """Test starting a new conversation."""
        old_id = agent.conversation.id
        agent.conversation.add_message("user", "Old message")

        agent.new_conversation()

        assert agent.conversation.id != old_id
        assert len(agent.conversation.messages) == 0
        assert agent.conversation.system_prompt == "You are a test assistant."

    @pytest.mark.asyncio
    async def test_multiple_messages_in_conversation(self, agent, mock_provider):
        """Test multiple message exchanges."""
        mock_provider.complete = AsyncMock(
            side_effect=[
                Message(role="assistant", content="First response"),
                Message(role="assistant", content="Second response"),
            ]
        )

        response1 = await agent.send_message("First question")
        response2 = await agent.send_message("Second question")

        assert response1 == "First response"
        assert response2 == "Second response"
        assert len(agent.conversation.messages) == 4

